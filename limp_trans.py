import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import datetime

df = pd.read_csv('spotify-2023.csv', encoding="ISO-8859-1")

#Eliminamos una fila con datos erróneos
index_to_drop = df.loc[~df['streams'].str.isnumeric()].index
df = df.drop(index_to_drop)
#Convertimos a numerico la columna 'streams'
df['streams'] = pd.to_numeric(df['streams'], errors='coerce')

#Añadimos una columna fecha al dataframe
df["fecha"] = df.apply(lambda row: datetime.datetime(row["released_year"], row["released_month"], row["released_day"]), axis=1)

# Configura las credenciales del cliente
# sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=xxx...x,
#                                                          client_secret=xxx...x))

def get_album_cover(track_name):
    # Busca la canción en la API de Spotify
    results = sp.search(q='track:' + track_name, type='track')
    
    # Obtiene la URL de la imagen de la portada del primer resultado
    try:
        url = results['tracks']['items'][0]['album']['images'][0]['url']
    except IndexError:
        url = None
    
    # Devuelve el código HTML de la imagen
    return f'<img src="{url}">' if url else None

# Agrega la nueva columna al DataFrame
df['album_image'] = df['track_name'].apply(get_album_cover)

# Exportar el DataFrame a un archivo CSV
df.to_csv('spotify_updated.csv', index=False, encoding='ISO-8859-1')