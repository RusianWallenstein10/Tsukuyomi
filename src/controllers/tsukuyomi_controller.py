from typing import List, Optional
from src.models.entities import Activity, Area, Objective, Project, Task, Habit, HabitLog, Reflection
from src.models.repository import TsukuyomiRepository, NotificationService


class TsukuyomiUseCases:
    def __init__(self, repository: TsukuyomiRepository,
                 notifier: Optional[NotificationService] = None):
        self.repository = repository
        self.notifier = notifier

    # --- ACTIVITY (HORARIOS) ---
    def add_activity(
            self,
            user_id: int,
            actividad: str,
            fase: str,
            inicio: str,
            fin: str,
            categoria: str,
            task_id: Optional[int] = None,
            habit_id: Optional[int] = None) -> Activity:
        activity = Activity(id=0, actividad=actividad, fase=fase,
                            inicio=inicio, fin=fin, categoria=categoria, task_id=task_id, habit_id=habit_id)
        saved_activity = self.repository.add_activity(activity, user_id)

        if self.notifier:
            msg = (
                f"Nueva actividad creada: {actividad} "
                f"para el {fase} a las {inicio}."
            )
            self.notifier.send_notification(msg)

        return saved_activity

    def get_all_activities(self, user_id: int) -> List[Activity]:
        return self.repository.get_activities(user_id)

    def delete_activity(self, activity_id: int, user_id: int) -> None:
        self.repository.delete_activity(activity_id, user_id)
        if self.notifier:
            self.notifier.send_notification(
                f"Actividad eliminada (ID: {activity_id}).")

    def update_activity(
            self,
            activity_id: int,
            user_id: int,
            actividad: str,
            fase: str,
            inicio: str,
            fin: str,
            categoria: str) -> Activity:
        activity = Activity(
            id=activity_id,
            actividad=actividad,
            fase=fase,
            inicio=inicio,
            fin=fin,
            categoria=categoria)
        updated_act = self.repository.update_activity(activity, user_id)
        if self.notifier:
            msg = (
                f"🔄 Se ha actualizado el ritual "
                f"'{actividad}' en el Tsukuyomi."
            )
            self.notifier.send_notification(msg)
        return updated_act

    # --- AREA (IKIGAI) ---
    def add_area(self, user_id: int, nombre: str, vision: Optional[str] = None) -> Area:
        area = Area(id=0, nombre=nombre, vision=vision)
        return self.repository.add_area(area, user_id)

    def get_areas(self, user_id: int) -> List[Area]:
        return self.repository.get_areas(user_id)

    # --- OBJECTIVE ---
    def add_objective(self, user_id: int, titulo: str, area_id: Optional[int] = None) -> Objective:
        obj = Objective(id=0, titulo=titulo, area_id=area_id, estado="Activo")
        return self.repository.add_objective(obj, user_id)

    def get_objectives(self, user_id: int) -> List[Objective]:
        return self.repository.get_objectives(user_id)

    # --- PROJECT (KANBAN) ---
    def add_project(self, user_id: int, nombre: str, objective_id: Optional[int] = None) -> Project:
        proj = Project(id=0, nombre=nombre, objective_id=objective_id, estado="Backlog")
        return self.repository.add_project(proj, user_id)

    def get_projects(self, user_id: int) -> List[Project]:
        return self.repository.get_projects(user_id)

    def update_project_status(self, project_id: int, user_id: int, nuevo_estado: str) -> Project:
        # Check WIP Limit
        if nuevo_estado == "En progreso":
            projs = self.repository.get_projects(user_id)
            wip_count = sum(1 for p in projs if p.estado == "En progreso")
            if wip_count >= 3:
                msg_err = "⚠️ Límite WIP Excedido: Ya tienes 3 proyectos en progreso. Aplica 5S y termina uno antes de comenzar otro."
                if self.notifier:
                    self.notifier.send_notification(msg_err)
                raise ValueError(msg_err)
        
        projs = self.repository.get_projects(user_id)
        proj = next((p for p in projs if p.id == project_id), None)
        if not proj:
            raise ValueError("Proyecto no encontrado.")
        proj.estado = nuevo_estado
        res = self.repository.update_project(proj, user_id)
        
        if self.notifier and nuevo_estado == "Completado":
            self.notifier.send_notification(f"🏆 ¡Proyecto Completado! Has finalizado el proyecto: {proj.nombre}")
        
        return res

    # --- TASK ---
    def add_task(self, user_id: int, titulo: str, project_id: Optional[int] = None) -> Task:
        task = Task(id=0, titulo=titulo, project_id=project_id, estado="Pendiente")
        return self.repository.add_task(task, user_id)

    def get_tasks(self, user_id: int) -> List[Task]:
        return self.repository.get_tasks(user_id)

    def update_task_status(self, task_id: int, user_id: int, nuevo_estado: str) -> Task:
        tasks = self.repository.get_tasks(user_id)
        task = next((t for t in tasks if t.id == task_id), None)
        if not task:
            raise ValueError("Tarea no encontrada.")
        task.estado = nuevo_estado
        res = self.repository.update_task(task, user_id)
        
        if self.notifier and nuevo_estado == "Completada":
            self.notifier.send_notification(f"🎯 Tarea Completada: {task.titulo}")
            
        return res

    # --- HABITS (SHUKAN) ---
    def add_habit(self, user_id: int, nombre: str, objective_id: Optional[int] = None) -> Habit:
        habit = Habit(id=0, nombre=nombre, frecuencia="Diario", objective_id=objective_id)
        return self.repository.add_habit(habit, user_id)

    def get_habits(self, user_id: int) -> List[Habit]:
        return self.repository.get_habits(user_id)

    def log_habit(self, user_id: int, habit_id: int, fecha: str, estado: bool) -> HabitLog:
        log = HabitLog(id=0, habit_id=habit_id, fecha=fecha, estado=estado)
        res = self.repository.log_habit(log, user_id)
        
        if self.notifier and estado:
            habits = self.repository.get_habits(user_id)
            h_nombre = next((h.nombre for h in habits if h.id == habit_id), "Desconocido")
            self.notifier.send_notification(f"✅ Hábito logrado: {h_nombre}")
            
        return res

    def get_habit_logs(self, user_id: int, fecha: str) -> List[HabitLog]:
        return self.repository.get_habit_logs(user_id, fecha)

    # --- HANSEI (REFLEXIÓN) ---
    def add_reflection(self, user_id: int, tipo: str, fecha: str, respuestas: dict) -> Reflection:
        reflection = Reflection(id=0, tipo=tipo, fecha=fecha, respuestas=respuestas)
        res = self.repository.add_reflection(reflection, user_id)
        
        if self.notifier:
            self.notifier.send_notification(f"🧘‍♂️ Reflexión {tipo} guardada para el {fecha}. ¡Sigue mejorando (Kaizen)!")
            
        return res

    def get_reflections(self, user_id: int, tipo: str = None) -> List[Reflection]:
        return self.repository.get_reflections(user_id, tipo)
