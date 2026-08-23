import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import time
import datetime
import base64
from src.application.use_cases import ActivityUseCases
from src.infrastructure.adapters.supabase_repository import SupabaseRepository
from src.infrastructure.services.telegram_service import TelegramNotificationService
from src.infrastructure.services.github_service import GitHubMetricsService

load_dotenv(override=True)

# Configuración inicial
st.set_page_config(page_title="Tsukuyomi Master System", page_icon="🌙", layout="wide")

st.markdown("<h1 style='text-align: center; color: var(--primary-color);'>月読 TSUKUYOMI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Sincronización Multidía de Actividades</p>", unsafe_allow_html=True)

def render_auth_ui(use_cases):
    """Maneja el registro e inicio de sesión con Auth Custom (DIY)."""
    if "user_id" in st.session_state:
        return True

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.info("Santuario sellado. Identifícate para acceder.")
        tab_login, tab_register = st.tabs(["Iniciar Sesión", "Registrarse"])
        
        with tab_login:
            user_login = st.text_input("Usuario", key="login_user")
            pass_login = st.text_input("Contraseña", type="password", key="login_pass")
            if st.button("Entrar", use_container_width=True):
                user_id = use_cases.repository.authenticate_user(user_login, pass_login)
                if user_id:
                    st.session_state["user_id"] = user_id
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas.")
                    
        with tab_register:
            user_reg = st.text_input("Usuario", key="reg_user")
            pass_reg = st.text_input("Contraseña", type="password", key="reg_pass")
            if st.button("Crear Cuenta", use_container_width=True):
                user_id = use_cases.repository.create_user(user_reg, pass_reg)
                if user_id:
                    st.success("Cuenta creada. Ya puedes iniciar sesión.")
                else:
                    st.error("Error al registrar: el usuario ya existe u otro error.")
                    
    return False

def get_use_cases():
    repository = SupabaseRepository(os.getenv("SUPABASE_URL", ""), os.getenv("SUPABASE_KEY", ""))
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
    notifier = TelegramNotificationService(token, chat_id) if token and chat_id else None
    return ActivityUseCases(repository, notifier)

use_cases = get_use_cases()

if not render_auth_ui(use_cases):
    st.stop()

# Usuario actual
current_user_id = st.session_state["user_id"]

# --- SIDEBAR LOGOUT ---
with st.sidebar:
    if st.button("Cerrar Sesión"):
        del st.session_state["user_id"]
        st.rerun()
    st.markdown("---")


