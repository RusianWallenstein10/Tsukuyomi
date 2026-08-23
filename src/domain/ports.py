from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities import Activity

class ActivityRepository(ABC):
    @abstractmethod
    def save_config(self, key: str, value: str, user_id: int) -> None:
        pass

    @abstractmethod
    def get_config(self, key: str, user_id: int) -> str:
        pass

    @abstractmethod
    def add_activity(self, activity: Activity, user_id: int) -> Activity:
        pass

    @abstractmethod
    def get_activities(self, user_id: int) -> List[Activity]:
        pass

    @abstractmethod
    def delete_activity(self, activity_id: int, user_id: int) -> None:
        pass

    @abstractmethod
    def update_activity(self, activity: Activity, user_id: int) -> Activity:
        pass

class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, message: str) -> None:
        pass
