import streamlit as st
import datetime
import base64

DAYS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
CAT_COLORS = {
    "Asignatura Universidad": "#3b82f6",
    "Tarea": "#8b5cf6",
    "Espacio Libre": "#6b7280",
    "Deporte": "#f97316",
    "Producción": "#10b981"
}

import os

import os
from PIL import Image
import io

def get_default_bg_b64():
    try:
        if os.path.exists("assets/default_bg.jpg"):
            with open("assets/default_bg.jpg", "rb") as f:
                return base64.b64encode(f.read()).decode()
    except Exception:
        pass
    return None

@st.cache_data(show_spinner=False)
def get_cached_theme_css_v4(b64_str):
    try:
        img_bytes = base64.b64decode(b64_str)
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img = img.resize((1, 1))
        r, g, b = img.getpixel((0, 0))
        luminance = (0.299 * r + 0.587 * g + 0.114 * b)
        
        if luminance > 128:
            text_color = "#09090b"
            overlay = "rgba(255, 255, 255, 0.15)"
            card_bg = "rgba(255, 255, 255, 0.15)"
            border = "rgba(255, 255, 255, 0.4)"
            accent = f"rgb({max(0,r-100)}, {max(0,g-100)}, {max(0,b-100)})"
            glow = f"rgba({max(0,r-100)}, {max(0,g-100)}, {max(0,b-100)}, 0.4)"
        else:
            text_color = "#ffffff"
            overlay = "rgba(9, 9, 11, 0.15)"
            card_bg = "rgba(24, 24, 27, 0.20)"
            border = "rgba(255, 255, 255, 0.10)"
            accent = f"rgb({min(255,r+100)}, {min(255,g+100)}, {min(255,b+100)})"
            glow = f"rgba({min(255,r+100)}, {min(255,g+100)}, {min(255,b+100)}, 0.4)"
            
        return f"""
        <style>
        :root {{
            --dyn-text: {text_color};
            --dyn-overlay: {overlay};
            --dyn-card: {card_bg};
            --dyn-border: {border};
            --dyn-accent: {accent};
            --dyn-glow: {glow};
        }}
        
        /* Global Background */
        body, .stApp, [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/jpeg;base64,{b64_str}") !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
        }}
        
        body::before, .stApp::before, [data-testid="stAppViewContainer"]::before {{
            content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: var(--dyn-overlay); z-index: -1;
        }}
        
        /* Typography */
        .stApp, .stMarkdown p, .stMarkdown span, h1, h2, h3, h4, h5, h6, label p, label span, .stMetric label {{
            color: var(--dyn-text) !important;
            text-shadow: 0 1px 3px rgba(0,0,0,0.2);
        }}
        
        /* Sidebar Glassmorphism Fix for Newer Streamlit */
        [data-testid="stSidebar"] {{
            background-color: transparent !important;
        }}
        [data-testid="stSidebar"] > div:first-child, [data-testid="stSidebarContent"] {{
            background-color: var(--dyn-card) !important;
            backdrop-filter: blur(5px) !important;
            -webkit-backdrop-filter: blur(5px) !important;
            border-right: 1px solid var(--dyn-border) !important;
        }}
        [data-testid="stSidebarHeader"] {{
            background-color: transparent !important;
        }}

        /* Glassmorphism Cards & Metrics */
        .activity-card, 
        div[data-testid="stExpander"], 
        div[data-testid="stForm"], 
        [data-testid="stMetric"], 
        [data-testid="stVerticalBlockBorderWrapper"],
        div[data-testid="stVerticalBlock"] > div[style*="border"] {{
            background: var(--dyn-card) !important;
            backdrop-filter: blur(5px) !important;
            -webkit-backdrop-filter: blur(5px) !important;
            border: 1px solid var(--dyn-border) !important;
            border-radius: 12px !important;
        }}
        
        /* Add padding specifically to metrics so they look like cards */
        [data-testid="stMetric"] {{
            padding: 15px !important;
        }}
        
        /* Sidebar Radio Navigation Upgrade */
        section[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label {
            padding: 12px 16px;
            border-radius: 12px;
            margin-bottom: 6px;
            background-color: transparent;
            border: 1px solid transparent;
            transition: all 0.2s ease;
            cursor: pointer;
        }
        section[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label:hover {
            background-color: var(--dyn-border);
            transform: translateX(4px);
        }
        
        /* HIDE DEFAULT RADIO CIRCLES - Bulletproof for all versions */
        section[data-testid="stSidebar"] .stRadio div[role="radio"] { display: none !important; }
        section[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child { display: none !important; }
        section[data-testid="stSidebar"] .stRadio label > div:first-child { display: none !important; }
        section[data-testid="stSidebar"] .stRadio svg { display: none !important; }
        section[data-testid="stSidebar"] .stRadio input[type="radio"] { display: none !important; }
        section[data-testid="stSidebar"] .stRadio .st-c* { display: none !important; }
        /* Target the specific circle in new Streamlit versions */
        section[data-testid="stSidebar"] .stRadio label span:first-child { display: none !important; }
        /* Make navigation text bold */
        section[data-testid="stSidebar"] .stRadio p,
        section[data-testid="stSidebar"] .stRadio span {{
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            margin: 0 !important;
        }}
        
        /* Buttons and Inputs */
        button[kind="primary"] {{
            background: var(--dyn-accent) !important;
            border-color: var(--dyn-accent) !important;
            box-shadow: 0 4px 15px var(--dyn-glow) !important;
            color: #ffffff !important;
        }}
        
        div[data-baseweb="input"] > div, div[data-baseweb="select"] > div, textarea, section[data-testid="stSidebar"] button[kind="secondary"] {{
            background-color: var(--dyn-card) !important;
            color: var(--dyn-text) !important;
            border-color: var(--dyn-border) !important;
        }}
        
        div[data-testid="stFileUploader"] {{
            background-color: transparent !important;
        }}
        </style>
        """
    except Exception as e:
        return ""

