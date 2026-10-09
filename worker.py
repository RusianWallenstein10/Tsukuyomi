import os
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from dotenv import load_dotenv
from src.models.supabase_dao import SupabaseRepository
from src.services.telegram_service import TelegramNotificationService
from src.models.entities import Task

class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Tsukuyomi Worker is running 24/7!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), DummyHandler)
    print(f"🌐 Servidor fantasma corriendo en el puerto {port} (Para calmar a Render.com)")
    server.serve_forever()

def main():
    print("🌙 Iniciando Tsukuyomi Notification Worker (Bidireccional)...")
    threading.Thread(target=run_dummy_server, daemon=True).start()
    load_dotenv(override=True)
    
    supabase_url = os.environ.get("SUPABASE_URL", "")
    supabase_key = os.environ.get("SUPABASE_KEY", "")
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    
    if not all([supabase_url, supabase_key, bot_token]):
        print("❌ Error: Faltan variables de entorno (.env).")
        return
        
    repo = SupabaseRepository(supabase_url, supabase_key)
    notifier = TelegramNotificationService(bot_token)
    
    notified_events = set()
    last_update_id = None
    last_schedule_check = 0
    
    print("✅ Worker conectado a Supabase y Telegram. Escuchando comandos (Multi-Usuario)...")
    
    while True:
        try:
            # 1. ESCUCHAR MENSAJES (LONG POLLING 5 SEG)
            updates = notifier.get_updates(offset=last_update_id)
            if updates and "result" in updates:
                for update in updates["result"]:
                    last_update_id = update["update_id"] + 1
                    message = update.get("message", {})
                    text = message.get("text", "")
                    chat_id_in = str(message.get("chat", {}).get("id", ""))
                    
                    if text.startswith("/tarea "):
                        task_title = text.replace("/tarea ", "").strip()
                        if task_title and chat_id_in:
                            # Buscar usuario dueño de este chat_id
                            user_id = repo.get_user_id_by_telegram_chat_id(chat_id_in)
                            if user_id:
                                new_task = Task(id=0, titulo=task_title, project_id=None, estado="Pendiente")
                                repo.add_task(new_task, user_id)
                                notifier.send_notification(f"✅ Tarea añadida al Kanban: {task_title}", chat_id_in)
                                print(f"📥 Tarea de usuario {user_id}: {task_title}", flush=True)
                            else:
                                notifier.send_notification("❌ No estás registrado. Ve a Tsukuyomi Web > Mi Perfil y vincula este número de ID de Telegram.", chat_id_in)
            
            # 2. REVISAR HORARIOS (CADA 60 SEG)
            current_time = time.time()
            if current_time - last_schedule_check >= 60:
                last_schedule_check = current_time
                res = repo.supabase.table("horarios").select("*").eq("is_deleted", False).execute()
                activities = res.data if hasattr(res, 'data') else []
                now = datetime.now()
                
                # Cache user chat_ids so we don't query the DB 100 times if not needed
                user_chats = {}
                
                for act in activities:
                    try:
                        fase_str = act.get('fase', '')
                        inicio_str = act.get('inicio', '')
                        act_user_id = act.get('user_id')
                        
                        if not fase_str or not inicio_str or not act_user_id:
                            continue
                            
                        if len(inicio_str.split(':')) == 3:
                            inicio_str = ':'.join(inicio_str.split(':')[:2])
                            
                        act_time = datetime.strptime(inicio_str, "%H:%M").time()
                        act_dt = datetime.combine(now.date(), act_time)
                    except Exception:
                        continue
                    
                    # Fetch user chat ID
                    if act_user_id not in user_chats:
                        user_chats[act_user_id] = repo.get_telegram_chat_id(act_user_id)
                    
                    user_chat_id = user_chats[act_user_id]
                    if not user_chat_id:
                        continue # El usuario no ha vinculado Telegram
                    
                    time_diff = act_dt - now
                    minutes_left = time_diff.total_seconds() / 60.0
                    
                    id_exact = f"{act['id']}_{now.date()}_exact"
                    id_20min = f"{act['id']}_{now.date()}_20min"
                    
                    if 19.0 <= minutes_left <= 21.0 and id_20min not in notified_events:
                        notifier.send_notification(f"⏳ Recordatorio: En 20 minutos empieza '{act['actividad']}'.", user_chat_id)
                        notified_events.add(id_20min)
                        
                    if -1.0 <= minutes_left <= 1.0 and id_exact not in notified_events:
                        notifier.send_notification(f"🚀 ¡Es hora! Comenzando: '{act['actividad']}'.", user_chat_id)
                        notified_events.add(id_exact)
                        
        except Exception as e:
            print(f"⚠️ Error en el ciclo del worker: {e}")
            
        time.sleep(5) # Bucle corto para que responda rápido en Telegram

if __name__ == "__main__":
    main()