# Cargar fondo
bg_base64 = use_cases.repository.get_config("app_background", current_user_id)
if bg_base64:
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bg_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        /* Hacer que el contenido principal sea translúcido oscuro */
        .block-container {{
            background-color: rgba(14, 17, 23, 0.85);
            padding: 2rem;
            border-radius: 15px;
            margin-top: 2rem;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
        }}
        /* Hacer que la barra lateral sea translúcida oscura */
        [data-testid="stSidebar"] {{
            background-color: rgba(14, 17, 23, 0.85) !important;
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
        }}
        /* Header invisible */
        header[data-testid="stHeader"] {{
            background-color: transparent !important;
        }}
        </style>
        """, unsafe_allow_html=True)

with st.sidebar:
    st.header("🎨 Entorno")
    uploaded_bg = st.file_uploader("Cambiar Fondo (JPG/PNG)", type=['png', 'jpg', 'jpeg'])
    if uploaded_bg is not None:
        if st.button("Guardar Fondo"):
            bytes_data = uploaded_bg.getvalue()
            base64_img = base64.b64encode(bytes_data).decode()
            use_cases.repository.save_config("app_background", base64_img, current_user_id)
            st.success("Fondo actualizado!")
            st.rerun()

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
                    use_cases.add_activity(current_user_id, act_nombre, dia, str(horas[0]), str(horas[1]), categoria)
                st.success(f"Ciclo '{act_nombre}' sincronizado en {len(dias_seleccionados)} días.")
                st.rerun()
            else:
                st.error("Por favor, nombra la actividad.")

# --- ACTUALIZAR RITUAL ---
@st.dialog("Editar Ritual")
def edit_activity_dialog(activity):
    st.write(f"Editando: **{activity.actividad}**")
    
    # Nuevos valores
    nuevo_nombre = st.text_input("Nombre", value=activity.actividad)
    nueva_categoria = st.selectbox("Categoría", list(CAT_COLORS.keys()), 
                                   index=list(CAT_COLORS.keys()).index(activity.categoria) if activity.categoria in CAT_COLORS else 0)
    
    col_inicio, col_fin = st.columns(2)
    with col_inicio:
        nueva_h_inicio = st.time_input("Inicio", value=datetime.datetime.strptime(activity.inicio, "%H:%M:%S").time())
    with col_fin:
        nueva_h_fin = st.time_input("Fin", value=datetime.datetime.strptime(activity.fin, "%H:%M:%S").time())
        
    if st.button("Guardar Cambios", type="primary"):
        use_cases.update_activity(
            activity.id,
            current_user_id,
            nuevo_nombre,
            activity.fase,
            nueva_h_inicio.strftime("%H:%M:%S"),
            nueva_h_fin.strftime("%H:%M:%S"),
            nueva_categoria
        )
        st.success("Actualizado")
        st.rerun()

# --- TAB DE GITHUB METRICS ---
def render_github_metrics():
    gh_token = os.getenv("GITHUB_TOKEN")
    if not gh_token:
        st.warning("⚠️ No se ha configurado el token de GitHub.")
        return

    gh_service = GitHubMetricsService(gh_token)
    with st.spinner("Conectando con GitHub..."):
        metrics = gh_service.get_summary_metrics()
        
    if "error" in metrics:
        st.error(f"Error al obtener métricas: {metrics['error']}")
        return

    st.markdown(f"### Perfil: {metrics.get('name', '')} ({metrics.get('username')})")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Repos Públicos", metrics.get("public_repos", 0))
    with col2:
        st.metric("Repos Privados", metrics.get("private_repos", 0))
    with col3:
        st.metric("Seguidores", metrics.get("followers", 0))

    st.markdown("---")
    
    col4, col5 = st.columns(2)
    with col4:
        st.metric("⭐ Total Estrellas", metrics.get("total_stars", 0))
    with col5:
        st.metric("🍴 Total Forks", metrics.get("total_forks", 0))


# --- CUERPO PRINCIPAL: VISUALIZACIÓN ---
dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
tabs = st.tabs(["📅 Calendario Semanal", "🐙 GitHub Hub"])

# Tab de GitHub
with tabs[1]:
    render_github_metrics()

# Tabs de Calendario
activities = use_cases.get_all_activities(current_user_id)
if activities:
    df = pd.DataFrame([{
        "id": a.id,
        "actividad": a.actividad,
        "fase": a.fase,
        "inicio": a.inicio,
        "fin": a.fin,
        "categoria": a.categoria
    } for a in activities])
else:
    df = pd.DataFrame(columns=["id", "actividad", "fase", "inicio", "fin", "categoria"])

with tabs[0]:
    dias_cols = st.columns(7)
    
    for i, col in enumerate(dias_cols):
        with col:
            nombre_dia = dias_semana[i]
            st.markdown(f"<h3 style='text-align: center; font-size: 1.1rem;'>{nombre_dia}</h3>", unsafe_allow_html=True)
            
            if not df.empty:
                tareas = df[df['fase'] == nombre_dia].sort_values("inicio")
                
                if tareas.empty:
                    st.markdown("<p style='color:#555; text-align: center; font-size: 0.8rem;'>Libre</p>", unsafe_allow_html=True)
                else:
                    for _, row in tareas.iterrows():
                        color = CAT_COLORS.get(row['categoria'], "#FFF")
                        
                        # Diseño compacto de la tarjeta
                        with st.container():
                            st.markdown(f"""
                                <div style="border-left: 4px solid {color}; padding-left: 10px; margin-bottom: 5px; background: rgba(0,0,0,0.3); border-radius: 4px; padding-top: 5px; padding-bottom: 5px;">
                                    <span style="color:{color}; font-size:0.7rem; font-weight:bold;">{row['categoria'].upper()}</span><br>
                                    <span style="font-size:0.95rem; color:var(--text-color); line-height: 1.1;"><b>{row['actividad']}</b></span><br>
                                    <span style="color:gray; font-size:0.8rem;">🕒 {row['inicio']} - {row['fin']}</span>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # Botón de engranaje popover
                            with st.popover("⚙️"):
                                if st.button("✏️ Editar", key=f"edit_{row['id']}", use_container_width=True):
                                    act_obj = Activity(row['id'], row['actividad'], row['fase'], row['inicio'], row['fin'], row['categoria'])
                                    edit_activity_dialog(act_obj)
                                if st.button("🗑️ Borrar", key=f"del_{row['id']}", use_container_width=True):
                                    use_cases.delete_activity(row['id'], current_user_id)
                                    st.rerun()
            else:
                if i == 3: # Mostrar mensaje solo en el medio (Jueves)
                    st.markdown("<p style='text-align: center; color: gray;'>El Santuario está vacío.</p>", unsafe_allow_html=True)

# Gráfico de carga de tiempo (Opcional)
if not df.empty:
    with st.expander("📊 Ver Balance de Energías (Distribución de Tareas)"):
        stats = df['categoria'].value_counts()
        st.bar_chart(stats)