# Obtener la clasificación
import requests
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
def obtener_clasificacion(liga_id):
    url = f"https://api.football-data.org/v4/competitions/{liga_id}/standings"
    headers = {
        'X-Auth-Token': 'd21df9a683e74915bdb6dac39270a985'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        standings = data.get("standings", [])[0].get("table", [])
        return standings
    else:
        st.error(f"Error al obtener la clasificación: {response.status_code}")
        return []

def mostrar_clasificacion(clasificacion, liga,logos):
    if clasificacion:
        st.subheader("Clasificación Actual")
        data = []
        for equipo in clasificacion:
            # Cálculo de Diferencia de Goles
            dg_diferencia_goles = equipo["goalsFor"] - equipo["goalsAgainst"]
            
            # Obtener el logo del equipo
            club_name = equipo["team"]["name"].lower().replace(" ", "")
            logo_url = logos[liga].get(club_name, "")
            logo_html = f'<img src="{logo_url}" alt="{equipo["team"]["name"]}" style="width: 20px; height: 20px; vertical-align: middle;"> '
            
            # Preparar fila de datos en el formato solicitado
            data.append([
                equipo["position"],
                logo_html + equipo["team"]["name"].replace(" FC", ""),  # Añadir el logo al nombre del equipo
                equipo["playedGames"],
                equipo["won"],
                equipo["draw"],
                equipo["lost"],
                equipo["goalsFor"],
                equipo["goalsAgainst"],
                dg_diferencia_goles,
                equipo["points"]
            ])
        
        # Encabezados de la tabla
        columns = [
            "Posición", "Club", "PJ", "V", "E", 
            "D", "GF", "GC", 
            "DG", "Pts"
        ]
        
        # Crear DataFrame y configurar "Posición" como índice
        df = pd.DataFrame(data, columns=columns).set_index("Posición")
        
        # Convertir el DataFrame a HTML
        df_html = df.to_html(escape=False)
        
        # Mostrar la tabla con el índice configurado
        st.markdown(df_html, unsafe_allow_html=True)

def obtener_partidos(liga):
    url = f'https://api.football-data.org/v4/competitions/{liga}/matches'
    headers = {
        'X-Auth-Token': 'd21df9a683e74915bdb6dac39270a985'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        partidos = data['matches']
        
        # Fecha "hoy" como string, luego convertirla a datetime
        hoy = "2025-01-31 10:45:43.394385"
        hoy_datetime = datetime.strptime(hoy, "%Y-%m-%d %H:%M:%S.%f")
        
        un_mes_despues = hoy_datetime + timedelta(days=5)
        
        # Filtrar los partidos entre hoy y un mes después
        partidos_filtrados = [
            partido for partido in partidos 
            if hoy_datetime <= datetime.strptime(partido['utcDate'], '%Y-%m-%dT%H:%M:%SZ') <= un_mes_despues
        ]
        
        return partidos_filtrados
    else:
        st.error("No se pudieron obtener los partidos.")
        return []
    
def agrupar_partidos_por_jornadas(partidos, liga):
    jornadas_iniciales = {
        'LaLiga': 22,
        'Premier League': 24,
        'Serie A': 23,
        'Ligue 1': 20,
        'Bundesliga': 19
    }
    jornada_inicial = jornadas_iniciales.get(liga, 1)  # Si la liga no está definida, comienza desde la jornada 1
    
    # Ordenar partidos por fecha
    partidos.sort(key=lambda p: p['utcDate'])
    
    jornada_actual = []
    for partido in partidos:
        jornada_actual.append(partido)
    
    return {jornada_inicial: jornada_actual}
          
def mostrar_partidos(partidos, liga, logos):
    jornadas = agrupar_partidos_por_jornadas(partidos, liga)
    
    if not jornadas:
        st.markdown("No hay partidos en la jornada actual.")
        return
    
    # Obtener la jornada inicial
    jornada_actual_numero = list(jornadas.keys())[0]
    partidos_jornada_actual = jornadas[jornada_actual_numero]
    
    # Mostrar título de la jornada
    st.markdown(f"""
    <div style="font-size: 1.5rem; font-weight: bold; margin-top: 1rem; margin-bottom: 0.5rem;">
        Jornada {jornada_actual_numero}
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar los partidos de la jornada
    for partido in partidos_jornada_actual:
        local = partido['homeTeam']['name']
        visitante = partido['awayTeam']['name']
        
        # Convertir la fecha y sumar una hora
        fecha = datetime.strptime(partido['utcDate'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=1)
        
        fecha = fecha.strftime('%d/%m/%Y %H:%M')  # Día, mes, año y hora
        
        # Obtener logos
        logo_local = logos[liga].get(local.lower().replace(" ", ""), "")
        logo_visitante = logos[liga].get(visitante.lower().replace(" ", ""), "")
        
        # Generar el HTML
        st.markdown(f"""
<div class="match-container" style="display: flex; align-items: center; justify-content: space-between; padding: 1rem; background-color: #000000; margin-bottom: 0.5rem; border-radius: 8px;">
    <div class="team-container" style="text-align: center; width: 40%;">
        <div class="team-logo">
            <img src="{logo_local}" alt="{local}" style="width: 100px; height: 100px;">
        </div>
        <div class="team-name" style="font-weight: bold; margin-top: 0.5rem; font-size: 1.2rem;">
            {local}
        </div>
    </div>
    <div class="match-time" style="text-align: center; width: 20%; font-size: 1.2rem; font-weight: bold;">
        <strong>{fecha}</strong>
    </div>
    <div class="team-container" style="text-align: center; width: 40%;">
        <div class="team-logo">
            <img src="{logo_visitante}" alt="{visitante}" style="width: 100px; height: 100px;">
        </div>
        <div class="team-name" style="font-weight: bold; margin-top: 0.5rem; font-size: 1.2rem;">
            {visitante}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
