import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os
import glob

def load_data(ruta):
    """
    Carga los datos desde archivos CSV de La Liga
    """
    archivos = glob.glob(ruta)
    
    if not archivos:
        raise ValueError(f"No se encontraron archivos en la ruta: {ruta}")
    
    print(f"Archivos encontrados: {archivos}")
    
    dataframes = []
    for f in archivos:
        try:
            temp = pd.read_csv(f, usecols=range(22))
            años = os.path.basename(f).split('_')[1]
            temp['Temporada'] = '20' + años
            dataframes.append(temp)
        except Exception as e:
            print(f"Error al procesar archivo {f}: {str(e)}")
    
    if not dataframes:
        raise ValueError("No se pudo cargar ningún archivo correctamente")
    
    return pd.concat(dataframes, ignore_index=True)

def calcular_posicion_tabla(df, equipo):
    """
    Calcula la posición en la tabla de un equipo para la temporada actual
    """
    # Obtener la temporada más reciente
    ultima_temporada = df['Temporada'].max()
    
    # Filtrar solo los partidos de la temporada actual
    partidos_temporada = df[df['Temporada'] == ultima_temporada]
    
    if len(partidos_temporada) == 0:
        return 10  # Posición media por defecto
        
    equipos_stats = {}
    
    # Inicializar estadísticas para todos los equipos
    equipos = set(partidos_temporada['HomeTeam'].unique()) | set(partidos_temporada['AwayTeam'].unique())
    for eq in equipos:
        equipos_stats[eq] = {'puntos': 0, 'gf': 0, 'gc': 0}
    
    # Calcular estadísticas
    for _, partido in partidos_temporada.iterrows():
        # Actualizar goles
        equipos_stats[partido['HomeTeam']]['gf'] += partido['FTHG']
        equipos_stats[partido['HomeTeam']]['gc'] += partido['FTAG']
        equipos_stats[partido['AwayTeam']]['gf'] += partido['FTAG']
        equipos_stats[partido['AwayTeam']]['gc'] += partido['FTHG']
        
        # Actualizar puntos
        if partido['FTR'] == 'H':
            equipos_stats[partido['HomeTeam']]['puntos'] += 3
        elif partido['FTR'] == 'A':
            equipos_stats[partido['AwayTeam']]['puntos'] += 3
        else:
            equipos_stats[partido['HomeTeam']]['puntos'] += 1
            equipos_stats[partido['AwayTeam']]['puntos'] += 1
    
    # Ordenar equipos por puntos y diferencia de goles
    tabla = sorted(equipos_stats.items(), 
                  key=lambda x: (x[1]['puntos'], x[1]['gf'] - x[1]['gc'], x[1]['gf']), 
                  reverse=True)
    
    # Encontrar posición del equipo
    for pos, (team, _) in enumerate(tabla, 1):
        if team == equipo:
            return pos
    
    return 10  # Posición media por defecto si no se encuentra

