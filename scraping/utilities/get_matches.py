# import json
# import pandas as pd 
# import numpy as np 

# teams = ["Broncos", "Roosters", "Wests Tigers", "Rabbitohs", "Storm", "Eels", "Raiders", "Knights", "Dragons", "Sea Eagles", "Panthers", "Sharks", "Bulldogs", "Dolphins", "Titans", "Cowboys", "Warriors"]
# variables =["Year", "Win", "Defense", "Attack", "Margin", "Home", "Versus",  "Round"]
# years =  [2023]


# def get_matches(year='2023'):
#     # Initialize an empty dictionary to store data for each year
#     years_arr = {}

#     with open('../../data/nrl_data_multi_years_2023.json', 'r') as file:
#         data = json.load(file)
#         data = data['NRL']
#         for year in years:
#             years_arr[year] = data[years.index(year)][str(year)]
#     # Create a DataFrame with columns representing combinations of team and variable names
#     df = pd.DataFrame(columns=[f"{team} {variable}" for team in teams for variable in variables])

#     # Iterate over each round (assuming 26 rounds)
#     for round in range(0, 26):
#         try:
#             # Extract data for the current round
#             round_data = years_arr[year][round][str(round+1)]
            
#             # Create an empty feature array 
#             round_store = np.zeros([len(teams)*len(variables)], dtype=int)
#             home_teams = []
#             away_teams = [] 
            
#             # Iterate over each game in the round data
#             for game in round_data:
#                 # Extract information about the game
#                 h_team = game['Home']
#                 h_score = int(game['Home_Score'])
#                 a_team = game['Away']
#                 a_score = int(game['Away_Score'])
#                 round_teams.append(h_team)
#                 round_teams.append(a_team)
#             print(round_teams)
                
#         except:
#             pass
    
# get_matches()