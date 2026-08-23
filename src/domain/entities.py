from dataclasses import dataclass

@dataclass
class Activity:
    id: int
    actividad: str
    fase: str
    inicio: str
    fin: str
    categoria: str
