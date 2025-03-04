"""
Optimized Web Scraper for NRL Player Statistics (Fast Execution, Saves Per Round, Includes Year)
"""

from bs4 import BeautifulSoup
import json
import sys
import os
from utilities.set_up_driver import set_up_driver

sys.path.append("..")
import ENVIRONMENT_VARIABLES as EV

# List of variables for data extraction
variables = ["Year", "Win", "Versus", "Round"]

selected_year = 2024
selected_rounds = 27

years_overall = [selected_year]
years = [selected_year]

# Define file path for player statistics
player_stats_file = f"../data/player_statistics_{selected_year}.json"

# **RESET FILE EACH RUN**: Overwrite file with an empty structure
player_stats = {"PlayerStats": [{str(selected_year): []}]}

# Load NRL match data
with open(f"../data/nrl_data_{selected_year}.json", "r") as file:
    data = json.load(file)
    data = data["NRL"]

# Store match data for the selected year
years_arr = {year: data[years_overall.index(year)][str(year)] for year in years}

# **Start WebDriver once and reuse it**
driver = set_up_driver()

for year in years:
    try:
        for round in range(selected_rounds):
            round_data = years_arr[year][round][str(round + 1)]
            round_results = []  # Store all matches for this round

            for game in round_data:
                h_team, a_team = [game[x].replace(" ", "-") for x in ["Home", "Away"]]
                match_key = f"{year}-{round+1}-{h_team}-v-{a_team}"

                url = f"{EV.NRL_WEBSITE}{year}/round-{round+1}/{h_team}-v-{a_team}/"
                print(f"Fetching: {url}")

                # Use existing WebDriver (runs headless for speed)
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, "html.parser")

                # Extract player data
                rows = soup.find_all("tr", class_="table-tbody__tr")
                players_info = []

                for row in rows:
                    player_info = {}
                    player_name_elem = row.find("a", class_="table__content-link")

                    if player_name_elem:
                        player_info["Name"] = player_name_elem.get_text(strip=True, separator=" ")

                    statistics = row.find_all("td", class_="table__cell table-tbody__td")

                    for i, label in enumerate(EV.PLAYER_LABELS):
                        player_info[label] = statistics[i].get_text(strip=True) if i < len(statistics) else "na"

                    players_info.append(player_info)

                # Store match data for this round
                round_results.append({match_key: players_info})
                print(f"Processed match: {match_key}")

            # **Add round data under the correct year**
            year_index = 0  # Since there's only one year in PlayerStats list
            player_stats["PlayerStats"][year_index][str(year)].append({str(round): round_results})

            # **Write to file immediately after each round**
            with open(player_stats_file, "w") as file:
                json.dump(player_stats, file, indent=4)

            print(f"✅ Round {round+1} data saved.")

    except Exception as ex:
        print(f"Error: {ex}")

# **Close WebDriver after all matches are processed**
driver.quit()

print(f"Final player statistics saved to {player_stats_file}")
