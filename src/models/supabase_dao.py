import hashlib
from typing import List, Optional
from supabase import create_client, Client
from src.models.entities import Activity, Area, Objective, Project, Task, Habit, HabitLog, Reflection
from src.models.repository import TsukuyomiRepository


class SupabaseRepository(TsukuyomiRepository):
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
        res = self.supabase.table("usuarios").select("id").eq(
            "username", username).eq("password_hash", hashed).execute()
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
            "task_id": activity.task_id,
            "habit_id": activity.habit_id,
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
        response = self.supabase.table(self.table_name).select(
            "*").eq("user_id", user_id).execute()
        activities = []
        if hasattr(response, 'data'):
            for item in response.data:
                activities.append(Activity(
                    id=item['id'],
                    actividad=item['actividad'],
                    fase=item['fase'],
                    inicio=item['inicio'],
                    fin=item['fin'],
                    categoria=item['categoria'],
                    task_id=item.get('task_id'),
                    habit_id=item.get('habit_id')
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
        self.supabase.table(self.table_name).update(data).eq(
            "id", activity.id).eq("user_id", user_id).execute()
        return activity

    def delete_activity(self, activity_id: int, user_id: int) -> None:
        self.supabase.table(self.table_name).delete().eq(
            "id", activity_id).eq("user_id", user_id).execute()

    # Configuraciones (Background)
    def save_config(self, key: str, value: str, user_id: int) -> None:
        data = {"key": key, "value": value, "user_id": user_id}
        self.supabase.table("app_config").upsert(data).execute()

    def get_config(self, key: str, user_id: int) -> str:
        response = self.supabase.table("app_config").select(
            "value").eq("key", key).eq("user_id", user_id).execute()
        if hasattr(response, 'data') and response.data:
            return response.data[0]['value']
        return ""

    # --- TSUKUYOMI PHASE 3 ---

    def add_area(self, area: Area, user_id: int) -> Area:
        data = {"nombre": area.nombre, "vision": area.vision, "user_id": user_id}
        res = self.supabase.table("areas").insert(data).execute()
        if hasattr(res, 'data') and res.data:
            d = res.data[0]
            return Area(id=d['id'], nombre=d['nombre'], vision=d.get('vision'))
        return area

    def get_areas(self, user_id: int) -> List[Area]:
        res = self.supabase.table("areas").select("*").eq("user_id", user_id).execute()
        return [Area(id=d['id'], nombre=d['nombre'], vision=d.get('vision')) for d in res.data] if hasattr(res, 'data') else []

    def add_objective(self, obj: Objective, user_id: int) -> Objective:
        data = {"titulo": obj.titulo, "estado": obj.estado, "area_id": obj.area_id, "user_id": user_id}
        res = self.supabase.table("objectives").insert(data).execute()
        if hasattr(res, 'data') and res.data:
            d = res.data[0]
            return Objective(id=d['id'], titulo=d['titulo'], estado=d['estado'], area_id=d.get('area_id'))
        return obj

    def get_objectives(self, user_id: int) -> List[Objective]:
        res = self.supabase.table("objectives").select("*").eq("user_id", user_id).execute()
        return [Objective(id=d['id'], titulo=d['titulo'], estado=d['estado'], area_id=d.get('area_id')) for d in res.data] if hasattr(res, 'data') else []

    def add_project(self, proj: Project, user_id: int) -> Project:
        data = {"nombre": proj.nombre, "estado": proj.estado, "objective_id": proj.objective_id, "user_id": user_id}
        res = self.supabase.table("projects").insert(data).execute()
        if hasattr(res, 'data') and res.data:
            d = res.data[0]
            return Project(id=d['id'], nombre=d['nombre'], estado=d['estado'], objective_id=d.get('objective_id'))
        return proj

    def get_projects(self, user_id: int) -> List[Project]:
        res = self.supabase.table("projects").select("*").eq("user_id", user_id).execute()
        return [Project(id=d['id'], nombre=d['nombre'], estado=d['estado'], objective_id=d.get('objective_id')) for d in res.data] if hasattr(res, 'data') else []

    def update_project(self, proj: Project, user_id: int) -> Project:
        data = {"nombre": proj.nombre, "estado": proj.estado, "objective_id": proj.objective_id}
        self.supabase.table("projects").update(data).eq("id", proj.id).eq("user_id", user_id).execute()
        return proj

    def add_task(self, task: Task, user_id: int) -> Task:
        data = {"titulo": task.titulo, "estado": task.estado, "project_id": task.project_id, "user_id": user_id}
        res = self.supabase.table("tasks").insert(data).execute()
        if hasattr(res, 'data') and res.data:
            d = res.data[0]
            return Task(id=d['id'], titulo=d['titulo'], estado=d['estado'], project_id=d.get('project_id'))
        return task

    def get_tasks(self, user_id: int) -> List[Task]:
        res = self.supabase.table("tasks").select("*").eq("user_id", user_id).execute()
        return [Task(id=d['id'], titulo=d['titulo'], estado=d['estado'], project_id=d.get('project_id')) for d in res.data] if hasattr(res, 'data') else []

    def update_task(self, task: Task, user_id: int) -> Task:
        data = {"titulo": task.titulo, "estado": task.estado, "project_id": task.project_id}
        self.supabase.table("tasks").update(data).eq("id", task.id).eq("user_id", user_id).execute()
        return task

    # --- TSUKUYOMI PHASE 4 (HABITS) ---

    def add_habit(self, habit: Habit, user_id: int) -> Habit:
        data = {"nombre": habit.nombre, "frecuencia": habit.frecuencia, "objective_id": habit.objective_id, "user_id": user_id}
        res = self.supabase.table("habits").insert(data).execute()
        if hasattr(res, 'data') and res.data:
            d = res.data[0]
            return Habit(id=d['id'], nombre=d['nombre'], frecuencia=d['frecuencia'], objective_id=d.get('objective_id'))
        return habit

    def get_habits(self, user_id: int) -> List[Habit]:
        res = self.supabase.table("habits").select("*").eq("user_id", user_id).execute()
        return [Habit(id=d['id'], nombre=d['nombre'], frecuencia=d['frecuencia'], objective_id=d.get('objective_id')) for d in res.data] if hasattr(res, 'data') else []

    def log_habit(self, habit_log: HabitLog, user_id: int) -> HabitLog:
        data = {"habit_id": habit_log.habit_id, "fecha": habit_log.fecha, "estado": habit_log.estado, "user_id": user_id}
        # upsert based on unique constraint (habit_id, fecha)
        res = self.supabase.table("habit_logs").upsert(data, on_conflict="habit_id,fecha").execute()
        if hasattr(res, 'data') and res.data:
            d = res.data[0]
            return HabitLog(id=d['id'], habit_id=d['habit_id'], fecha=d['fecha'], estado=d['estado'])
        return habit_log

    def get_habit_logs(self, user_id: int, fecha: str) -> List[HabitLog]:
        res = self.supabase.table("habit_logs").select("*").eq("user_id", user_id).eq("fecha", fecha).execute()
        return [HabitLog(id=d['id'], habit_id=d['habit_id'], fecha=d['fecha'], estado=d['estado']) for d in res.data] if hasattr(res, 'data') else []

    # --- TSUKUYOMI PHASE 5 (HANSEI) ---
    def add_reflection(self, reflection: Reflection, user_id: int) -> Reflection:
        data = {"tipo": reflection.tipo, "fecha": reflection.fecha, "respuestas": reflection.respuestas, "user_id": user_id}
        res = self.supabase.table("reflections").insert(data).execute()
        if hasattr(res, 'data') and res.data:
            d = res.data[0]
            return Reflection(id=d['id'], tipo=d['tipo'], fecha=d['fecha'], respuestas=d['respuestas'])
        return reflection

    def get_reflections(self, user_id: int, tipo: str = None) -> List[Reflection]:
        query = self.supabase.table("reflections").select("*").eq("user_id", user_id)
        if tipo:
            query = query.eq("tipo", tipo)
        res = query.order("fecha", desc=True).execute()
        return [Reflection(id=d['id'], tipo=d['tipo'], fecha=d['fecha'], respuestas=d['respuestas']) for d in res.data] if hasattr(res, 'data') else []
