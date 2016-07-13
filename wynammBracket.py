'''Tasks:
1) save it all in a dictionary?
2) present us each with 2 options for teams
3) once 16 teams (8 each) have been chosen, progress to second round
    a) print out score from 1st round so we know who won etc.
4) once 2 legs have been played, halve the bracket, if one player has more than 4 teams go through they choose 1 team to keep and 1 team to eliminate
5) repeat'''

import random
import os

def team_chooser(team_list):
    '''Team chooser helper function.Enter '1' to select first displayed team, and '2' or anything other than '1' for second team'''
    chosen_teams = []
    for i, team in enumerate(team_list):
        if i % 2 == 0:
            selection = input("Enter 1 for {0} or 2 for {1}: ".format(team_list[i], team_list[i+1]))
            if selection == '1':
                chosen_teams.append(team_list[i])
            else:
                chosen_teams.append(team_list[i+1])
    return chosen_teams

# Set colors for terminal output
colour_red = "\033[01;31m{0}\033[00m"
colour_green = "\033[1;36m{0}\033[00m"

matchups_dict = {}
scores_dict = {}

with open('wynammBracket_possible_teams.txt', 'r') as file:
    possible_teams=file.read().splitlines()
random.shuffle(possible_teams) # Randomise teams

if len(possible_teams) < 32:
    raise Exception("Minimum of 32 teams required in text file")

# Create random list of 16 teams each
possible_wyn_teams = possible_teams[:16]
possible_amm_teams = possible_teams[16:32]

# Present 2 teams at a time and have each choose their 8 teams
chosen_wyn_teams = []
chosen_amm_teams = []
print(colour_red.format('***Choosing Wyn teams***'))
chosen_wyn_teams = team_chooser(possible_wyn_teams)
print(colour_red.format('***Choosing Amm teams***'))
chosen_amm_teams = team_chooser(possible_amm_teams)

print('*****************************')
print(chosen_wyn_teams)
print('*****************************')
print(chosen_amm_teams)

# Create matchups: wyn team 1 vs amm team 1 etc
for i, team in enumerate(chosen_wyn_teams):
    matchups_dict[team] = chosen_amm_teams[i]
    
print(colour_green.format(matchups_dict))
