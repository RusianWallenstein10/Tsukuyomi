# 🌙 Tsukuyomi Master System

**Tsukuyomi Master System** es una aplicación integral de productividad personal, gestión de tiempo y alineación vital diseñada con una estética inmersiva (inspirada en la estética anime japonesa y el *Glassmorphism*). 

Está construida 100% en Python utilizando **Streamlit** y conectada a **Supabase** (PostgreSQL) como base de datos, implementando una arquitectura **MVC** (Modelo-Vista-Controlador) limpia y escalable.

---

## ✨ Características Principales

*   📊 **Dashboard de Alineación:** Resumen general de tus métricas, proyectos en foco (WIP) y progreso de alineación vital.
*   🎯 **Visión & Objetivos (Ikigai):** Define tus áreas de vida, visión a largo plazo y objetivos estratégicos.
*   📋 **Proyectos (Kanban):** Gestión de proyectos con filosofía Lean/5S. Incluye un límite de Trabajo en Progreso (WIP) para evitar la sobrecarga.
*   🔁 **Hábitos (Shūkan):** Registro diario de hábitos vinculados a tus objetivos para mantener la consistencia.
*   🏋️ **Deporte (Rutinas):** Planificador de rutinas de entrenamiento con pestañas interactivas para registrar series, repeticiones y peso.
*   📝 **Notas (Pizarrón):** Sistema interactivo de *sticky notes* (post-its) con físicas y colores personalizables.
*   🧘‍♂️ **Hansei (Reflexión):** Módulo de retrospectiva para escribir tus reflexiones y aplicar mejora continua (Kaizen).
*   📅 **Calendario (Bloques de Tiempo):** Organiza tus actividades diarias y rutinas por franjas horarias.
*   🤖 **Notificaciones Automáticas por Telegram:** Un *daemon* en segundo plano vigila tu calendario y te envía alertas directamente a Telegram **20 minutos antes** y **a la hora exacta** en que comienzan tus actividades.
*   🎨 **Motor de Temado Dinámico (Dynamic Theming):** Puedes subir cualquier imagen de fondo (JPG/PNG). El sistema la procesa, extrae su color dominante y luminancia matemática, y **reescribe el CSS en tiempo real** para crear un tema translúcido (*True Glassmorphism*) que se adapta perfectamente a fotos claras u oscuras.

---

## 🛠️ Stack Tecnológico

*   **Frontend & Interfaz:** [Streamlit](https://streamlit.io/)
*   **Base de Datos & Almacenamiento:** [Supabase](https://supabase.com/)
*   **Procesamiento de Imagen:** Pillow (PIL)
*   **Notificaciones:** Telegram Bot API
*   **Arquitectura:** Patrón MVC (Models, Views, Controllers) en Python puro.

---

## 🚀 Instalación y Despliegue Local

### 1. Clonar y Preparar el Entorno
Asegúrate de tener Python 3.9 o superior instalado.
```bash
git clone <tu-repositorio>
cd Tsukuyomi
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto y añade tus tokens y claves de acceso:
```env
SUPABASE_URL="https://<tu-id>.supabase.co"
SUPABASE_KEY="tu-anon-key"
TELEGRAM_BOT_TOKEN="tu-token-del-bot-creado-en-botfather"
TELEGRAM_CHAT_ID="tu-id-de-chat-de-telegram"
```

### 3. Base de Datos
El proyecto incluye un archivo `supabase_schema.sql` con todas las tablas relacionales necesarias (`activities`, `areas`, `objectives`, `projects`, `tasks`, `habits`, `habit_logs`, `reflections`, `app_config`). Ejecuta este script SQL directamente en el SQL Editor de tu panel de Supabase.

### 4. Ejecutar la Aplicación
```bash
streamlit run app.py
```
> **Nota:** La primera vez que se ejecuta, el sistema activará automáticamente el hilo en segundo plano que gestiona los recordatorios de Telegram.

---

## ☁️ Despliegue en Streamlit Community Cloud

Este proyecto está optimizado para ser desplegado gratuitamente en Streamlit Community Cloud:

1. Conecta tu repositorio de GitHub a [share.streamlit.io](https://share.streamlit.io/).
2. Configura como archivo principal: `app.py`.
3. En la sección **Advanced Settings > Secrets**, pega tus claves en formato TOML:
   ```toml
   SUPABASE_URL = "https://..."
   SUPABASE_KEY = "eyJh..."
   TELEGRAM_BOT_TOKEN = "..."
   TELEGRAM_CHAT_ID = "..."
   ```
4. Despliega la aplicación. 

*(Recordatorio: En cuentas gratuitas de Streamlit Cloud, la app "se duerme" si no recibe tráfico. Para que el bot de notificaciones siga activo 24/7, utiliza un servicio gratuito de ping como cron-job.org para hacer solicitudes HTTP y mantener la app despierta).*

---
*Desarrollado para mantener la disciplina, la alineación y el enfoque absoluto.* 🌙