def apply_dynamic_theme(b64_str):
    if not b64_str:
        # Tema fallback (Dark Red Moon) si falta la imagen (ej: login)
        fallback_css = """
        <style>
        :root {
            --dyn-text: #ffffff;
            --dyn-overlay: transparent;
            --dyn-card: rgba(40, 10, 10, 0.7);
            --dyn-border: rgba(220, 38, 38, 0.8);
            --dyn-accent: #ff3333;
            --dyn-glow: rgba(255, 50, 50, 0.6);
        }
        
        body, .stApp, [data-testid="stAppViewContainer"] {
            background-color: #050000 !important;
            background-image: 
                radial-gradient(circle at 50% 20%, rgba(220, 20, 20, 0.4) 0%, transparent 40%), 
                radial-gradient(circle at 50% 100%, rgba(139, 0, 0, 0.3) 0%, transparent 60%) !important;
            background-size: cover !important;
        }

        .activity-card, div[data-testid="stExpander"], div[data-testid="stForm"], [data-testid="stMetric"], [data-testid="stVerticalBlockBorderWrapper"], div[data-testid="stVerticalBlock"] > div[style*="border"] {
            background: var(--dyn-card) !important;
            backdrop-filter: blur(15px) !important;
            -webkit-backdrop-filter: blur(15px) !important;
            border: 1px solid var(--dyn-border) !important;
            border-radius: 16px !important;
            box-shadow: 0 0 30px rgba(220, 38, 38, 0.4), inset 0 0 20px rgba(220, 38, 38, 0.1) !important;
        }
        div[data-baseweb="input"] > div {
            background-color: rgba(0,0,0,0.6) !important;
            border: 1px solid rgba(220,38,38,0.5) !important;
        }
        div[data-baseweb="input"] > div:focus-within {
            border-color: #ff3333 !important;
            box-shadow: 0 0 15px rgba(255, 50, 50, 0.5) !important;
        }
        button[kind="primary"] {
            background: linear-gradient(135deg, #dc2626 0%, #7f1d1d 100%) !important;
            border: 1px solid #ff6666 !important;
            box-shadow: 0 4px 20px rgba(220, 38, 38, 0.6) !important;
            color: white !important;
            font-weight: bold !important;
            letter-spacing: 2px !important;
        }
        button[kind="primary"]:hover {
            box-shadow: 0 4px 30px rgba(255, 50, 50, 0.8) !important;
            transform: translateY(-2px);
        }
        /* Make tabs look good too */
        button[data-baseweb="tab"] {
            color: #d4d4d8 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #ff3333 !important;
            border-bottom: 2px solid #ff3333 !important;
        }
        </style>
"""
        st.markdown(fallback_css, unsafe_allow_html=True)
        return
        
    css = get_cached_theme_css_v4(b64_str)
    if css:
        st.markdown(css, unsafe_allow_html=True)

