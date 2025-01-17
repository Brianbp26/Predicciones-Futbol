import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, cross_val_score
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
    ultima_temporada = df['Temporada'].max()
    partidos_temporada = df[df['Temporada'] == ultima_temporada]

    if len(partidos_temporada) == 0:
        return 10

    equipos_stats_home = partidos_temporada.groupby('HomeTeam').agg(
        puntos_home=('FTR', lambda x: (x == 'H').sum() * 3 + (x == 'D').sum()),
        gf_home=('FTHG', 'sum'),
        gc_home=('FTAG', 'sum')
    ).reset_index()

    equipos_stats_away = partidos_temporada.groupby('AwayTeam').agg(
        puntos_away=('FTR', lambda x: (x == 'A').sum() * 3 + (x == 'D').sum()),
        gf_away=('FTAG', 'sum'),
        gc_away=('FTHG', 'sum')
    ).reset_index()

    equipos_stats = pd.merge(equipos_stats_home, equipos_stats_away, left_on='HomeTeam', right_on='AwayTeam', how='outer').fillna(0)
    equipos_stats['equipo'] = equipos_stats['HomeTeam'].combine_first(equipos_stats['AwayTeam'])
    equipos_stats['puntos'] = equipos_stats['puntos_home'] + equipos_stats['puntos_away']
    equipos_stats['gf'] = equipos_stats['gf_home'] + equipos_stats['gf_away']
    equipos_stats['gc'] = equipos_stats['gc_home'] + equipos_stats['gc_away']

    equipos_stats['dif_goles'] = equipos_stats['gf'] - equipos_stats['gc']
    equipos_stats = equipos_stats.sort_values(by=['puntos', 'dif_goles', 'gf'], ascending=False).reset_index(drop=True)

    try:
        return equipos_stats[equipos_stats['equipo'] == equipo].index[0] + 1
    except IndexError:
        return 10

