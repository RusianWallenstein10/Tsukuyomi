from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities import Activity

class ActivityRepository(ABC):
    @abstractmethod
    def add_activity(self, activity: Activity) -> Activity:
        pass

    @abstractmethod
    def get_activities(self) -> List[Activity]:
        pass

    @abstractmethod
    def delete_activity(self, activity_id: int) -> None:
        pass

class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, message: str) -> None:
        pass
