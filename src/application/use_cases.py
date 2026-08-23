from typing import List
from src.domain.entities import Activity
from src.domain.ports import ActivityRepository, NotificationService

class ActivityUseCases:
    def __init__(self, repository: ActivityRepository, notifier: NotificationService = None):
        self.repository = repository
        self.notifier = notifier

    def add_activity(self, user_id: int, actividad: str, fase: str, inicio: str, fin: str, categoria: str) -> Activity:
        activity = Activity(id=0, actividad=actividad, fase=fase, inicio=inicio, fin=fin, categoria=categoria)
        saved_activity = self.repository.add_activity(activity, user_id)
        
        if self.notifier:
            self.notifier.send_notification(f"Nueva actividad creada: {actividad} para el {fase} a las {inicio}.")
            
        return saved_activity

    def get_all_activities(self, user_id: int) -> List[Activity]:
        return self.repository.get_activities(user_id)

    def delete_activity(self, activity_id: int, user_id: int) -> None:
        self.repository.delete_activity(activity_id, user_id)
        if self.notifier:
            self.notifier.send_notification(f"Actividad eliminada (ID: {activity_id}).")

    def update_activity(self, activity_id: int, user_id: int, actividad: str, fase: str, inicio: str, fin: str, categoria: str) -> Activity:
        activity = Activity(
            id=activity_id, actividad=actividad, fase=fase, inicio=inicio, fin=fin, categoria=categoria
        )
        updated_act = self.repository.update_activity(activity, user_id)
        if self.notifier:
            self.notifier.send_notification(f"🔄 Se ha actualizado el ritual '{actividad}' en el Tsukuyomi.")
        return updated_act