def login_register_view(repo):
    apply_dynamic_theme(get_default_bg_b64())
    
    st.markdown("""
        <div style='text-align: center; margin-top: 5vh; margin-bottom: 2rem;'>
            <h1 style='font-size: 4.5rem; text-shadow: 0 0 25px rgba(220, 38, 38, 0.8), 0 0 50px rgba(220, 38, 38, 0.4); color: white; letter-spacing: 0.1em; margin-bottom: 0;'>
                🩸 TSUKUYOMI
            </h1>
            <p style='color: #d4d4d8; font-size: 1.2rem; letter-spacing: 0.4em; text-transform: uppercase; text-shadow: 0 0 10px rgba(255,255,255,0.3);'>
                M I N D   R E A L M
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.container(border=True):
            tab1, tab2 = st.tabs(["👁️ Despertar", "⛩️ Forjar Alma"])
            with tab1:
                l_user = st.text_input("Usuario", key="l_user")
                l_pass = st.text_input("Contraseña", type="password", key="l_pass")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Entrar al Reino", use_container_width=True, type="primary"):
                    try:
                        uid = repo.authenticate_user(l_user, l_pass)
                        if uid:
                            st.session_state.user_id = uid
                            st.rerun()
                        else:
                            st.error("Credenciales inválidas o el usuario no existe.")
                    except Exception as e:
                        st.error(f"Error: {e}")
            with tab2:
                r_user = st.text_input("Usuario", key="r_user")
                r_pass = st.text_input("Contraseña", type="password", key="r_pass")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Crear Vínculo", use_container_width=True, type="primary"):
                    try:
                        uid = repo.create_user(r_user, r_pass)
                        if uid:
                            st.success("Alma forjada exitosamente. Por favor, despierta (inicia sesión).")
                    except Exception as e:
                        st.error(f"Error: {e}")

def view_dashboard(use_cases):
    st.header("🌌 Dashboard de Alineación")
    
    # 1. METRICA DE ALINEACIÓN
    acts = use_cases.get_all_activities(st.session_state.user_id)
    total_acts = len(acts)
    aligned_acts = sum(1 for a in acts if a.task_id is not None or getattr(a, 'habit_id', None) is not None)
    
    perc = (aligned_acts / total_acts * 100) if total_acts > 0 else 0
    
    col_met1, col_met2, col_met3 = st.columns(3)
    with col_met1:
        st.metric(label="Alineación Vital", value=f"{perc:.1f}%", delta="🎯 Óptimo" if perc > 70 else "⚠️ Requiere Foco")
    with col_met2:
        st.metric(label="Bloques Temporales", value=total_acts)
    with col_met3:
        st.metric(label="Bloques Alineados", value=aligned_acts)
        
    st.progress(perc / 100.0, text="Progreso general de alineación de actividades semanales a tus objetivos/hábitos")
    st.divider()
    
    col1, col2 = st.columns(2)
    
    # 2. PROYECTOS WIP
    with col1:
        st.subheader("🔥 Proyectos en Foco (WIP)")
        projects = use_cases.get_projects(st.session_state.user_id)
        wip_projs = [p for p in projects if p.estado == "En progreso"]
        
        if not wip_projs:
            st.info("No tienes proyectos en progreso en este momento.")
        else:
            tasks = use_cases.get_tasks(st.session_state.user_id)
            for p in wip_projs:
                with st.container(border=True):
                    st.markdown(f"**{p.nombre}**")
                    p_tasks = [t for t in tasks if t.project_id == p.id]
                    completed = sum(1 for t in p_tasks if t.estado == "Completada")
                    total = len(p_tasks)
                    if total > 0:
                        st.progress(completed / total, text=f"Progreso: {completed}/{total} tareas")
                    else:
                        st.caption("Sin tareas")

    # 3. HÁBITOS DE HOY
    with col2:
        st.subheader("🔁 Check-in de Hoy")
        habits = use_cases.get_habits(st.session_state.user_id)
        today_str = datetime.date.today().isoformat()
        logs_today = use_cases.get_habit_logs(st.session_state.user_id, today_str)
        
        if not habits:
            st.info("No tienes hábitos registrados.")
        else:
            with st.container(border=True):
                for h in habits:
                    log = next((l for l in logs_today if l.habit_id == h.id), None)
                    current_state = log.estado if log else False
                    new_state = st.checkbox(h.nombre, value=current_state, key=f"dash_hab_{h.id}")
                    if new_state != current_state:
                        use_cases.log_habit(st.session_state.user_id, h.id, today_str, new_state)
                        st.rerun()

def view_vision(use_cases):
    st.header("🎯 Visión y Objetivos (Ikigai)")
    
    # Crear nueva área
    with st.expander("➕ Añadir Nueva Área de Vida"):
        with st.form("area_form"):
            a_nombre = st.text_input("Nombre del Área (Ej. Universidad, Salud)")
            a_vision = st.text_area("Visión (¿Qué quieres lograr aquí a largo plazo?)")
            if st.form_submit_button("Crear Área"):
                use_cases.add_area(st.session_state.user_id, a_nombre, a_vision)
                st.rerun()

    areas = use_cases.get_areas(st.session_state.user_id)
    objectives = use_cases.get_objectives(st.session_state.user_id)

    if not areas:
        st.info("No tienes áreas definidas. Empieza por crear una.")
        return

    for area in areas:
        st.markdown(f"### 🏔️ {area.nombre}")
        if area.vision:
            st.caption(f"_{area.vision}_")
        
        # Objetivos de esta área
        area_objs = [o for o in objectives if o.area_id == area.id]
        if area_objs:
            for obj in area_objs:
                st.markdown(f"- **{obj.titulo}** ({obj.estado})")
        else:
            st.markdown("- _Sin objetivos._")

        with st.popover(f"Añadir objetivo a {area.nombre}"):
            obj_titulo = st.text_input("Título del objetivo", key=f"obj_{area.id}")
            if st.button("Guardar", key=f"btn_obj_{area.id}"):
                use_cases.add_objective(st.session_state.user_id, obj_titulo, area.id)
                st.rerun()
        st.markdown("---")

def view_kanban(use_cases):
    st.header("📋 Tablero Kanban (Proyectos y Tareas)")
    objectives = use_cases.get_objectives(st.session_state.user_id)
    projects = use_cases.get_projects(st.session_state.user_id)
    tasks = use_cases.get_tasks(st.session_state.user_id)

    with st.expander("➕ Nuevo Proyecto"):
        with st.form("proj_form"):
            p_nombre = st.text_input("Nombre del Proyecto")
            p_obj = st.selectbox("Objetivo Relacionado", ["Ninguno"] + [o.titulo for o in objectives])
            if st.form_submit_button("Crear Proyecto"):
                obj_id = next((o.id for o in objectives if o.titulo == p_obj), None)
                use_cases.add_project(st.session_state.user_id, p_nombre, obj_id)
                st.rerun()

    estados = ["Backlog", "Pendiente", "En progreso", "Completado"]
    cols = st.columns(4)

    for i, est in enumerate(estados):
        with cols[i]:
            st.markdown(f"**{est}**")
            st.markdown('<div class="kanban-column">', unsafe_allow_html=True)
            est_projs = [p for p in projects if p.estado == est]
            
            for p in est_projs:
                with st.container(border=True):
                    st.markdown(f"**{p.nombre}**")
                    p_tasks = [t for t in tasks if t.project_id == p.id]
                    completed = sum(1 for t in p_tasks if t.estado == "Completada")
                    total = len(p_tasks)
                    if total > 0:
                        st.progress(completed / total, text=f"Tareas: {completed}/{total}")
                    
                    # Tareas
                    with st.popover("Ver Tareas"):
                        for t in p_tasks:
                            nuevo_est = st.checkbox(t.titulo, value=(t.estado=="Completada"), key=f"t_{t.id}")
                            estado_esperado = "Completada" if nuevo_est else "Pendiente"
                            if estado_esperado != t.estado:
                                use_cases.update_task_status(t.id, st.session_state.user_id, estado_esperado)
                                st.rerun()
                                
                        new_t = st.text_input("Nueva tarea", key=f"nt_{p.id}")
                        if st.button("Añadir", key=f"bt_{p.id}") and new_t:
                            use_cases.add_task(st.session_state.user_id, new_t, p.id)
                            st.rerun()

                    # Mover Proyecto
                    new_est = st.selectbox("Mover a", estados, index=estados.index(p.estado), key=f"mv_{p.id}")
                    if new_est != p.estado:
                        try:
                            use_cases.update_project_status(p.id, st.session_state.user_id, new_est)
                            st.rerun()
                        except ValueError as e:
                            st.error(str(e))
                            
            st.markdown('</div>', unsafe_allow_html=True)


def view_habits(use_cases):
    st.header("🔁 Hábitos (Shūkan)")
    objectives = use_cases.get_objectives(st.session_state.user_id)
    habits = use_cases.get_habits(st.session_state.user_id)
    today_str = datetime.date.today().isoformat()
    logs_today = use_cases.get_habit_logs(st.session_state.user_id, today_str)

    with st.expander("➕ Nuevo Hábito"):
        with st.form("habit_form"):
            h_nombre = st.text_input("Nombre del Hábito (Ej. Meditar 10 min)")
            h_obj = st.selectbox("Objetivo Relacionado", ["Ninguno"] + [o.titulo for o in objectives])
            if st.form_submit_button("Crear Hábito"):
                obj_id = next((o.id for o in objectives if o.titulo == h_obj), None)
                use_cases.add_habit(st.session_state.user_id, h_nombre, obj_id)
                st.rerun()

    if not habits:
        st.info("No tienes hábitos registrados.")
        return

    st.subheader(f"Check-ins para Hoy ({today_str})")
    for h in habits:
        log = next((l for l in logs_today if l.habit_id == h.id), None)
        current_state = log.estado if log else False
        new_state = st.checkbox(h.nombre, value=current_state, key=f"hab_{h.id}")
        if new_state != current_state:
            use_cases.log_habit(st.session_state.user_id, h.id, today_str, new_state)
            st.rerun()

def view_hansei(use_cases):
    st.header("🧘‍♂️ Hansei (Reflexión)")
    
    tabs = st.tabs(["Diaria", "Semanal", "Mensual", "Historial"])
    today_str = datetime.date.today().isoformat()
    
    with tabs[0]:
        st.subheader("Revisión Diaria")
        with st.form("diaria_form"):
            q1 = st.text_area("¿Qué hice hoy?")
            q2 = st.text_input("¿Qué conseguí?")
            q3 = st.text_area("¿Qué no hice?")
            q4 = st.text_input("¿Por qué no lo hice?")
            q5 = st.text_input("¿Qué salió bien?")
            q6 = st.text_input("¿Qué salió mal?")
            q7 = st.text_input("¿Qué aprendí?")
            q8 = st.text_input("¿Qué debo cambiar mañana?")
            if st.form_submit_button("Guardar Reflexión Diaria"):
                resp = {"Que hice hoy": q1, "Que consegui": q2, "Que no hice": q3, "Por que no lo hice": q4, "Salio bien": q5, "Salio mal": q6, "Aprendi": q7, "Cambiar manana": q8}
                use_cases.add_reflection(st.session_state.user_id, "Diaria", today_str, resp)
                st.success("Reflexión Diaria guardada.")
                
    with tabs[1]:
        st.subheader("Revisión Semanal")
        with st.form("semanal_form"):
            s1 = st.text_area("¿Qué objetivos avancé?")
            s2 = st.text_area("¿Qué proyectos avanzaron?")
            s3 = st.text_input("¿Qué quedó pendiente?")
            s4 = st.text_input("¿Dónde desperdicié tiempo?")
            s5 = st.text_input("¿Qué problemas se repitieron?")
            s6 = st.text_input("¿Qué debería eliminar?")
            s7 = st.text_input("¿Qué debería mantener?")
            s8 = st.text_input("¿Qué debería mejorar la próxima semana?")
            if st.form_submit_button("Guardar Reflexión Semanal"):
                resp = {"Objetivos avance": s1, "Proyectos avance": s2, "Pendiente": s3, "Desperdicie tiempo": s4, "Problemas repetidos": s5, "Eliminar": s6, "Mantener": s7, "Mejorar prox semana": s8}
                use_cases.add_reflection(st.session_state.user_id, "Semanal", today_str, resp)
                st.success("Reflexión Semanal guardada.")
                
    with tabs[2]:
        st.subheader("Revisión Mensual")
        with st.form("mensual_form"):
            m1 = st.text_area("¿Qué progreso real conseguí?")
            m2 = st.text_area("¿Qué objetivos siguen siendo importantes?")
            m3 = st.text_input("¿Qué objetivos ya no tienen sentido?")
            m4 = st.text_input("¿Qué proyectos debo continuar?")
            m5 = st.text_input("¿Qué proyectos debo abandonar?")
            m6 = st.text_input("¿Qué hábitos están funcionando?")
            m7 = st.text_input("¿Qué debería cambiar el próximo mes?")
            if st.form_submit_button("Guardar Reflexión Mensual"):
                resp = {"Progreso real": m1, "Importantes": m2, "No tienen sentido": m3, "Continuar": m4, "Abandonar": m5, "Habitos funcionan": m6, "Cambiar prox mes": m7}
                use_cases.add_reflection(st.session_state.user_id, "Mensual", today_str, resp)
                st.success("Reflexión Mensual guardada.")
                
    with tabs[3]:
        st.subheader("Historial de Reflexiones")
        refs = use_cases.get_reflections(st.session_state.user_id)
        if not refs:
            st.info("No hay reflexiones pasadas.")
        for r in refs:
            with st.expander(f"{r.fecha} - {r.tipo}"):
                for k, v in r.respuestas.items():
                    if v:
                        st.markdown(f"**{k}:** {v}")

def view_calendar(use_cases):
    st.header("📅 Calendario Semanal (Time Management)")
    
    with st.sidebar:
        st.header("🌑 Sincronizar Tiempo")
        tasks = [t for t in use_cases.get_tasks(st.session_state.user_id) if t.estado == "Pendiente"]
        habits = use_cases.get_habits(st.session_state.user_id)
        with st.form("activity_form"):
            act_nombre = st.text_input("Nombre de la Actividad")
            tarea_vinculada = st.selectbox("Vincular Tarea (Opcional)", ["Ninguna"] + [t.titulo for t in tasks])
            habito_vinculado = st.selectbox("Vincular Hábito (Opcional)", ["Ninguno"] + [h.nombre for h in habits])
            categoria = st.selectbox("Categoría", list(CAT_COLORS.keys()))
            
            selected_days = st.multiselect("Selecciona los días", DAYS)
            
            horarios = {}
            for day in selected_days:
                col_h1, col_h2 = st.columns(2)
                with col_h1:
                    inicio = st.time_input(f"Inicio ({day})")
                with col_h2:
                    fin = st.time_input(f"Fin ({day})")
                horarios[day] = {"inicio": inicio.strftime("%H:%M"), "fin": fin.strftime("%H:%M")}
                
            if st.form_submit_button("Sincronizar", use_container_width=True):
                if not act_nombre and tarea_vinculada == "Ninguna" and habito_vinculado == "Ninguno":
                    st.warning("Debes dar un nombre, o seleccionar una tarea, o seleccionar un hábito.")
                elif not selected_days:
                    st.warning("Selecciona al menos un día.")
                else:
                    t_id = next((t.id for t in tasks if t.titulo == tarea_vinculada), None)
                    h_id = next((h.id for h in habits if h.nombre == habito_vinculado), None)
                    
                    nombre_final = act_nombre
                    if not nombre_final:
                        if tarea_vinculada != "Ninguna": nombre_final = tarea_vinculada
                        elif habito_vinculado != "Ninguno": nombre_final = habito_vinculado

                    for day in selected_days:
                        use_cases.add_activity(
                            user_id=st.session_state.user_id,
                            actividad=nombre_final,
                            fase=day,
                            inicio=horarios[day]["inicio"] + ":00",
                            fin=horarios[day]["fin"] + ":00",
                            categoria=categoria,
                            task_id=t_id,
                            habit_id=h_id
                        )
                    st.success("Sincronizado")
                    st.rerun()
                    
    acts = use_cases.get_all_activities(st.session_state.user_id)
    cols = st.columns(7)
    for i, day in enumerate(DAYS):
        with cols[i]:
            st.markdown(f"**{day}**")
            day_acts = sorted([a for a in acts if a.fase == day], key=lambda x: x.inicio)
            if not day_acts:
                st.caption("Libre")
            for act in day_acts:
                color = CAT_COLORS.get(act.categoria, "#fff")
                alineado_tarea = "🎯" if act.task_id else ""
                alineado_habito = "🔁" if getattr(act, 'habit_id', None) else ""
                alineado = alineado_tarea + alineado_habito
                html = f'''
                <div class="activity-card" style="border-left: 4px solid {color}; padding: 12px; margin-bottom: 12px; cursor: pointer;">
                    <div style="color: {color}; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">
                        {act.categoria} {alineado}
                    </div>
                    <div style="font-weight: 600; font-size: 1.05rem; margin-bottom: 6px; color: #f4f4f5;">
                        {act.actividad}
                    </div>
                    <div style="color: #a1a1aa; font-size: 0.85rem; display: flex; align-items: center; gap: 6px;">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                        {act.inicio[:5]} - {act.fin[:5]}
                    </div>
                </div>
                '''
                st.markdown(html, unsafe_allow_html=True)
                if st.button("✖", key=f"del_{act.id}", help="Eliminar actividad"):
                    use_cases.delete_activity(act.id, st.session_state.user_id)
                    st.rerun()


def view_notes(use_cases):
    st.header("📝 Pizarrón de Notas")
    
    # Inyectar CSS exclusivo para las notas adhesivas
    st.markdown("""
    <style>
    .sticky-note {
        padding: 25px 20px 20px 20px;
        box-shadow: 4px 8px 20px rgba(0,0,0,0.5);
        margin-bottom: 15px;
        min-height: 180px;
        position: relative;
        font-family: 'Outfit', sans-serif;
        border-radius: 2px 15px 15px 15px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        backdrop-filter: blur(0px) !important;
        -webkit-backdrop-filter: blur(0px) !important;
    }
    .sticky-note:hover {
        transform: scale(1.05) rotate(0deg) !important;
        box-shadow: 6px 12px 25px rgba(0,0,0,0.6);
        z-index: 10;
    }
    /* El trozo de cinta adhesiva arriba */
    .sticky-note::before {
        content: "";
        position: absolute;
        top: -8px; left: 50%;
        transform: translateX(-50%) rotate(-2deg);
        width: 60px; height: 20px;
        background-color: rgba(255, 255, 255, 0.5);
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        border-radius: 2px;
    }
    /* Estilos y colores de las notas */
    .note-yellow { background: linear-gradient(135deg, #fef08a 0%, #fde047 100%); transform: rotate(-2deg); }
    .note-mint { background: linear-gradient(135deg, #a7f3d0 0%, #6ee7b7 100%); transform: rotate(1.5deg); }
    .note-pink { background: linear-gradient(135deg, #fbcfe8 0%, #f9a8d4 100%); transform: rotate(-1deg); }
    .note-blue { background: linear-gradient(135deg, #bfdbfe 0%, #93c5fd 100%); transform: rotate(2deg); }
    
    .sticky-note p { 
        color: #1f2937 !important; 
        text-shadow: none !important; 
        font-size: 1.15rem !important; 
        font-weight: 600 !important;
        line-height: 1.4;
    }
    </style>
    """, unsafe_allow_html=True)
    
    import json
    raw_notes = use_cases.repository.get_config("sticky_notes", st.session_state.user_id)
    try:
        notes_list = json.loads(raw_notes) if raw_notes else []
    except:
        notes_list = []
        
    with st.expander("➕ Escribir nueva nota"):
        with st.form("note_form"):
            new_text = st.text_area("Contenido de la nota...", height=100)
            color_choice = st.selectbox("Color del Post-it", ["Amarillo", "Menta", "Rosa", "Azul"])
            if st.form_submit_button("Pegar en el Pizarrón", type="primary"):
                if new_text.strip():
                    color_class = {"Amarillo": "note-yellow", "Menta": "note-mint", "Rosa": "note-pink", "Azul": "note-blue"}[color_choice]
                    notes_list.append({"text": new_text, "color": color_class})
                    use_cases.repository.save_config("sticky_notes", json.dumps(notes_list), st.session_state.user_id)
                    st.rerun()
                    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if not notes_list:
        st.info("No hay notas pegadas en el pizarrón aún.")
    else:
        cols = st.columns(4)
        for i, note in enumerate(notes_list):
            with cols[i % 4]:
                st.markdown(f"""
                <div class="sticky-note {note['color']}">
                    <p>{note['text'].replace(chr(10), '<br>')}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🗑️ Despegar", key=f"del_note_{i}", help="Eliminar esta nota"):
                    notes_list.pop(i)
                    use_cases.repository.save_config("sticky_notes", json.dumps(notes_list), st.session_state.user_id)
                    st.rerun()


def view_sports(use_cases):
    st.header("💪 Rutinas de Entrenamiento")
    
    # CSS para la vista de deporte
    st.markdown("""
    <style>
    .routine-card {
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        border-left: 6px solid var(--dyn-accent);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .routine-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    /* Alinear textos verticalmente en la lista de ejercicios */
    .exercise-text {
        display: flex;
        align-items: center;
        height: 100%;
        margin: 0;
        padding-top: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    import json
    raw_sports = use_cases.repository.get_config("workout_routines", st.session_state.user_id)
    try:
        data = json.loads(raw_sports) if raw_sports else {"rutinas": []}
    except:
        data = {"rutinas": []}
        
    rutinas = data.get("rutinas", [])
    
    # Crear nueva rutina
    with st.expander("➕ Crear Nueva Rutina"):
        with st.form("new_routine_form"):
            r_name = st.text_input("Nombre de la rutina (ej. Día de Pecho y Tríceps, Pierna, Full Body)")
            if st.form_submit_button("Crear Rutina", type="primary"):
                if r_name.strip():
                    rutinas.append({"nombre": r_name, "ejercicios": []})
                    use_cases.repository.save_config("workout_routines", json.dumps(data), st.session_state.user_id)
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if not rutinas:
        st.info("No tienes rutinas registradas. Crea una para empezar a planificar tu entrenamiento.")
        return
        
    # Mostrar rutinas como Tabs de Streamlit (Pestañas)
    tabs = st.tabs([r["nombre"] for r in rutinas])
    
    for i, tab in enumerate(tabs):
        rutina = rutinas[i]
        with tab:
            st.markdown('<div class="activity-card routine-card">', unsafe_allow_html=True)
            st.subheader(f"⚡ {rutina['nombre']}")
            
            # Formulario para agregar ejercicio a la rutina
            with st.form(f"add_ex_{i}"):
                cols = st.columns([3, 1, 1.2, 1, 1])
                ex_name = cols[0].text_input("Ejercicio", placeholder="Sentadilla con Barra")
                ex_sets = cols[1].number_input("Series", min_value=1, value=4)
                ex_reps = cols[2].text_input("Reps", placeholder="8-12", value="10")
                ex_weight = cols[3].text_input("Peso", placeholder="60 kg", value="-")
                
                # Usamos st.markdown con hack CSS para centrar verticalmente el botón
                cols[4].markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)
                submitted = cols[4].form_submit_button("Añadir")
                
                if submitted and ex_name.strip():
                    rutina["ejercicios"].append({
                        "nombre": ex_name.strip(),
                        "series": ex_sets,
                        "repeticiones": ex_reps.strip(),
                        "peso_kg": ex_weight.strip()
                    })
                    use_cases.repository.save_config("workout_routines", json.dumps(data), st.session_state.user_id)
                    st.rerun()
            
            # Mostrar la tabla de ejercicios si hay alguno
            if rutina["ejercicios"]:
                st.markdown("#### 📋 Ejercicios")
                # Cabecera simulada
                h_cols = st.columns([3, 1, 1.2, 1, 1])
                h_cols[0].markdown("**Nombre**")
                h_cols[1].markdown("**Series**")
                h_cols[2].markdown("**Reps**")
                h_cols[3].markdown("**Peso**")
                st.markdown("---")
                
                for j, ex in enumerate(rutina["ejercicios"]):
                    r_cols = st.columns([3, 1, 1.2, 1, 1])
                    r_cols[0].markdown(f"<p class='exercise-text'>{ex['nombre']}</p>", unsafe_allow_html=True)
                    r_cols[1].markdown(f"<p class='exercise-text'>{ex['series']}</p>", unsafe_allow_html=True)
                    r_cols[2].markdown(f"<p class='exercise-text'>{ex['repeticiones']}</p>", unsafe_allow_html=True)
                    r_cols[3].markdown(f"<p class='exercise-text'>{ex['peso_kg']}</p>", unsafe_allow_html=True)
                    
                    if r_cols[4].button("❌", key=f"del_ex_{i}_{j}", help="Eliminar ejercicio"):
                        rutina["ejercicios"].pop(j)
                        use_cases.repository.save_config("workout_routines", json.dumps(data), st.session_state.user_id)
                        st.rerun()
            else:
                st.write("Esta rutina está vacía. Agrega ejercicios usando el panel superior.")
                
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Botón para borrar la rutina
            col1, col2 = st.columns([4, 1])
            if col2.button("🗑️ Eliminar Rutina", key=f"del_rut_{i}"):
                rutinas.pop(i)
                use_cases.repository.save_config("workout_routines", json.dumps(data), st.session_state.user_id)
                st.rerun()

def main_app_view(use_cases):
    col1, col2 = st.columns([8, 1])
    with col1:
        st.title("🌙 TSUKUYOMI MASTER SYSTEM")
    with col2:
        st.write("")
        if st.button("Cerrar Sesión"):
            st.session_state.user_id = None
            st.rerun()

    menu_options = {
        "📊 Dashboard (Resumen)": view_dashboard,
        "🎯 Visión & Objetivos": view_vision,
        "📋 Proyectos (Kanban)": view_kanban,
        "🔁 Hábitos (Shūkan)": view_habits,
        "📝 Notas (Pizarrón)": view_notes,
        "🏋️ Deporte (Rutinas)": view_sports,
        "🧘‍♂️ Hansei (Reflexión)": view_hansei,
        "📅 Calendario": view_calendar
    }
    
    st.sidebar.markdown("### Navegación")
    menu = st.sidebar.radio("Opciones", list(menu_options.keys()), label_visibility="collapsed")

    # Ejecuta la función de vista seleccionada dinámicamente
    if menu in menu_options:
        menu_options[menu](use_cases)
        
        
    # --- Background Image Logic ---
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🖼️ Fondo de Pantalla")
    
    if "bg_image" not in st.session_state:
        bg = use_cases.repository.get_config("background_image", st.session_state.user_id)
        st.session_state.bg_image = bg if bg else None
        
    if st.session_state.bg_image:
        apply_dynamic_theme(st.session_state.bg_image)
    else:
        apply_dynamic_theme(get_default_bg_b64())
        
    uploaded_bg = st.sidebar.file_uploader("Subir imagen (PNG/JPG)", type=['png', 'jpg', 'jpeg'])
    if uploaded_bg is not None:
        try:
            # Optimize image
            img = Image.open(uploaded_bg).convert("RGB")
            # Downscale if massive to prevent base64 browser lag
            img.thumbnail((2560, 1440), Image.Resampling.LANCZOS)
            
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=92)
            base64_str = base64.b64encode(buffer.getvalue()).decode()
            
            st.session_state.bg_image = base64_str
            use_cases.repository.save_config("background_image", base64_str, st.session_state.user_id)
            st.rerun()
        except Exception as e:
            st.error(f"Error procesando imagen: {e}")
    elif st.session_state.bg_image:
        if st.sidebar.button("Quitar fondo actual", use_container_width=True):
            st.session_state.bg_image = None
            use_cases.repository.save_config("background_image", "", st.session_state.user_id)
            st.rerun()

