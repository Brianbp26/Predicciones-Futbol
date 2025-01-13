import streamlit as st
from datetime import datetime
import pandas as pd
import os

# Configuración de la página
st.set_page_config(
    page_title="Predicciones Fútbol",
    page_icon="⚽",
    layout="wide"
)

# Rutas base
LOGOS_PATH = os.path.join(os.path.dirname(__file__), "logos")

# Aplicar algunos estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
    }
    .match-container {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar para selección de liga
st.sidebar.title("⚽ Predicciones Fútbol")
liga_seleccionada = st.sidebar.selectbox(
    "Selecciona una liga",
    ["LaLiga", "Premier League", "Serie A", "Bundesliga", "Ligue 1"]
)

# Diccionario para mapear nombres de equipos a nombres de archivo
NOMBRES_EQUIPOS = {
    'RCD Espanyol': 'espanyol',
    'Valladolid': 'valladolid',
    'Osasuna': 'osasuna',
    'Rayo Vallecano': 'rayovallecano',
    'Leganés': 'leganes',
    'Atlético Madrid': 'atleticomadrid',
    'Celta de Vigo': 'celta',
    'Athletic': 'athletic',
    'Getafe': 'getafe',
    'Barcelona': 'barcelona',
    'Betis': 'betis',
    'Alavés': 'alaves',
    'Real Madrid': 'realmadrid',
    'U. D. Las Palmas': 'laspalmas',
    'Valencia C. F.': 'valencia',
    'Real Sociedad': 'realsociedad',
    'Girona': 'girona',
    'Sevilla': 'sevilla',
    'Villarreal': 'villarreal',
    'R.C.D. Mallorca': 'mallorca'
}

# Función para cargar logos
def cargar_logo(equipo):
    # Obtener el nombre del archivo desde el diccionario
    nombre_archivo = NOMBRES_EQUIPOS.get(equipo, equipo.lower().replace(' ', ''))
    logo_path = os.path.join(LOGOS_PATH, "España", "Primera División", f"{nombre_archivo}.png")
    if os.path.exists(logo_path):
        return logo_path
    return None

# Datos de ejemplo con los partidos de la jornada 20
partidos_ejemplo = pd.DataFrame({
    'local': ['RCD Espanyol', 'Osasuna', 'Leganés', 'Celta de Vigo', 
              'Getafe', 'Betis', 'Real Madrid', 'Valencia C. F.', 
              'Girona', 'Villarreal'],
    'visitante': ['Valladolid', 'Rayo Vallecano', 'Atlético Madrid', 'Athletic',
                  'Barcelona', 'Alavés', 'U. D. Las Palmas', 'Real Sociedad',
                  'Sevilla', 'R.C.D. Mallorca'],
    'fecha': ['2024-01-17', '2024-01-18', '2024-01-18', '2024-01-18',
              '2024-01-18', '2024-01-19', '2024-01-19', '2024-01-19',
              '2024-01-19', '2024-01-20'],
    'hora': ['21:00', '14:00', '16:15', '18:30',
             '21:00', '14:00', '16:15', '18:30',
             '21:00', '21:00'],
    'prob_local': [0.35, 0.40, 0.30, 0.35,
                   0.25, 0.45, 0.60, 0.40,
                   0.45, 0.50],
    'prob_empate': [0.30, 0.30, 0.35, 0.30,
                    0.25, 0.30, 0.25, 0.30,
                    0.30, 0.30],
    'prob_visitante': [0.35, 0.30, 0.35, 0.35,
                       0.50, 0.25, 0.15, 0.30,
                       0.25, 0.20],
    'pred_goles_local': [1, 2, 1, 1,
                         1, 2, 3, 2,
                         2, 2],
    'pred_goles_visitante': [1, 1, 2, 1,
                            2, 0, 0, 1,
                            1, 0]
})

# Header principal
st.title(f"Predicciones {liga_seleccionada}")
st.markdown("---")

# Información de la jornada
st.subheader("Jornada 20 de 38 - Próximos partidos")

# Mostrar los partidos
for idx, partido in partidos_ejemplo.iterrows():
    # Crear tres columnas para cada partido
    col1, col2, col3 = st.columns([2,3,2])
    
    with st.container():
        st.markdown('<div class="match-container">', unsafe_allow_html=True)
        
        # Columna equipo local
        with col1:
            logo_local = cargar_logo(partido['local'])
            if logo_local:
                st.image(logo_local, width=100)
            st.markdown(f"<h3 style='text-align: center;'>{partido['local']}</h3>", unsafe_allow_html=True)

        # Columna central con predicciones
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center;'>{partido['pred_goles_local']} - {partido['pred_goles_visitante']}</h2>", unsafe_allow_html=True)
            
            # Mostrar probabilidades
            col_prob1, col_prob2, col_prob3 = st.columns(3)
            with col_prob1:
                st.metric("Victoria Local", f"{int(partido['prob_local']*100)}%")
            with col_prob2:
                st.metric("Empate", f"{int(partido['prob_empate']*100)}%")
            with col_prob3:
                st.metric("Victoria Visitante", f"{int(partido['prob_visitante']*100)}%")

        # Columna equipo visitante
        with col3:
            logo_visitante = cargar_logo(partido['visitante'])
            if logo_visitante:
                st.image(logo_visitante, width=100)
            st.markdown(f"<h3 style='text-align: center;'>{partido['visitante']}</h3>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

# Métricas adicionales en el sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Estadísticas del Modelo")
st.sidebar.metric("Precisión Global", "73%")
st.sidebar.metric("Partidos Predichos", "152")
