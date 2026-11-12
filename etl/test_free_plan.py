import os 
import sys
import requests
import json
from dotenv import load_dotenv
from pathlib import Path
from datetime import date

BASE_URL = "https://v3.football.api-sports.io"
BARCELONA_TEAM_ID = 529
today = date.today().isoformat()

load_dotenv()
api_key = os.getenv("API_FOOTBALL_KEY")
print("Clé trouvée" if api_key else "Clé absente")

response = requests.get(
    f"{BASE_URL}/fixtures/statistics",
    headers = {"x-apisports-key": api_key},
    params = {"fixture": 1208494},
    timeout = 15,
)

api_data = response.json()

Path("data/raw").mkdir(parents=True, exist_ok=True)
with open(f'data/raw/matchstats_1208494_{today}.json', "w", encoding="utf-8") as fichier:
    json.dump(api_data, fichier, indent=2, ensure_ascii=False)

print(api_data["errors"])
print(api_data["results"])

if api_data["errors"]:
    sys.exit(f"L'API signale une erreur : {api_data['errors']}")