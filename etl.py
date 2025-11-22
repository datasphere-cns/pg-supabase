import os
import time
import requests
from supabase import create_client
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

# ========================
# LOGGING
# ========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger()

# ========================
# CREDENCIALES
# ========================
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")

if not all([SUPABASE_URL, SUPABASE_KEY, API_FOOTBALL_KEY]):
    log.critical("Faltan variables de entorno")
    raise SystemExit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
headers = {
    "x-rapidapi-key": API_FOOTBALL_KEY,
    "x-rapidapi-host": "v3.football.api-sports.io"
}

TEAMS = {40: "Liverpool", 33: "Manchester United", 42: "Arsenal"}
LEAGUE_ID = 39
SEASONS = [2021, 2022, 2023]

# ========================
# FUNCIÓN SEGURA
# ========================
@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10))
def get_team_stats(team_id: int, season: int):
    resp = requests.get(
        "https://v3.football.api-sports.io/teams/statistics",
        headers=headers,
        params={"team": team_id, "league": LEAGUE_ID, "season": season},
        timeout=15
    )
    resp.raise_for_status()
    data = resp.json().get("response")
    if not data:
        return None
    return data[0] if isinstance(data, list) else data

# ========================
# PAYLOAD
# ========================
def build_payload(data, team_id, team_name, season):
    f = data["fixtures"]["played"]["total"]
    gf = data["goals"]["for"]["total"]["total"] or 0
    ga = data["goals"]["against"]["total"]["total"] or 0

    # Tarjetas amarillas y rojas con fallback brutal
    yellow_cards = 0
    red_cards = 0
    if "cards" in data and data["cards"]:
        yellow_dict = data["cards"].get("yellow", {})
        red_dict = data["cards"].get("red", {})
        for v in yellow_dict.values():
            if v and isinstance(v, dict):
                yellow_cards += v.get("total") or 0
        for v in red_dict.values():
            if v and isinstance(v, dict):
                red_cards += v.get("total") or 0

    return {
        "team_id": team_id,
        "team_name": team_name,
        "league_id": LEAGUE_ID,
        "league_name": "Premier League",
        "season": season,
        "fixtures_played": f,
        "fixtures_wins": data["fixtures"]["wins"]["total"],
        "fixtures_draws": data["fixtures"]["draws"]["total"],
        "fixtures_loses": data["fixtures"]["loses"]["total"],
        "goals_for": gf,
        "goals_against": ga,
        "goal_difference": gf - ga,
        "goals_per_match": round(gf / f, 2) if f else 0,
        "clean_sheets": data.get("clean_sheet", {}).get("total", 0),
        "failed_to_score": data.get("failed_to_score", {}).get("total", 0),
        "cards_yellow": yellow_cards,
        "cards_red": red_cards,
        "form": data.get("form"),
    }

# ========================
# MAIN
# ========================
def main():
    log.info("INICIANDO ETL BIG 3 PREMIER LEAGUE (2021-2023)")
    guardadas = 0

    for team_id, team_name in TEAMS.items():
        for season in SEASONS:
            log.info(f"{team_name} {season}/{season+1} → descargando...")
            try:
                data = get_team_stats(team_id, season)
                if not data:
                    log.warning(f"{team_name} {season}/{season+1} → sin datos")
                    time.sleep(1.1)
                    continue

                payload = build_payload(data, team_id, team_name, season)
                supabase.table("team_stats").upsert(payload).execute()
                guardadas += 1
                log.info(f"{team_name} {season}/{season+1} → OK")

            except Exception as e:
                log.error(f"{team_name} {season}/{season+1} → ERROR: {e}")

            time.sleep(1.1)

    log.info(f"ETL COMPLETADO {guardadas}/9 registros guardados")
    log.info("https://supabase.com/dashboard/project/mjbadhagxiamihxtuiso/editor/tables/public/team_stats")

if __name__ == "__main__":
    main()
