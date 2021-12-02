from bs4 import BeautifulSoup
import requests, json
from tqdm import tqdm
from plexapi.server import PlexServer
from plexapi.myplex import MyPlexAccount, MyPlexUser, MyPlexAccount
from plexapi.library import Library

email = "SET_EMAIL_HERE"




data = open('plex.json','r').read().split("\n")
data = list(filter(None, data))
servers = []
for x in data:
    servers.append(json.loads(x)['ip_str'])


for server in tqdm(servers):
    try:
        page = requests.get(f'http://{server}:8181/settings')
        soup = BeautifulSoup(page.content, 'html.parser')
        token = soup.find("input", {"id": "pms_token"})["value"]

        plex = PlexServer(f'http://{server}:32400', token)
        plex.myPlexAccount().inviteFriend(email, plex, plex.library.sections())
    except:
        print(f'Failed to access {server}')
    else:
        print(f'Successfully accessed {server}')
