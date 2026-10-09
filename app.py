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
    notifier = TelegramNotificationService(token) if token else None
    
    return TsukuyomiUseCases(repo, notifier)

use_cases = get_use_cases()

# Scheduler movido a Edge Functions / Worker para evitar cuellos de botella en Streamlit

inject_styles()

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if st.session_state.user_id is None:
    login_register_view(use_cases.repository)
else:
    main_app_view(use_cases)
