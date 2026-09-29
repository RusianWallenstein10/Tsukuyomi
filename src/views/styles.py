import streamlit as st

def inject_styles():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        
        /* Hide Streamlit Default Elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {background-color: transparent !important;}
        
        /* Global App Style */
        .stApp { 
            background-color: #09090b; 
            color: #fafafa; 
            font-family: 'Outfit', sans-serif;
        }

        /* Animations */
        @keyframes slideUpFade {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Typography */
        h1, h2, h3, h4 {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 600 !important;
            letter-spacing: -0.5px;
        }

        h1 {
            background: -webkit-linear-gradient(45deg, #ffffff, #a1a1aa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Glassmorphism Cards (Activity, Kanban, etc) */
        .activity-card, .kanban-column, div[data-testid="stExpander"], div[data-testid="stForm"], div[data-testid="stVerticalBlock"] > div[style*="border"] {
            background: rgba(24, 24, 27, 0.4) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 16px !important;
            padding: 15px !important;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            animation: slideUpFade 0.4s ease-out;
        }
        
        /* Hover effects */
        .activity-card:hover, div[data-testid="stVerticalBlock"] > div[style*="border"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px -8px rgba(0,0,0,0.5) !important;
            border-color: rgba(255, 255, 255, 0.15) !important;
            background: rgba(24, 24, 27, 0.7) !important;
        }
        
        /* Inputs and Buttons styling */
        div[data-baseweb="input"] > div, div[data-baseweb="select"] > div, textarea {
            background-color: #18181b !important;
            border: 1px solid #3f3f46 !important;
            border-radius: 10px !important;
            color: #fff !important;
            transition: all 0.2s ease !important;
        }

        div[data-baseweb="input"] > div:focus-within, div[data-baseweb="select"] > div:focus-within, textarea:focus {
            border-color: #8b5cf6 !important;
            box-shadow: 0 0 0 1px #8b5cf6 !important;
        }
        
        /* Primary Buttons (Tsukuyomi Theme) */
        button[kind="primary"] {
            background: linear-gradient(135deg, #b91c1c 0%, #7f1d1d 100%) !important;
            border: 1px solid #ef4444 !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            letter-spacing: 1px !important;
            color: white !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(220, 38, 38, 0.3), inset 0 0 10px rgba(0,0,0,0.5) !important;
            text-transform: uppercase !important;
        }
        button[kind="primary"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(220, 38, 38, 0.6), inset 0 0 10px rgba(0,0,0,0.5) !important;
            border-color: #f87171 !important;
        }

        /* Secondary Buttons */
        button[kind="secondary"] {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
            transition: all 0.2s ease !important;
        }
        button[kind="secondary"]:hover {
            background: rgba(255, 255, 255, 0.08) !important;
            border-color: rgba(255, 255, 255, 0.2) !important;
        }
        
        /* Sidebar styling (Glassmorphism) */
        [data-testid="stSidebar"] {
            background-color: rgba(9, 9, 11, 0.3) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        [data-testid="stSidebarHeader"] {
            background-color: transparent !important;
        }

        /* Custom Sidebar Navigation (st.radio styling) */
        section[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label {
            padding: 12px 16px;
            border-radius: 10px;
            margin-bottom: 8px;
            background-color: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.2s ease;
            cursor: pointer;
        }
        section[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label:hover {
            background-color: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.15);
            transform: translateX(4px);
        }
        /* Hide the radio bullet circle completely */
        section[data-testid="stSidebar"] .stRadio div[role="radio"] {
            display: none !important;
        }
        section[data-testid="stSidebar"] .stRadio label > div:first-child {
            display: none !important;
        }
        /* Style the text inside the navigation */
        section[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label p {
            font-size: 1.05rem !important;
            font-weight: 500 !important;
            margin: 0 !important;
        }
        
        /* Metrics styling */
        [data-testid="stMetricValue"] {
            font-weight: 700 !important;
            font-size: 2.5rem !important;
            background: -webkit-linear-gradient(45deg, #10b981, #34d399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Progress Bars */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #8b5cf6, #d946ef) !important;
            border-radius: 10px;
        }

        /* Tabs */
        button[data-baseweb="tab"] {
            background-color: transparent !important;
            border-bottom: 2px solid transparent !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            border-bottom: 2px solid #8b5cf6 !important;
        }
    </style>
""", unsafe_allow_html=True)
