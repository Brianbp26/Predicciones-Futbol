# Predicciones-Futbol
Para crear una web de predicciones de fútbol, decidimos usar streamlit, que es una librería de python que facilita mucho el desarrollo web de forma que podíamos centrarnos tanto en el desarrollo web como en las predicciones al mismo nivel.

Para que el proyecto no se quedara solo como un proyecto en local, vimos que streamlit daba soporte a los usuarios puediendo usar su plataforma para publicar nuestra web. Para ello, creamos un repositorio de github (https://github.com/Brianbp26/Predicciones-Futbol/blob/main/app.py) de forma que enlazando github con streamlit podemos crear la web.

Sin embargo, nos parecía más óptimo explicar el proyecto con ipynbs, de forma que hemos creado una carpeta aparte con los archivos adaptados a ipynb de forma que vamos explicando todo.

La estrucutra de los archivos es la siguiente: 
    archivos: Carpeta donde se almacenan todos los archivos utilizados (fuente: https://www.football-data.co.uk/data.php)
    app.ipynb: Archivo principal de la arquitectura de la web.
    datos.ipynb: Archivo donde están definidas todas las funciones utilizadas en el app.ipynb.
    main.ipynb: Archivo de las predicciones.

Para el desarrollo de la web, también hicimos uso de la API de football-data para ciertas cosas commo obtener la tabla de clasificación o la jornada actual.

El sitio web de la página es: https://predicciones-futbol-cdia.streamlit.app/

DISCLAIMER: La página web tarda aproximadamente entre 2-3min en cargar la prediccion de cada partido debido a:
    Tiempo de ejecución de la predicción.
    Servidor de streamlit no muy potente.
    Uso gratuito de la API de football-data de forma que va un poco lento.

Mantenimiento de la web: Cada 5 días se actualizará manualmente la fecha que tenemos definida para cargar los partidos de la jornada(datos.ipynb), y los csvs de la última temporada de cada liga, de forma que se pueda seguir utilizando la web, y teniendo la mayor cantidad de datos posibles para hacer las predicciones.
