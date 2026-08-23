import os
import hashlib
from typing import List, Optional
from supabase import create_client, Client
from src.domain.entities import Activity
from src.domain.ports import ActivityRepository

class SupabaseRepository(ActivityRepository):
    def __init__(self, supabase_url: str, supabase_key: str):
        self.supabase: Client = create_client(supabase_url, supabase_key)
        self.table_name = "horarios"

    # --- CUSTOM AUTHENTICATION ---
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def create_user(self, username: str, password: str) -> Optional[int]:
        data = {
            "username": username,
            "password_hash": self._hash_password(password)
        }
        res = self.supabase.table("usuarios").insert(data).execute()
        if hasattr(res, 'data') and res.data:
            return res.data[0]['id']
        return None

    def authenticate_user(self, username: str, password: str) -> Optional[int]:
        hashed = self._hash_password(password)
        res = self.supabase.table("usuarios").select("id").eq("username", username).eq("password_hash", hashed).execute()
        if hasattr(res, 'data') and res.data:
            return res.data[0]['id']
        return None

    # --- CRUD OPERATIONS ---

    def add_activity(self, activity: Activity, user_id: int) -> Activity:
        data = {
            "actividad": activity.actividad,
            "fase": activity.fase,
            "inicio": activity.inicio,
            "fin": activity.fin,
            "categoria": activity.categoria,
            "user_id": user_id
        }
        response = self.supabase.table(self.table_name).insert(data).execute()
        if hasattr(response, 'data') and response.data:
            act_data = response.data[0]
            return Activity(
                id=act_data['id'],
                actividad=act_data['actividad'],
                fase=act_data['fase'],
                inicio=act_data['inicio'],
                fin=act_data['fin'],
                categoria=act_data['categoria']
            )
        return activity

    def get_activities(self, user_id: int) -> List[Activity]:
        response = self.supabase.table(self.table_name).select("*").eq("user_id", user_id).execute()
        activities = []
        if hasattr(response, 'data'):
            for item in response.data:
                activities.append(Activity(
                    id=item['id'],
                    actividad=item['actividad'],
                    fase=item['fase'],
                    inicio=item['inicio'],
                    fin=item['fin'],
                    categoria=item['categoria']
                ))
        return activities

    def update_activity(self, activity: Activity, user_id: int) -> Activity:
        data = {
            "actividad": activity.actividad,
            "fase": activity.fase,
            "inicio": activity.inicio,
            "fin": activity.fin,
            "categoria": activity.categoria
        }
        response = self.supabase.table(self.table_name).update(data).eq("id", activity.id).eq("user_id", user_id).execute()
        return activity

    def delete_activity(self, activity_id: int, user_id: int) -> None:
        self.supabase.table(self.table_name).delete().eq("id", activity_id).eq("user_id", user_id).execute()

    # Configuraciones (Background)
    def save_config(self, key: str, value: str, user_id: int) -> None:
        data = {"key": key, "value": value, "user_id": user_id}
        self.supabase.table("app_config").upsert(data).execute()

    def get_config(self, key: str, user_id: int) -> str:
        response = self.supabase.table("app_config").select("value").eq("key", key).eq("user_id", user_id).execute()
        if hasattr(response, 'data') and response.data:
            return response.data[0]['value']
        return ""
