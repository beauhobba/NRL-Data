# script to run the scraper
from match_data_select import match_data_select
from match_data_detailed_select import match_data_detailed_select
from player_data_select import player_data_select
import os

SELECTION_TYPE = 'HOSTPLUS'  # NRL, NRLW, HOSTPLUST, KNOCKON
SELECT_YEARS = [2024, 2023]
SELECT_ROUNDS = [1, 1]


for year, rounds in zip(SELECT_YEARS, SELECT_ROUNDS):
    print(f"Starting: {year} {rounds}")
    directory_path = f"../data/{SELECTION_TYPE}/{year}/"
    os.makedirs(directory_path, exist_ok=True)
    
    match_data_select(year, rounds, SELECTION_TYPE)
    match_data_detailed_select(year, rounds, SELECTION_TYPE)
    player_data_select(year, rounds, SELECTION_TYPE)