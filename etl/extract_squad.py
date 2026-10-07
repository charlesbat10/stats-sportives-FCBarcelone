import os 

import requests
from dotenv import load_dotenv

BASE_URL = "https://v3.football.api-sports.io"
BARCELONA_TEAM_ID = 529

load_dotenv()
api_key = os.getenv("API_FOOTBALL_KEY")
print("Clé trouvée" if api_key else "Clé absente")

response = requests.get(
    f"{BASE_URL}/players/squads",
    headers = {"x-apisports-key": api_key},
    params = {"team": BARCELONA_TEAM_ID},
    timeout = 15,
)
print(response.status_code)
print(response.json()["response"][0]["team"]["name"])