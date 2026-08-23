import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import time
from src.application.use_cases import ActivityUseCases
from src.infrastructure.adapters.supabase_repository import SupabaseRepository
from src.infrastructure.services.telegram_service import TelegramNotificationService

load_dotenv()

# Configuración inicial
st.set_page_config(page_title="Tsukuyomi Master System", page_icon="🌙", layout="wide")

st.markdown("<h1 style='text-align: center; color: var(--primary-color);'>月読 TSUKUYOMI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Sincronización Multidía de Actividades</p>", unsafe_allow_html=True)

def check_password():
    """Valida la contraseña maestra antes de mostrar el contenido."""
    app_password = os.getenv("APP_PASSWORD")
    if not app_password:
        return True # Si no hay contraseña configurada, deja pasar (útil para desarrollo local rápido)
        
    def password_entered():
        if st.session_state["password"] == app_password:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Por seguridad, borramos la contraseña del estado
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    # Muestra el formulario si no está autenticado
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.info("Santuario sellado. Ingresa la llave para acceder.")
        st.text_input("Contraseña de Acceso", type="password", on_change=password_entered, key="password")
        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.error("😕 Llave incorrecta")
    return False

# Si la contraseña es incorrecta o no se ha introducido, detenemos la ejecución de la app aquí
if not check_password():
    st.stop()

@st.cache_resource
def get_use_cases():
    repository = SupabaseRepository(os.getenv("SUPABASE_URL", ""), os.getenv("SUPABASE_KEY", ""))
    
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
    notifier = TelegramNotificationService(token, chat_id) if token and chat_id else None
    
    return ActivityUseCases(repository, notifier)

use_cases = get_use_cases()

CAT_COLORS = {
    "Asignatura Universidad": "#4A90E2",
    "Tarea": "#9B59B6",
    "Espacio Libre": "#BDC3C7",
    "Deporte": "#E67E22",
    "Producción": "#2ECC71"
}

# --- SIDEBAR: CREADOR MULTIDÍA ---
st.sidebar.markdown("### 🌑 Programación Maestra")

with st.sidebar:
    act_nombre = st.text_input("Nombre de la Actividad")
    categoria = st.selectbox("Categoría", list(CAT_COLORS.keys()))
    
    # Selección de múltiples días
    dias_seleccionados = st.multiselect(
        "Selecciona los días para esta actividad",
        ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    )

    # Diccionario para guardar los horarios de cada día
    horarios_config = {}

    if dias_seleccionados:
        st.markdown("---")
        st.markdown("#### 🕒 Definir Horarios")
        for d in dias_seleccionados:
            st.write(f"**{d}:**")
            c1, c2 = st.columns(2)
            h_ini = c1.time_input(f"Inicio ({d})", time(8, 0), key=f"ini_{d}")
            h_fin = c2.time_input(f"Fin ({d})", time(9, 0), key=f"fin_{d}")
            horarios_config[d] = (h_ini, h_fin)
        
        st.markdown("---")
        if st.button("🌙 Sincronizar Calendario"):
            if act_nombre:
                for dia, horas in horarios_config.items():
                    use_cases.add_activity(act_nombre, dia, str(horas[0]), str(horas[1]), categoria)
                st.success(f"Ciclo '{act_nombre}' sincronizado en {len(dias_seleccionados)} días.")
                st.rerun()
            else:
                st.error("Por favor, nombra la actividad.")

# --- CUERPO PRINCIPAL: VISUALIZACIÓN ---
dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
tabs = st.tabs([f"🏮 {d}" for d in dias_semana])

activities = use_cases.get_all_activities()
if activities:
    df = pd.DataFrame([vars(a) for a in activities])
else:
    df = pd.DataFrame(columns=["id", "actividad", "fase", "inicio", "fin", "categoria"])

for i, tab in enumerate(tabs):
    with tab:
        nombre_dia = dias_semana[i]
        if not df.empty:
            # Filtrar y ordenar por hora de inicio
            tareas = df[df['fase'] == nombre_dia].sort_values("inicio")
            
            if tareas.empty:
                st.write(f"<p style='color:#555;'>No hay rituales programados para el {nombre_dia}.</p>", unsafe_allow_html=True)
            else:
                for _, row in tareas.iterrows():
                    color = CAT_COLORS.get(row['categoria'], "#FFF")
                    
                    # Diseño de la tarjeta de actividad
                    with st.container():
                        c_marca, c_info, c_del = st.columns([0.05, 0.80, 0.15])
                        
                        # Línea de color lateral
                        c_marca.markdown(f"<div style='background-color:{color}; height:60px; width:5px; border-radius:5px;'></div>", unsafe_allow_html=True)
                        
                        with c_info:
                            st.markdown(f"""
                                <div style="margin-bottom: 15px;">
                                    <span style="color:{color}; font-size:0.75rem; font-weight:bold; letter-spacing:1px;">{row['categoria'].upper()}</span><br>
                                    <span style="font-size:1.1rem; color:var(--text-color);"><b>{row['actividad']}</b></span><br>
                                    <span style="color:gray; font-size:0.9rem;">🕒 {row['inicio']} - {row['fin']}</span>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        with c_del:
                            if st.button("🗑️", key=f"del_{row['id']}"):
                                use_cases.delete_activity(row['id'])
                                st.rerun()
        else:
            st.write("El Santuario está vacío.")

# Gráfico de carga de tiempo (Opcional)
if not df.empty:
    with st.expander("📊 Ver Balance de Energías (Distribución de Tareas)"):
        stats = df['categoria'].value_counts()
        st.bar_chart(stats)