def prepare_data_for_model(df, home_team, away_team):
    """
    Prepara los datos para el modelo usando todas las temporadas con ponderación.
    """
    #Como teníamos varios formatos en los csvs, definimos los formatos para poder operar con todos
    date_formats = ["%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d"]
    for fmt in date_formats:
        try:
            df.loc[:, 'Date'] = pd.to_datetime(df['Date'], format=fmt, errors='coerce')  
            break
        except ValueError:
            continue
    else:
        # Si todos los formatos fallan, intentamos con dayfirst=True
        df.loc[:, 'Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')

    #Para trabajar con un dataframe independiente, creamos una copia
    df = df.dropna(subset=['Date']).copy() 
    df = df.sort_values('Date').copy()     


    temporadas = sorted(df['Temporada'].unique())
    num_temporadas = len(temporadas)

    # Creamos un  diccionario de pesos para cada temporada, con mayor peso para la última temporada
    pesos_temporadas = {temp: 1 - (0.8 * (num_temporadas - i - 1) / (num_temporadas - 1)) 
                        for i, temp in enumerate(temporadas)}

    # Incrementamos el peso de la última temporada ya que la consideramos más importante
    if temporadas:
        pesos_temporadas[temporadas[-1]] *= 1.5

    #Definimos las variables que queremos analizar
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
        'h2h_draws': 0,
        'home_win_streak': 0,
        'away_win_streak': 0
    }

    # Calculamos estas estadísticas para cada temporada ponderando
    for temporada in temporadas:
        peso = pesos_temporadas[temporada]
        df_temp = df[df['Temporada'] == temporada].copy() 

        # Manejamos las divisiones por 0 al calcular promedios (equipos con una unica temporadd)
        try:
            # Partidos como local del equipo local
            home_local = df_temp[df_temp['HomeTeam'] == home_team].copy()
            stats['home_wins'] += peso * sum(home_local['FTR'] == 'H')
            stats['home_draws'] += peso * sum(home_local['FTR'] == 'D')
            stats['home_losses'] += peso * sum(home_local['FTR'] == 'A')
            stats['home_goals_scored'] += peso * home_local['FTHG'].mean() if len(home_local) > 0 else 0
            stats['home_goals_conceded'] += peso * home_local['FTAG'].mean() if len(home_local) > 0 else 0

            # Partidos como visitante del equipo visitante
            away_visit = df_temp[df_temp['AwayTeam'] == away_team].copy()
            stats['away_wins'] += peso * sum(away_visit['FTR'] == 'A')
            stats['away_draws'] += peso * sum(away_visit['FTR'] == 'D')
            stats['away_losses'] += peso * sum(away_visit['FTR'] == 'H')
            stats['away_goals_scored'] += peso * away_visit['FTAG'].mean() if len(away_visit) > 0 else 0
            stats['away_goals_conceded'] += peso * away_visit['FTHG'].mean() if len(away_visit) > 0 else 0

            # Enfrentamientos directos
            h2h_matches = df_temp[
                ((df_temp['HomeTeam'] == home_team) & (df_temp['AwayTeam'] == away_team)) |
                ((df_temp['HomeTeam'] == away_team) & (df_temp['AwayTeam'] == home_team))
            ].copy()

            if len(h2h_matches) > 0:
                stats['h2h_matches'] += peso * len(h2h_matches)
                stats['h2h_home_wins'] += peso * sum((h2h_matches['HomeTeam'] == home_team) & (h2h_matches['FTR'] == 'H'))
                stats['h2h_away_wins'] += peso * sum((h2h_matches['HomeTeam'] == away_team) & (h2h_matches['FTR'] == 'H'))
                stats['h2h_draws'] += peso * sum(h2h_matches['FTR'] == 'D')

        except ZeroDivisionError:
            continue

    #Estados de forma (ultimos 5 partidos)
    ultimos_partidos_home = df[
        (df['HomeTeam'] == home_team) | 
        (df['AwayTeam'] == home_team)
    ].tail(5).copy()

    ultimos_partidos_away = df[
        (df['HomeTeam'] == away_team) | 
        (df['AwayTeam'] == away_team)
    ].tail(5).copy()

    # Calculamos la racha de victorias para potenciar al equipo
    stats['home_win_streak'] = sum((ultimos_partidos_home['HomeTeam'] == home_team) & (ultimos_partidos_home['FTR'] == 'H') |
                                   (ultimos_partidos_home['AwayTeam'] == home_team) & (ultimos_partidos_home['FTR'] == 'A'))
    stats['away_win_streak'] = sum((ultimos_partidos_away['HomeTeam'] == away_team) & (ultimos_partidos_away['FTR'] == 'H') |
                                   (ultimos_partidos_away['AwayTeam'] == away_team) & (ultimos_partidos_away['FTR'] == 'A'))

    # Definimos lo que queremos devolver
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
        
        # Forma reciente
        'home_last5_wins': sum((ultimos_partidos_home['HomeTeam'] == home_team) & (ultimos_partidos_home['FTR'] == 'H') |
                              (ultimos_partidos_home['AwayTeam'] == home_team) & (ultimos_partidos_home['FTR'] == 'A')),
        'home_last5_draws': sum(ultimos_partidos_home['FTR'] == 'D'),
        
        'away_last5_wins': sum((ultimos_partidos_away['HomeTeam'] == away_team) & (ultimos_partidos_away['FTR'] == 'H') |
                              (ultimos_partidos_away['AwayTeam'] == away_team) & (ultimos_partidos_away['FTR'] == 'A')),
        'away_last5_draws': sum(ultimos_partidos_away['FTR'] == 'D'),

        # Racha de victorias
        'home_win_streak': stats['home_win_streak'],
        'away_win_streak': stats['away_win_streak']
    }

    return pd.DataFrame([features])

