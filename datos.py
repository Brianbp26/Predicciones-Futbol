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

def mostrar_clasificacion(clasificacion, liga):
    logos = {
    "LaLiga": {
    "athleticclub": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/athletic.png",
    "clubatléticodemadrid": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/atleticomadrid.png",
    "fcbarcelona": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/barcelona.png",
    "deportivoalavés": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/alaves.png",
    "realbetisbalompié": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/betis.png",
    "rcceltadevigo": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/celta.png",
    "rcdespanyoldebarcelona": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/espanyol.png",
    "getafecf": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/getafe.png",
    "gironafc": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/girona.png",
    "udlaspalmas": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/laspalmas.png",
    "cdleganés": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/leganes.png",
    "rcdmallorca": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/mallorca.png",
    "caosasuna": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/osasuna.png",
    "rayovallecanodemadrid": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/rayovallecano.png",
    "realmadridcf": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/realmadrid.png",
    "realsociedaddefútbol": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/realsociedad.png",
    "sevillafc": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/sevilla.png",
    "valenciacf": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/valencia.png",
    "realvalladolidcf": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/valladolid.png",
    "villarrealcf": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/villarreal.png"
    },
    "Premier League": {
        "newcastleunitedfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/newcastle.png",
        "afcbournemouth": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/bournemouth.png",
        "arsenalfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/arsenal.png",
        "astonvillafc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/astonvilla.png",
        "brentfordfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/brentford.png",
        "brighton&hovealbionfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/brighton.png",
        "chelseafc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/chelsea.png",
        "crystalpalacefc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/crystalpalace.png",
        "evertonfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/everton.png",
        "ipswichtownfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/ipswich.png",
        "nottinghamforestfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/nottinghamforest.png",
        "fulhamfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/fulham.png",
        "leicestercityfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/leicester.png",
        "liverpoolfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/liverpool.png",
        "manchesterunitedfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/manunited.png",
        "manchestercityfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/mancity.png",
        "southamptonfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/southampton.png",
        "tottenhamhotspurfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/tottenham.png",
        "westhamunitedfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/westham.png",
        "wolverhamptonwanderersfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/wolves.png"
        },
    "Serie A": {
       "atalantabc": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/atalanta.png",
        "bolognafc1909": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/bolonia.png",
        "cagliaricalcio": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/cagliari.png",
        "empolifc": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/empoli.png",
        "acffiorentina": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/fiorentina.png",
        "hellasveronafc": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/hellasverona.png",
        "genoacfc": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/genoa.png",
        "fcinternazionalemilano": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/inter.png",
        "juventusfc": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/juventus.png",
        "sslazio": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/lazio.png",
        "uslecce": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/lecce.png",
        "acmilan": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/milan.png",
        "acmonza": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/monza.png",
        "sscnapoli": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/napoles.png",
        "asroma": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/roma.png",
        "parmacalcio1913": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/parma.png",
        "como1907": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/como.png",
        "torinofc": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/torino.png",
        "udinesecalcio": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/udinese.png",
        "veneziafc": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/venezia.png"
        },
    "Bundesliga": {
        "fcaugsburg": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/augsburgo.png",
        "bayer04leverkusen": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/bayerleverkusen.png",
        "fcbayernmünchen": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/bayernmunich.png",
        "vflbochum1848": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/bochum.png",
        "borussiadortmund": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/borussiadortmund.png",
        "borussiamönchengladbach": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/borussiamgladbach.png",
        "eintrachtfrankfurt": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/eintrachtfrankfurt.png",
        "scfreiburg": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/friburgo.png",
        "1.fcheidenheim1846": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/heidenheim.png",
        "tsg1899hoffenheim": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/hoffenheim.png",
        "holsteinkiel": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/holsteinkiel.png",
        "1.fsvmainz05": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/mainz.png",
        "rbleipzig": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/rbleipzig.png",
        "fcst.pauli1910": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/st_pauli.png",
        "vfbstuttgart": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/stuttgart.png",
        "1.fcunionberlin": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/unionberlin.png",
        "svwerderbremen": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/werderbremen.png",
        "vflwolfsburg": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/wolfsburgo.png"
        },
    "Ligue 1": {
        "angerssco": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/angers.png",
        "ajauxerre": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/auxerre.png",
        "rcstrasbourgalsace": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/estrasburgo.png",
        "lehavreac": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/havre.png",
        "racingclubdelens": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/lens.png",
        "lilleosc": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/lille.png",
        "olympiquelyonnais": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/lyon.png",
        "olympiquedemarseille": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/marsella.png",
        "asmonacofc": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/monaco.png",
        "montpellierhsc": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/montpellier.png",
        "fcnantes": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/nantes.png",
        "ogcnice": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/niza.png",
        "parissaint-germainfc": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/psg.png",
        "assaint-étienne": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/saintetienne.png",
        "stadebrestois29": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/stadebretois.png",
        "stadedereims": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/stadereims.png",
        "staderennaisfc1901": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/staderennais.png",
        "toulousefc": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/toulouse.png"
        }
}
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
        hoy = "2025-01-17 10:45:43.394385"
        hoy_datetime = datetime.strptime(hoy, "%Y-%m-%d %H:%M:%S.%f")
        
        # Sumar 90 días a la fecha actual
        un_mes_despues = hoy_datetime + timedelta(days=90)
        
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
    'LaLiga': 20,   
    'Premier League': 22,   
    'Serie A': 21,   
    'Ligue 1': 18,   
    'Bundesliga': 17  }
    jornada_inicial = jornadas_iniciales.get(liga, 1)  # Si la liga no está definida, comienza desde la jornada 1
    
    # Ordenar partidos por fecha
    partidos.sort(key=lambda p: p['utcDate'])
    
    jornadas = []
    jornada_actual = []
    jornada_numero = jornada_inicial  # Comienza desde la jornada inicial
    inicio_jornada = None
    
    for partido in partidos:
        fecha_partido = datetime.strptime(partido['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
        
        if not inicio_jornada:
            # Inicio de una nueva jornada
            inicio_jornada = fecha_partido
            jornada_actual.append(partido)
        elif (fecha_partido - inicio_jornada).days > 5:
            # Cerrar la jornada actual si han pasado más de 5 días
            jornadas.append((jornada_numero, jornada_actual))
            jornada_numero += 1
            jornada_actual = [partido]
            inicio_jornada = fecha_partido
        else:
            # Continuar en la misma jornada
            jornada_actual.append(partido)
    
    # Añadir la última jornada si está incompleta
    if jornada_actual:
        jornadas.append((jornada_numero, jornada_actual))
    
    return jornadas

def mostrar_partidos(partidos, liga):
    # Agrupar partidos en jornadas
    logos = {
    "LaLiga": {
    "athleticclub": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/athletic.png",
    "clubatléticodemadrid": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/atleticomadrid.png",
    "fcbarcelona": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/barcelona.png",
    "deportivoalavés": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/alaves.png",
    "realbetisbalompié": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/betis.png",
    "rcceltadevigo": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/celta.png",
    "rcdespanyoldebarcelona": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/espanyol.png",
    "getafecf": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/getafe.png",
    "gironafc": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/girona.png",
    "udlaspalmas": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/laspalmas.png",
    "cdleganés": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/leganes.png",
    "rcdmallorca": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/mallorca.png",
    "caosasuna": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/osasuna.png",
    "rayovallecanodemadrid": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/rayovallecano.png",
    "realmadridcf": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/realmadrid.png",
    "realsociedaddefútbol": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/realsociedad.png",
    "sevillafc": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/sevilla.png",
    "valenciacf": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/valencia.png",
    "realvalladolidcf": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/valladolid.png",
    "villarrealcf": "https://raw.githubusercontent.com/Brianbp26/Logos/587d8554343bb8bbecf8de5342f7446a83c1d8ce/villarreal.png"
    },
    "Premier League": {
        "newcastleunitedfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/newcastle.png",
        "afcbournemouth": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/bournemouth.png",
        "arsenalfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/arsenal.png",
        "astonvillafc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/astonvilla.png",
        "brentfordfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/brentford.png",
        "brighton&hovealbionfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/brighton.png",
        "chelseafc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/chelsea.png",
        "crystalpalacefc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/crystalpalace.png",
        "evertonfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/everton.png",
        "ipswichtownfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/ipswich.png",
        "nottinghamforestfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/nottinghamforest.png",
        "fulhamfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/fulham.png",
        "leicestercityfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/leicester.png",
        "liverpoolfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/liverpool.png",
        "manchesterunitedfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/manunited.png",
        "manchestercityfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/mancity.png",
        "southamptonfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/southampton.png",
        "tottenhamhotspurfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/tottenham.png",
        "westhamunitedfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/westham.png",
        "wolverhamptonwanderersfc": "https://raw.githubusercontent.com/Brianbp26/Logos/8e59d34d0708184b05fca212a58335b28b7c4cdd/wolves.png"
        },
    "Serie A": {
       "atalantabc": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/atalanta.png",
        "bolognafc1909": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/bolonia.png",
        "cagliaricalcio": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/cagliari.png",
        "empolifc": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/empoli.png",
        "acffiorentina": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/fiorentina.png",
        "hellasveronafc": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/hellasverona.png",
        "genoacfc": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/genoa.png",
        "fcinternazionalemilano": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/inter.png",
        "juventusfc": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/juventus.png",
        "sslazio": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/lazio.png",
        "uslecce": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/lecce.png",
        "acmilan": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/milan.png",
        "acmonza": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/monza.png",
        "sscnapoli": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/napoles.png",
        "asroma": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/roma.png",
        "parmacalcio1913": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/parma.png",
        "como1907": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/como.png",
        "torinofc": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/torino.png",
        "udinesecalcio": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/udinese.png",
        "veneziafc": "https://raw.githubusercontent.com/Brianbp26/Logos/34d8e0a49b561f9f40530d0641b42e4905b5a09a/venezia.png"
        },
    "Bundesliga": {
        "fcaugsburg": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/augsburgo.png",
        "bayer04leverkusen": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/bayerleverkusen.png",
        "fcbayernmünchen": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/bayernmunich.png",
        "vflbochum1848": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/bochum.png",
        "borussiadortmund": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/borussiadortmund.png",
        "borussiamönchengladbach": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/borussiamgladbach.png",
        "eintrachtfrankfurt": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/eintrachtfrankfurt.png",
        "scfreiburg": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/friburgo.png",
        "1.fcheidenheim1846": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/heidenheim.png",
        "tsg1899hoffenheim": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/hoffenheim.png",
        "holsteinkiel": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/holsteinkiel.png",
        "1.fsvmainz05": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/mainz.png",
        "rbleipzig": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/rbleipzig.png",
        "fcst.pauli1910": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/st_pauli.png",
        "vfbstuttgart": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/stuttgart.png",
        "1.fcunionberlin": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/unionberlin.png",
        "svwerderbremen": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/werderbremen.png",
        "vflwolfsburg": "https://raw.githubusercontent.com/Brianbp26/Logos/dfd5d4d28184c436605a74a19076f3859eef0ade/wolfsburgo.png"
        },
    "Ligue 1": {
        "angerssco": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/angers.png",
        "ajauxerre": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/auxerre.png",
        "rcstrasbourgalsace": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/estrasburgo.png",
        "lehavreac": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/havre.png",
        "racingclubdelens": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/lens.png",
        "lilleosc": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/lille.png",
        "olympiquelyonnais": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/lyon.png",
        "olympiquedemarseille": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/marsella.png",
        "asmonacofc": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/monaco.png",
        "montpellierhsc": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/montpellier.png",
        "fcnantes": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/nantes.png",
        "ogcnice": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/niza.png",
        "parissaint-germainfc": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/psg.png",
        "assaint-étienne": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/saintetienne.png",
        "stadebrestois29": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/stadebretois.png",
        "stadedereims": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/stadereims.png",
        "staderennaisfc1901": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/staderennais.png",
        "toulousefc": "https://raw.githubusercontent.com/Brianbp26/Logos/86bca5f130397bbc8c33368e275ce9a299f1e5ed/toulouse.png"
        }
}
    jornadas = agrupar_partidos_por_jornadas(partidos, liga)
    
    for numero_jornada, partidos_jornada in jornadas:
        # Mostrar título de la jornada
        st.markdown(f"""
        <div style="font-size: 1.5rem; font-weight: bold; margin-top: 1rem; margin-bottom: 0.5rem;">
            Jornada {numero_jornada}
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar los partidos de la jornada
        for partido in partidos_jornada:
            local = partido['homeTeam']['name']
            visitante = partido['awayTeam']['name']
            
            # Convertir la fecha
            fecha = datetime.strptime(partido['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
            
            # Verificar si la hora es 00:00
            if fecha.strftime('%H:%M') == '00:00':
                fecha = fecha.strftime('%d/%m/%Y')  # Solo día, mes y año
            else:
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