def prepare_data_for_model(df, home_team, away_team):
    """
    Prepara los datos para el modelo usando todas las temporadas con ponderación
    """
    # Intentar múltiples formatos de fecha
    date_formats = ["%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d"]
    for fmt in date_formats:
        try:
            df['Date'] = pd.to_datetime(df['Date'], format=fmt)
            break
        except ValueError:
            continue
    else:
        # Si todos los formatos fallan, intentar con dayfirst=True
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    
    df = df.dropna(subset=['Date'])  # Eliminar filas con fechas no válidas
    df = df.sort_values('Date')
    
    # Obtener todas las temporadas ordenadas
    temporadas = sorted(df['Temporada'].unique())
    num_temporadas = len(temporadas)
    
    # Crear diccionario de pesos para cada temporada
    # La temporada más reciente tendrá peso 1, y las anteriores irán disminuyendo
    pesos_temporadas = {temp: 1 - (0.8 * (num_temporadas - i - 1) / (num_temporadas - 1)) 
                        for i, temp in enumerate(temporadas)}
    
    # Inicializar variables para acumular estadísticas ponderadas
    stats = {
        'home_wins': 0,
        'home_draws': 0,
        'home_losses': 0,
        'away_wins': 0,
        'away_draws': 0,
        'away_losses': 0,
        'home_goals_scored': 0,
        'home_goals_conceded': 0,
        'away_goals_scored': 0,
        'away_goals_conceded': 0,
        'h2h_matches': 0,
        'h2h_home_wins': 0,
        'h2h_away_wins': 0,
        'h2h_draws': 0
    }
    
    # Calcular estadísticas ponderadas por temporada
    for temporada in temporadas:
        peso = pesos_temporadas[temporada]
        df_temp = df[df['Temporada'] == temporada]
        
        # Partidos como local del equipo local
        home_local = df_temp[df_temp['HomeTeam'] == home_team]
        stats['home_wins'] += peso * sum(home_local['FTR'] == 'H')
        stats['home_draws'] += peso * sum(home_local['FTR'] == 'D')
        stats['home_losses'] += peso * sum(home_local['FTR'] == 'A')
        stats['home_goals_scored'] += peso * home_local['FTHG'].mean() if len(home_local) > 0 else 0
        stats['home_goals_conceded'] += peso * home_local['FTAG'].mean() if len(home_local) > 0 else 0
        
        # Partidos como visitante del equipo visitante
        away_visit = df_temp[df_temp['AwayTeam'] == away_team]
        stats['away_wins'] += peso * sum(away_visit['FTR'] == 'A')
        stats['away_draws'] += peso * sum(away_visit['FTR'] == 'D')
        stats['away_losses'] += peso * sum(away_visit['FTR'] == 'H')
        stats['away_goals_scored'] += peso * away_visit['FTAG'].mean() if len(away_visit) > 0 else 0
        stats['away_goals_conceded'] += peso * away_visit['FTHG'].mean() if len(away_visit) > 0 else 0
        
        # Enfrentamientos directos
        h2h_matches = df_temp[
            ((df_temp['HomeTeam'] == home_team) & (df_temp['AwayTeam'] == away_team)) |
            ((df_temp['HomeTeam'] == away_team) & (df_temp['AwayTeam'] == home_team))
        ]
        
        if len(h2h_matches) > 0:
            stats['h2h_matches'] += peso * len(h2h_matches)
            stats['h2h_home_wins'] += peso * sum((h2h_matches['HomeTeam'] == home_team) & (h2h_matches['FTR'] == 'H'))
            stats['h2h_away_wins'] += peso * sum((h2h_matches['HomeTeam'] == away_team) & (h2h_matches['FTR'] == 'H'))
            stats['h2h_draws'] += peso * sum(h2h_matches['FTR'] == 'D')
    
    # Obtener los últimos 5 partidos (sin ponderar, son los más recientes)
    ultimos_partidos_home = df[
        (df['HomeTeam'] == home_team) | 
        (df['AwayTeam'] == home_team)
    ].tail(5)
    
    ultimos_partidos_away = df[
        (df['HomeTeam'] == away_team) | 
        (df['AwayTeam'] == away_team)
    ].tail(5)
    
    # Preparar features finales
    features = {
        # Posiciones en la tabla actual
        'home_position': calcular_posicion_tabla(df, home_team),
        'away_position': calcular_posicion_tabla(df, away_team),
        
        # Estadísticas históricas ponderadas
        'home_historical_wins_weighted': stats['home_wins'],
        'home_historical_draws_weighted': stats['home_draws'],
        'home_historical_losses_weighted': stats['home_losses'],
        'away_historical_wins_weighted': stats['away_wins'],
        'away_historical_draws_weighted': stats['away_draws'],
        'away_historical_losses_weighted': stats['away_losses'],
        
        # Promedios de goles históricos ponderados
        'home_historical_goals_scored_weighted': stats['home_goals_scored'],
        'home_historical_goals_conceded_weighted': stats['home_goals_conceded'],
        'away_historical_goals_scored_weighted': stats['away_goals_scored'],
        'away_historical_goals_conceded_weighted': stats['away_goals_conceded'],
        
        # Historial directo ponderado
        'h2h_home_wins_weighted': stats['h2h_home_wins'],
        'h2h_away_wins_weighted': stats['h2h_away_wins'],
        'h2h_draws_weighted': stats['h2h_draws'],
        'h2h_total_matches': stats['h2h_matches'],
        
        # Forma reciente (últimos 5 partidos, sin ponderar)
        'home_last5_wins': sum((ultimos_partidos_home['HomeTeam'] == home_team) & (ultimos_partidos_home['FTR'] == 'H') |
                              (ultimos_partidos_home['AwayTeam'] == home_team) & (ultimos_partidos_home['FTR'] == 'A')),
        'home_last5_draws': sum(ultimos_partidos_home['FTR'] == 'D'),
        
        'away_last5_wins': sum((ultimos_partidos_away['HomeTeam'] == away_team) & (ultimos_partidos_away['FTR'] == 'H') |
                              (ultimos_partidos_away['AwayTeam'] == away_team) & (ultimos_partidos_away['FTR'] == 'A')),
        'away_last5_draws': sum(ultimos_partidos_away['FTR'] == 'D')
    }
    
    # Añadir losses de últimos 5 partidos
    features['home_last5_losses'] = 5 - (features['home_last5_wins'] + features['home_last5_draws'])
    features['away_last5_losses'] = 5 - (features['away_last5_wins'] + features['away_last5_draws'])
    
    return pd.DataFrame([features])


