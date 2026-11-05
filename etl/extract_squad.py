import os 
import sys
import requests
import json
from dotenv import load_dotenv
from pathlib import Path
from datetime import date

BASE_URL = "https://v3.football.api-sports.io"
BARCELONA_TEAM_ID = 529
QUOTA_SAFETY = 10
today = date.today().isoformat()

def stop_quota_if_almost_exhausted(daily_remaining):
    if(daily_remaining<=QUOTA_SAFETY):
        sys.exit(f"Il ne reste plus que {daily_remaining} requêtes aujourd'hui. Arrêt du script")

def print_squad(players):
    for player in players :
        print(f"numéro : {player['number']}  nom : {player['name']} position: {player['position']}")
    print(len(players))
    
load_dotenv()
api_key = os.getenv("API_FOOTBALL_KEY")
print("Clé trouvée" if api_key else "Clé absente")

response = requests.get(
    f"{BASE_URL}/players/squads",
    headers = {"x-apisports-key": api_key},
    params = {"team": BARCELONA_TEAM_ID},
    timeout = 15,
)

api_data = response.json()
if api_data["errors"]:
    sys.exit(f"L'API signale une erreur : {api_data['errors']}")

Path("data/raw").mkdir(parents=True, exist_ok=True)
with open(f'data/raw/squad_{today}.json', "w", encoding="utf-8") as fichier:
    json.dump(api_data, fichier, indent=2, ensure_ascii=False)

daily_remaining = int(response.headers["x-ratelimit-requests-remaining"])
stop_quota_if_almost_exhausted(daily_remaining)
daily_limit = int(response.headers["x-ratelimit-requests-limit"])
minute_remaining = int(response.headers["x-ratelimit-remaining"])
print(f"Quota : {daily_remaining} requêtes restantes sur {daily_limit} aujourd'hui")
print(f"Requêtes restantes cette minute : {minute_remaining}")
print(api_data["response"][0]["team"]["name"])
players = api_data["response"][0]["players"]
print_squad(players)