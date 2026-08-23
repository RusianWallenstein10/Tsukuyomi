import requests
from src.domain.ports import NotificationService

class TelegramNotificationService(NotificationService):
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def send_notification(self, message: str) -> None:
        if not self.bot_token or not self.chat_id:
            # Si no hay configuración, no hacemos nada (o podríamos loguear un warning)
            return
            
        payload = {
            "chat_id": self.chat_id,
            "text": message
        }
        try:
            requests.post(self.base_url, json=payload, timeout=5)
        except Exception as e:
            print(f"Error enviando notificación a Telegram: {e}")