def train_model(df, home_team, away_team):
    """
    Entrena el modelo usando solo los partidos del equipo local y visitante especificados.
    
    Args:
        df: DataFrame con los datos históricos
        home_team: Equipo local
        away_team: Equipo visitante
    """
    # Crear listas para almacenar features y resultados
    features_list = []
    results = []

    # Ordenar las temporadas
    temporadas = sorted(df['Temporada'].unique())
    
    # Filtrar solo partidos donde participen los equipos de interés
    df_equipos = df[
        ((df['HomeTeam'] == home_team) | (df['AwayTeam'] == home_team) |
         (df['HomeTeam'] == away_team) | (df['AwayTeam'] == away_team))
    ]
    
    # Para cada partido en el dataset, excluyendo la primera temporada
    for idx, partido in df_equipos[df_equipos['Temporada'] != temporadas[0]].iterrows():
        temporada_actual = partido['Temporada']
        
        # Obtener datos de todas las temporadas anteriores
        temporadas_anteriores = [t for t in temporadas if t < temporada_actual]
        if not temporadas_anteriores:
            continue
            
        # Obtener datos hasta la temporada actual, manteniedo solo partidos de los equipos
        df_hasta_temporada = df_equipos[df_equipos['Temporada'].isin(temporadas_anteriores)]
        
        try:
            # Preparar features usando los datos históricos
            features = prepare_data_for_model(
                df_hasta_temporada,
                partido['HomeTeam'],
                partido['AwayTeam']
            )
            
            # Solo añadimos si tenemos suficientes datos
            if features is not None and not features.empty:
                features_list.append(features)
                # Convertir resultado (0: Away, 1: Draw, 2: Home)
                result = 0 if partido['FTR'] == 'A' else (1 if partido['FTR'] == 'D' else 2)
                results.append(result)
                
        except Exception as e:
            print(f"Error procesando partido de temporada {temporada_actual}: {e}")
            continue
    
    if not features_list:
        raise ValueError("No se pudieron generar suficientes datos para entrenar el modelo")
    
    # Concatenar todos los features
    X = pd.concat(features_list, ignore_index=True)
    y = np.array(results)
    
    print(f"\nEntrenando modelo con {len(X)} partidos")
    print(f"Usando datos desde temporada {temporadas[0]} hasta {temporadas[-1]}")
    print(f"Solo para partidos que involucran a {home_team} y {away_team}")
    
    # Dividir en train y test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Escalar características
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Entrenar modelo
    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=20,
        min_samples_split=8,
        min_samples_leaf=4,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Evaluar el modelo
    train_score = model.score(X_train_scaled, y_train)
    test_score = model.score(X_test_scaled, y_test)
    
    print(f"Score en entrenamiento: {train_score:.3f}")
    print(f"Score en test: {test_score:.3f}")
    
    # Mostrar importancia de características
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nCaracterísticas más importantes:")
    print(feature_importance.head(10))
    
    return model, scaler, train_score, test_score

