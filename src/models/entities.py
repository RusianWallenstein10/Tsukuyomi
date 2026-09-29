from dataclasses import dataclass
from typing import Optional


@dataclass
class Area:
    id: int
    nombre: str
    vision: Optional[str]


@dataclass
class Objective:
    id: int
    titulo: str
    area_id: Optional[int]
    estado: str


@dataclass
class Project:
    id: int
    nombre: str
    objective_id: Optional[int]
    estado: str


@dataclass
class Task:
    id: int
    titulo: str
    project_id: Optional[int]
    estado: str


@dataclass
class Habit:
    id: int
    nombre: str
    objective_id: Optional[int]
    frecuencia: str


@dataclass
class HabitLog:
    id: int
    habit_id: int
    fecha: str
    estado: bool


@dataclass
class Activity:
    id: int
    actividad: str
    fase: str
    inicio: str
    fin: str
    categoria: str
    task_id: Optional[int] = None
    habit_id: Optional[int] = None


@dataclass
class Reflection:
    id: int
    tipo: str
    fecha: str
    respuestas: dict
