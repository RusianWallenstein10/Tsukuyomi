import os
from typing import List
from supabase import create_client, Client
from src.domain.entities import Activity
from src.domain.ports import ActivityRepository

class SupabaseRepository(ActivityRepository):
    def __init__(self, supabase_url: str, supabase_key: str):
        self.supabase: Client = create_client(supabase_url, supabase_key)
        self.table_name = "horarios"

    def add_activity(self, activity: Activity) -> Activity:
        data = {
            "actividad": activity.actividad,
            "fase": activity.fase,
            "inicio": activity.inicio,
            "fin": activity.fin,
            "categoria": activity.categoria
        }
        response = self.supabase.table(self.table_name).insert(data).execute()
        
        if response.data:
            inserted_id = response.data[0].get("id", 0)
            activity.id = inserted_id
        return activity

    def get_activities(self) -> List[Activity]:
        response = self.supabase.table(self.table_name).select("*").execute()
        
        activities = []
        for row in response.data:
            activities.append(Activity(
                id=row.get("id"),
                actividad=row.get("actividad"),
                fase=row.get("fase"),
                inicio=row.get("inicio"),
                fin=row.get("fin"),
                categoria=row.get("categoria")
            ))
        return activities

    def delete_activity(self, activity_id: int) -> None:
        self.supabase.table(self.table_name).delete().eq("id", activity_id).execute()
