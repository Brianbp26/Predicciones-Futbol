import requests
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# Cache the API results to avoid redundant calls
@st.cache_data
def obtener_clasificacion(liga_id):
    url = f"https://api.football-data.org/v4/competitions/{liga_id}/standings"
    headers = {'X-Auth-Token': 'd21df9a683e74915bdb6dac39270a985'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        standings = data.get("standings", [])[0].get("table", [])
        return standings
    else:
        st.error(f"Error al obtener la clasificación: {response.status_code}")
        return []

def mostrar_clasificacion(clasificacion, liga, logos):
    if clasificacion:
        st.subheader("Clasificación Actual")
        data = [
            [
                equipo["position"],
                f'<img src="{logos[liga].get(equipo["team"]["name"].lower().replace(" ", ""), "")}" alt="{equipo["team"]["name"]}" style="width: 20px; height: 20px; vertical-align: middle;"> {equipo["team"]["name"].replace(" FC", "")}',
                equipo["playedGames"],
                equipo["won"],
                equipo["draw"],
                equipo["lost"],
                equipo["goalsFor"],
                equipo["goalsAgainst"],
                equipo["goalsFor"] - equipo["goalsAgainst"],
                equipo["points"]
            ]
            for equipo in clasificacion
        ]
        
        columns = ["Posición", "Club", "PJ", "V", "E", "D", "GF", "GC", "DG", "Pts"]
        df = pd.DataFrame(data, columns=columns).set_index("Posición")
        st.markdown(df.to_html(escape=False), unsafe_allow_html=True)

@st.cache_data
def obtener_partidos(liga):
    url = f'https://api.football-data.org/v4/competitions/{liga}/matches'
    headers = {'X-Auth-Token': 'd21df9a683e74915bdb6dac39270a985'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        partidos = data['matches']
        
        # Fecha "hoy" como string, luego convertirla a datetime
        hoy = "2025-01-17 10:45:43.394385"
        hoy_datetime = datetime.strptime(hoy, "%Y-%m-%d %H:%M:%S.%f")
        
        # Sumar 90 días a la fecha actual
        un_mes_despues = hoy_datetime + timedelta(days=5)
        
        partidos_filtrados = [
            partido for partido in partidos 
            if hoy_datetime <= datetime.strptime(partido['utcDate'], '%Y-%m-%dT%H:%M:%SZ') <= un_mes_despues
        ]
        
        return partidos_filtrados
    else:
        st.error("No se pudieron obtener los partidos.")
        return []

def agrupar_partidos_por_jornadas(partidos, liga):
    jornadas_iniciales = {'LaLiga': 20, 'Premier League': 22, 'Serie A': 21, 'Ligue 1': 18, 'Bundesliga': 17}
    jornada_inicial = jornadas_iniciales.get(liga, 1)
    
    partidos.sort(key=lambda p: p['utcDate'])
    
    jornadas = []
    jornada_actual = []
    jornada_numero = jornada_inicial
    inicio_jornada = None
    
    for partido in partidos:
        fecha_partido = datetime.strptime(partido['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
        
        if not inicio_jornada:
            inicio_jornada = fecha_partido
            jornada_actual.append(partido)
        elif (fecha_partido - inicio_jornada).days > 5:
            jornadas.append((jornada_numero, jornada_actual))
            jornada_numero += 1
            jornada_actual = [partido]
            inicio_jornada = fecha_partido
        else:
            jornada_actual.append(partido)
    
    if jornada_actual:
        jornadas.append((jornada_numero, jornada_actual))
    
    return jornadas

def mostrar_partidos(partidos, liga, logos):
    jornadas = agrupar_partidos_por_jornadas(partidos, liga)
    
    for numero_jornada, partidos_jornada in jornadas:
        st.markdown(f"""
        <div style="font-size: 1.5rem; font-weight: bold; margin-top: 1rem; margin-bottom: 0.5rem;">
            Jornada {numero_jornada}
        </div>
        """, unsafe_allow_html=True)
        
        for partido in partidos_jornada:
            local = partido['homeTeam']['name']
            visitante = partido['awayTeam']['name']
            fecha = datetime.strptime(partido['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
            fecha_str = fecha.strftime('%d/%m/%Y %H:%M') if fecha.strftime('%H:%M') != '00:00' else fecha.strftime('%d/%m/%Y')
            logo_local = logos[liga].get(local.lower().replace(" ", ""), "")
            logo_visitante = logos[liga].get(visitante.lower().replace(" ", ""), "")
            
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
                    <strong>{fecha_str}</strong>
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
