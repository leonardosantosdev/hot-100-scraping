from spotify_auth import spotify_auth
from hot_100_scraping import Hot100Scraping

user_id = "<your spotify user_id>"
client_id = "<your spotify client_id>"
client_secret = "<your spotify cliente_secret>"
hot_100_url = "https://www.billboard.com/charts/hot-100/"

sp = spotify_auth(user_id, client_id, client_secret)
scraping = Hot100Scraping(user_id, hot_100_url, sp)

scraping.create_hot_100_playist()
