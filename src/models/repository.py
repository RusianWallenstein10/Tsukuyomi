from abc import ABC, abstractmethod
from typing import List
from src.models.entities import Activity, Area, Objective, Project, Task, Habit, HabitLog, Reflection


class TsukuyomiRepository(ABC):
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

    # --- TSUKUYOMI PHASE 3 ---
    @abstractmethod
    def add_area(self, area: Area, user_id: int) -> Area: pass
    @abstractmethod
    def get_areas(self, user_id: int) -> List[Area]: pass
    
    @abstractmethod
    def add_objective(self, obj: Objective, user_id: int) -> Objective: pass
    @abstractmethod
    def get_objectives(self, user_id: int) -> List[Objective]: pass
    
    @abstractmethod
    def add_project(self, proj: Project, user_id: int) -> Project: pass
    @abstractmethod
    def get_projects(self, user_id: int) -> List[Project]: pass
    @abstractmethod
    def update_project(self, proj: Project, user_id: int) -> Project: pass
    
    @abstractmethod
    def add_task(self, task: Task, user_id: int) -> Task: pass
    @abstractmethod
    def get_tasks(self, user_id: int) -> List[Task]: pass
    @abstractmethod
    def update_task(self, task: Task, user_id: int) -> Task: pass

    # --- TSUKUYOMI PHASE 4 ---
    @abstractmethod
    def add_habit(self, habit: Habit, user_id: int) -> Habit: pass
    @abstractmethod
    def get_habits(self, user_id: int) -> List[Habit]: pass
    @abstractmethod
    def log_habit(self, habit_log: HabitLog, user_id: int) -> HabitLog: pass
    @abstractmethod
    def get_habit_logs(self, user_id: int, fecha: str) -> List[HabitLog]: pass

    # --- TSUKUYOMI PHASE 5 ---
    @abstractmethod
    def add_reflection(self, reflection: Reflection, user_id: int) -> Reflection: pass
    @abstractmethod
    def get_reflections(self, user_id: int, tipo: str = None) -> List[Reflection]: pass



class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, message: str) -> None:
        pass
