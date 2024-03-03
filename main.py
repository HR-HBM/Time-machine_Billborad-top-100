import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth




#scraping Billboard 100

date = input("Which year do want to travel to? Type the date in this format YYYY-MM-DD: ")

billboard_URL = "https://www.billboard.com/charts/hot-100/"+ date + "/"

response = requests.get(billboard_URL)
website_html = response.text
soup = BeautifulSoup(website_html, "html.parser")

h3 = soup.select("li ul li h3")
song_titles = []

for song in h3:
    title = song.getText().strip()
    song_titles.append(title)

# print(song_titles)

# Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        #enter client id and client secret
        client_id="",
        client_secret="",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)


#searching spotify songs by title

song_uris = []
year = date.split("-")[0]
for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# creating a new private playlist in spotify

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

#adding songs found into new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)