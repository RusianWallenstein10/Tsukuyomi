import sqlite3
import pandas as pd
import os

if not os.path.exists('data'):
    os.makedirs('data')

DB_PATH = "data/tsukuyomi.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Mantenemos la estructura para que soporte tus nuevas categorías
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS horarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            actividad TEXT NOT NULL,
            fase TEXT NOT NULL,
            inicio TEXT NOT NULL,
            fin TEXT NOT NULL,
            categoria TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def agregar_actividad(actividad, fase, inicio, fin, categoria):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO horarios (actividad, fase, inicio, fin, categoria) VALUES (?,?,?,?,?)",
                   (actividad, fase, str(inicio), str(fin), categoria))
    conn.commit()
    conn.close()

def obtener_datos():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM horarios", conn)
    conn.close()
    return df

def borrar_dato(id_tarea):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM horarios WHERE id = ?", (id_tarea,))
    conn.commit()
    conn.close()