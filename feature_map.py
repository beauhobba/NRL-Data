# import pandas as pd 
# import json
# import numpy as np

# teams = ["Broncos", "Roosters", "Wests Tigers", "Rabbitohs", "Storm", "Eels", "Raiders", "Knights", "Dragons", "Sea Eagles", "Panthers", "Sharks", "Bulldogs", "Dolphins", "Titans", "Cowboys", "Warriors"]
# variables =["Win", "Defense", "Attack", "Margin"]

# with open('nrl_data.json', 'r') as file:
#     data = json.load(file)
#     data = data['NRL']
    
    
# df = pd.DataFrame(columns=[f"{team} {variable}" for team in teams for variable in variables])




# all_store = []
# for round in range(0, 22):
#     round_data = data[round][str(round+1)]
    
#     # Create an empty feature array 
#     round_store = np.zeros([len(teams)*len(variables)], dtype=int)
#     round_teams = []
#     for game in round_data:
#         h_team = game['Home']
#         h_score = int(game['Home_Score'])
#         a_team = game['Away']
#         a_score = int(game['Away_Score'])
        
#         # win or lose
#         h_team_win = h_score >= a_score
#         a_team_win = a_score >= h_score
        
#         # Defense (points let in)
#         h_team_defense = a_score
#         a_team_defense = h_score  
        
#         # Attack Points scored
#         h_team_attack = h_score 
#         a_team_attack = a_score   
        
#         # Margin
#         h_team_margin =  h_score-a_score   
#         a_team_margin =  a_score-h_score        
        
#         # Keep track of which teams played to work out which teams had a bye 
#         round_teams.append(h_team)
#         round_teams.append(a_team)
        
        
#         # Find the index of the team in the overaching array 
#         a_team_idx = teams.index(a_team)
#         h_team_idx = teams.index(h_team)
        
#         # Feature map index
#         a_team_idx_fm = a_team_idx*len(variables)
#         h_team_idx_fm = h_team_idx*len(variables)
        
#         # input(round_store)
#         # input(a_team_idx_fm)
#         # populate the data
#         round_store[a_team_idx_fm] = a_team_win
#         round_store[a_team_idx_fm+1] = a_team_defense
#         round_store[a_team_idx_fm+2] = a_team_attack
#         round_store[a_team_idx_fm+3] = a_team_margin
#         round_store[h_team_idx_fm] = h_team_win
#         round_store[h_team_idx_fm+1] = h_team_defense
#         round_store[h_team_idx_fm+2] = h_team_attack
#         round_store[h_team_idx_fm+3] = h_team_margin
    
#     # input(round_teams)
#     bye_teams = list(set(teams) - set(round_teams))
#     for bye_team in bye_teams:
#         b_team_idx = teams.index(bye_team)
#         b_team_idx_fm = b_team_idx*len(variables)
#         round_store[b_team_idx_fm] = -1
#         round_store[b_team_idx_fm+1] = -1
#         round_store[b_team_idx_fm+2] = -1
#         round_store[b_team_idx_fm+3] = 0
    
#     all_store.append(round_store)
#     # Create an array with the same size as the DataFrame

#     # Add the new row to the DataFrame using loc
#     df.loc[len(df)] = round_store
#     input(df)