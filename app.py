import streamlit as st
import os
from dotenv import load_dotenv
from src.controllers.tsukuyomi_controller import TsukuyomiUseCases
from src.models.supabase_dao import SupabaseRepository
from src.services.telegram_service import TelegramNotificationService
from src.views.styles import inject_styles
from src.views.components import login_register_view, main_app_view

load_dotenv(override=True)
st.set_page_config(page_title="Tsukuyomi", page_icon="🌙", layout="wide")

@st.cache_resource
def get_use_cases():
    supabase_url = os.environ.get("SUPABASE_URL", "")
    supabase_key = os.environ.get("SUPABASE_KEY", "")
    repo = SupabaseRepository(supabase_url, supabase_key)
    
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    notifier = TelegramNotificationService(token, chat_id) if token and chat_id else None
    
    return TsukuyomiUseCases(repo, notifier)

use_cases = get_use_cases()

import threading
import time
from datetime import datetime

@st.cache_resource
def start_telegram_scheduler():
    def scheduler_loop():
        from src.models.supabase_dao import SupabaseRepository
        from src.services.telegram_service import TelegramNotificationService
        import os
        from dotenv import load_dotenv

        load_dotenv(override=True)
        supabase_url = os.environ.get("SUPABASE_URL", "")
        supabase_key = os.environ.get("SUPABASE_KEY", "")
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
        
        if not all([supabase_url, supabase_key, bot_token, chat_id]):
            return
            
        repo = SupabaseRepository(supabase_url, supabase_key)
        notifier = TelegramNotificationService(bot_token, chat_id)
        
        notified_events = set()
        
        while True:
            try:
                res = repo.client.table("activities").select("*").execute()
                activities = res.data
                now = datetime.now()
                
                for act in activities:
                    try:
                        fase_str = act.get('fase', '')
                        inicio_str = act.get('inicio', '')
                        
                        if not fase_str or not inicio_str:
                            continue
                            
                        # Limpiar formato de hora si trae segundos (HH:MM:SS -> HH:MM)
                        if len(inicio_str.split(':')) == 3:
                            inicio_str = ':'.join(inicio_str.split(':')[:2])
                            
                        act_datetime_str = f"{fase_str} {inicio_str}"
                        act_time = datetime.strptime(act_datetime_str, "%Y-%m-%d %H:%M")
                    except Exception:
                        continue
                    
                    time_diff = act_time - now
                    minutes_left = time_diff.total_seconds() / 60.0
                    
                    id_exact = f"{act['id']}_exact"
                    id_20min = f"{act['id']}_20min"
                    
                    # Avisar 20 minutos antes (entre 19.0 y 21.0 mins para dar margen de 1 min)
                    if 19.0 <= minutes_left <= 21.0 and id_20min not in notified_events:
                        notifier.send_notification(f"⏳ Recordatorio: En 20 minutos empieza '{act['actividad']}'.")
                        notified_events.add(id_20min)
                        
                    # Avisar a la hora exacta
                    if -1.0 <= minutes_left <= 1.0 and id_exact not in notified_events:
                        notifier.send_notification(f"🚀 ¡Es hora! Comenzando: '{act['actividad']}'.")
                        notified_events.add(id_exact)
                        
            except Exception as e:
                print(f"Scheduler DB error: {e}")
                
            time.sleep(60)

    t = threading.Thread(target=scheduler_loop, daemon=True)
    t.start()
    return t

start_telegram_scheduler()

inject_styles()

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if st.session_state.user_id is None:
    login_register_view(use_cases.repository)
else:
    main_app_view(use_cases)