def train_model(df, home_team, away_team):
    """
    Entrena el modelo usando solo los partidos del equipo local y visitante especificados.
    
    Args:
        df: DataFrame con los datos históricos
        home_team: Equipo local
        away_team: Equipo visitante
    """
    # Creamos listas para almacenar los features y los resultados
    features_list = []
    results = []

    # Ordenamos las temporadas
    temporadas = sorted(df['Temporada'].unique())
    
    # Filtramos solo partidos donde participen los equipos de interés
    df_equipos = df[
        ((df['HomeTeam'] == home_team) | (df['AwayTeam'] == home_team) |
         (df['HomeTeam'] == away_team) | (df['AwayTeam'] == away_team))
    ]
    
    # Excluimos la primera temporada, ya que esta no tiene temporadas anteriores de las que "aprender"
    for idx, partido in df_equipos[df_equipos['Temporada'] != temporadas[0]].iterrows():
        temporada_actual = partido['Temporada']
        
        # Obtenemos los datos de todas las temporadas anteriores
        temporadas_anteriores = [t for t in temporadas if t < temporada_actual]
        if not temporadas_anteriores:
            continue
            
        # Obtenemos datos hasta la temporada actual, manteniedo solo partidos de los equipos
        df_hasta_temporada = df_equipos[df_equipos['Temporada'].isin(temporadas_anteriores)]
        
        try:
            # Preparamos features usando los datos históricos
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
            continue
    
    if not features_list:
        raise ValueError("No se pudieron generar suficientes datos para entrenar el modelo")
    
    # Concatenamos todos los features
    X = pd.concat(features_list, ignore_index=True)
    y = np.array(results)
    
    # Dividimos para entrenar el modelo
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Escalamos características para que se pueda tomar todas por igual
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Definimos el modelo y los hiperparámetros a optimizar
    model = RandomForestClassifier(random_state=42)
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'class_weight': ['balanced']
    }
    
    # Realizamos búsqueda de hiperparámetros para mejorar el modelo
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, n_jobs=-1, scoring='accuracy')
    grid_search.fit(X_train_scaled, y_train)
    
    best_model = grid_search.best_estimator_
    
    # Evaluamos el modelo
    train_score = best_model.score(X_train_scaled, y_train)
    test_score = best_model.score(X_test_scaled, y_test)
    
    return best_model, scaler, train_score, test_score
    

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
        # Entrenamos el modelo  para estos equipos
        model, scaler, _, _ = train_model(df, home_team, away_team)
        
        # Obtenemos las características para el partido actual
        current_features = prepare_data_for_model(df, home_team, away_team)
        
        if current_features is None:
            raise ValueError("No se pudieron preparar las características del partido")
        
        # Escalamos las características
        features_scaled = scaler.transform(current_features)
        
        # Obtenemos probabilidades
        probabilities = model.predict_proba(features_scaled)[0]
        
        # Creamos diccionario con los resultados
        prediccion = {
                'victoria_local': f"{probabilities[2]*100:.1f}%",
                'empate': f"{probabilities[1]*100:.1f}%",
                'victoria_visitante': f"{probabilities[0]*100:.1f}%"
            }
        return prediccion
        
    except Exception as e:
        print(f"Error al realizar la predicción: {e}")
        return None
    
        
def predict_match_score(df, home_team, away_team):
    """
    Predice el resultado y marcador del partido usando modelo entrenado y estadísticas.
    
    Args:
        df: DataFrame con histórico de partidos
        home_team: Equipo local
        away_team: Equipo visitante
    
    Returns:
        tuple: (goles_local, goles_visitante)
    """
    try:
        # Entrenamos el modelo para predecir el resultado
        model, scaler, _, _ = train_model(df, home_team, away_team)
        
        # Obtenemos características para el partido actual
        current_features = prepare_data_for_model(df, home_team, away_team)
        
        if current_features is None:
            raise ValueError("No se pudieron preparar las características del partido")
        
        # Escalamos características
        features_scaled = scaler.transform(current_features)
        
        # Obtenemos probabilidades del modelo
        probabilities = model.predict_proba(features_scaled)[0]
        
        # Obtenemos resultado más probable
        resultado_idx = probabilities.argmax()
        resultados = ['Victoria Visitante', 'Empate', 'Victoria Local']
        resultado_probable = resultados[resultado_idx]
        
        # Calculamos goles esperados usando estadísticas recientes
        recent_matches = df.tail(10*20)
        
        # Estadísticas equipo local
        home_recent = recent_matches[recent_matches['HomeTeam'] == home_team]['FTHG'].mean()
        home_historical = df[df['HomeTeam'] == home_team]['FTHG'].mean()
        
        # Estadísticas equipo visitante
        away_recent = recent_matches[recent_matches['AwayTeam'] == away_team]['FTAG'].mean()
        away_historical = df[df['AwayTeam'] == away_team]['FTAG'].mean()
        
        # Manejamos los valores NaN
        home_recent = home_recent if not pd.isna(home_recent) else home_historical
        away_recent = away_recent if not pd.isna(away_recent) else away_historical
        
        # Calculamos goles esperados (66% forma reciente, 33% histórico)
        home_expected = (0.66 * home_recent + 0.33 * home_historical)
        away_expected = (0.66 * away_recent + 0.33 * away_historical)
        
        # Predecimos marcador según resultado predicho por el modelo
        if resultado_probable == 'Victoria Local':
            home_score = round(max(home_expected, away_expected + 1))
            away_score = round(min(away_expected, home_score - 1))
        elif resultado_probable == 'Victoria Visitante':
            away_score = round(max(away_expected, home_expected + 1))
            home_score = round(min(home_expected, away_score - 1))
        else:  # Empate
            avg_goals = (home_expected + away_expected) / 2
            home_score = away_score = max(1, round(avg_goals))
            if home_score > 3:
                home_score = away_score = 2
        
        return home_score, away_score
        
    except Exception as e:
        print(f"Error al realizar la predicción: {e}")
        return None, None