def prepare_new_match_data(df, home_team, away_team, match_date):
    """
    Prepara los datos para un nuevo partido
    """
    # Convertir fecha a datetime si es string
    if isinstance(match_date, str):
        match_date = pd.to_datetime(match_date)
        
    # Crear un DataFrame con un solo partido
    new_match = pd.DataFrame({
        'Date': [match_date],
        'HomeTeam': [home_team],
        'AwayTeam': [away_team],
        'Temporada': [str(match_date.year)],
        'FTR': ['H']  # Valor temporal, no afecta la predicción
    })
    
    # Concatenar con datos históricos
    df_with_new = pd.concat([df, new_match], ignore_index=True)
    
    # Preparar datos
    X, _ = prepare_data_for_model(df_with_new)
    
    # Devolver solo la última fila (el nuevo partido)
    return X[-1:] if len(X) > 0 else None

def predict_match(df, home_team, away_team):
    """
    Entrena el modelo para los equipos específicos y predice el resultado del partido.
    
    Args:
        df: DataFrame con los datos históricos
        home_team: Equipo local
        away_team: Equipo visitante
        
    Returns:
        dict: Probabilidades y resultado más probable
    """
    try:
        # Entrenar el modelo específico para estos equipos
        model, scaler, train_score, test_score = train_model(df, home_team, away_team)
        
        # Obtener las características para el partido actual
        current_features = prepare_data_for_model(df, home_team, away_team)
        
        if current_features is None:
            raise ValueError("No se pudieron preparar las características del partido")
        
        # Escalar las características
        features_scaled = scaler.transform(current_features)
        
        # Obtener probabilidades
        probabilities = model.predict_proba(features_scaled)[0]
        
        # Encontrar el resultado más probable
        resultado_idx = probabilities.argmax()
        resultados = ['Victoria Visitante', 'Empate', 'Victoria Local']
        resultado_probable = resultados[resultado_idx]
        
        # Crear diccionario con los resultados
        prediccion = {
            'probabilidades': {
                'victoria_local': f"{probabilities[2]*100:.1f}%",
                'empate': f"{probabilities[1]*100:.1f}%",
                'victoria_visitante': f"{probabilities[0]*100:.1f}%"
            },
            'resultado_mas_probable': resultado_probable,
            'confianza_prediccion': f"{probabilities[resultado_idx]*100:.1f}%",
            'metricas_modelo': {
                'score_entrenamiento': f"{train_score:.3f}",
                'score_test': f"{test_score:.3f}"
            }
        }
        
        # Imprimir resultados de forma legible
        print(f"\nPredicción para {home_team} vs {away_team}:")
        print(f"Victoria {home_team}: {prediccion['probabilidades']['victoria_local']}")
        print(f"Empate: {prediccion['probabilidades']['empate']}")
        print(f"Victoria {away_team}: {prediccion['probabilidades']['victoria_visitante']}")
        
        return prediccion
        
    except Exception as e:
        print(f"Error al realizar la predicción: {e}")
        return None

    
