import requests
from src.models.repository import NotificationService


class TelegramNotificationService(NotificationService):
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def send_notification(self, message: str, chat_id: str = None) -> None:
        if not self.bot_token or not chat_id:
            return

        payload = {
            "chat_id": chat_id,
            "text": message
        }
        try:
            requests.post(self.base_url, json=payload, timeout=5)
        except Exception as e:
            print(f"Error enviando notificación a Telegram: {e}")

    def get_updates(self, offset: int = None) -> dict:
        if not self.bot_token:
            return {}
        
        url = f"https://api.telegram.org/bot{self.bot_token}/getUpdates"
        params = {"timeout": 10} # Long polling
        if offset:
            params["offset"] = offset
            
        try:
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error obteniendo actualizaciones de Telegram: {e}")
        return {}
