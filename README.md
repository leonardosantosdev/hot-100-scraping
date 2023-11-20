# Billboard Hot 100 Scraping

This project combines web scraping from the Billboard Hot 100 and Spotify API integration to create playlists of the top 100 songs from the Billboard Hot 100 chart.

### Spotify Authentication
Billboard Hot 100 Scraping utilizes the Spotipy module for Spotify API authentication. To connect to the Spotify API, the project uses the client credentials flow, obtaining an access token for making requests to the Spotify API. This authentication process is handled in `spotify_auth.py`.

### Web Scraping Process
The web scraping process involves extracting song information from the Billboard Hot 100 website. Billboard Hot 100 Scraping uses the requests library to make HTTP requests, BeautifulSoup for HTML parsing, and difflib for string similarity comparison. This step is under `hot_100_scraping.py`, with a class containing all functions needed.

### Usage
Before running the script, make sure you have Python installed on your machine. You can download it from [here](https://www.python.org/downloads/). Use a Python version compatible with the project, e.g., Python 3.7 or higher.

First, clone the repository to your machine:

    $ git clone https://github.com/leonardosantosdev/hot-100-scraping


Under root directory, install the needed modules:

    $ pip install -r requirements.txt

Inside /scripts, change `main.py` with your Spotify credentials.

```python 
from spotify_auth import spotify_auth
from hot_100_scraping import Hot100Scraping

user_id = "<your spotify user_id>"
client_id = "<your spotify client_id>"
client_secret = "<your spotify cliente_secret>"
genius_url = "https://www.billboard.com/charts/hot-100/"

sp = spotify_auth(user_id, client_id, client_secret)
scraping = Hot100Scraping(user_id, hot_100_url, sp)

scraping.create_hot_100_playist()

```

Simply run `main.py` and the playlist will be created with the samples in your Spotify account.