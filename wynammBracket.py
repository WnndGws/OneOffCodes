'''Tasks:
1) save it all in a dictionary?
2) present us each with 2 options for teams
3) once 16 teams (8 each) have been chosen, progress to second round
    a) print out score from 1st round so we know who won etc.
4) once 2 legs have been played, halve the bracket, if one player has more than 4 teams go through they choose 1 team to keep and 1 team to eliminate
5) repeat'''

import random
import os
import sys

# Set colors for terminal output
colour_red = "\033[01;31m{0}\033[00m"
colour_green = "\033[1;36m{0}\033[00m"

def team_chooser(team_list):
    '''Team chooser helper function. Enter '1' to select first displayed team, and '2' or anything other than '1' for second team'''
    chosen_teams = []
    i = 0  #using this so that we can print the same teams if incorrect entry
    print ('Press either "1" or "2" to choose your team')
    selection = input("(1) {0}\n(2) {1}: \nChoice: ".format(team_list[i], team_list[i+1]))
    if selection not in ('1','2'):
        print ('Please only enter 1 or 2')     
    elif selection == '1':
        chosen_teams.append(team_list[i])
    elif selection == '2':
        chosen_teams.append(team_list[i+1])
        i += 2
                                
    return chosen_teams
    
def load_teams():
    cwd = sys.path[0] # Get absolute path of the dir script resides in. os.getcwd() only returns dir script is invoked from
    if os.path.isfile(cwd + '/wynammBracket_possible_teams.txt'):        
        with open(cwd + '/wynammBracket_possible_teams.txt', 'r') as file:
            possible_teams = file.read().splitlines()
        random.shuffle(possible_teams) # Randomly order the teams
        return possible_teams
    else: #add default values when no config file is found
        print (colour_red.format('***NO TEAMS LIST FILE FOUND***'))
        print ('Loading default teams.........')
        possible_teams = ['FC Bayern', 'FC Barcelona', 'Real Madrid', 'PSG', 'Chelsea', 'Man City', 'Arsenal', 'Juventus',
                 'Bor Dortmund', 'Atletico Madrid', 'Man Utd.', 'Valencia', 'Napoli', 'Spurs', 'Liverpool', 'Roma', 'Sevilla FC',
                 'Villarreal CF', 'Bayer 04', 'Vfl Wolfsburg', 'Inter', 'Athletic Bilbao', 'SL Benfica', 'Sporting CP', 'Zenit',
                 'FC Schalke 04', 'Milan', 'Everton', 'Lazio', 'FC Porto', "Bor. M'gladbach", 'Besiktas', 'Fenerbahce', 'Fiorentina',
                 'Olym Lyonnais', 'AS Monaco', 'Real Sociedad', 'Newcastle Utd.', 'Stoke', 'West Ham', 'Celta Vigo', 'Swansea', 
                 'Olym. Marseille', 'Torino', 'Real Betis', 'Leicester City', 'Southampton', 'Malaga CF', 'Crystal Palace', 'PSV',
                 '1899 Hoffenheim', 'Shakhtar Donetsk', 'Ajax', 'AS Saint-Etienne', 'CSKA Moscow', 'RC Deportivo', 'Sunderland',
                 'Watford', 'Stade Rennais', 'RCD Espanyol']
        random.shuffle(possible_teams)
        return possible_teams


def team_list_edit(teams):
    ''' Step through default teams list team by team and ask whether to remove or keep '''
    num_teams = len(teams)
    for i, team in enumerate(teams):
        user_input = input("{0}/{1}th team: {2}. Press any key to keep, 'r' to remove, 'e' to exit: ".format(i+1, num_teams, team))
        if user_input == 'r':
            teams.remove(team)
            num_teams -= 1
        elif user_input == 'e':
            break

    if len(possible_teams) < 32:
        print("Warning: team list only has {0} teams. Need 32 or more!".format(len(teams)))

def team_list_add(teams):
    ''' Add team to default team list '''
    user_input = input("Type team name, or 'e' to exit: ")
    if user_input == 'e':
        return teams
    else:
        teams.append(user_input)
        
    return teams  
    
if __name__ == '__main__':
    # Set colors for terminal output
    colour_red = "\033[01;31m{0}\033[00m"
    colour_green = "\033[1;36m{0}\033[00m"

    matchups_dict = {}
    scores_dict = {}
    
    possible_teams = load_teams()
    print("mvy fef tournament-o-matic.\nLoaded the following teams: \n")
#    print(possible_teams)
    
    while True: # Keep looping until user explicitly chooses to proceed. Allows user as many chances as they want to edit/add teams
        user_input = input("(1) Proceed\n(2) Edit teams\n(3) Add teams\n(4) Print current teams\nChoice: ")
        if user_input == '1':
            break
        elif user_input == '2':
            possible_teams = team_list_edit(possible_teams)
        elif user_input == '3':
            possible_teams = team_list_add(possible_teams)
        elif user_input == '4':
            print(possible_teams)
        
    if len(possible_teams) < 32:
        raise Exception("Minimum of 32 teams required in default teams text file!")
            
    # Create random list of 16 teams each
    possible_wyn_teams = possible_teams[:16]
    possible_amm_teams = possible_teams[16:32]

    # Present 2 teams at a time and have each choose their 8 teams
    chosen_wyn_teams = []
    chosen_amm_teams = []
    print(colour_red.format("***Choosing Wyn teams***"))
    chosen_wyn_teams = team_chooser(possible_wyn_teams)
    print(colour_green.format("***Choosing Amm teams***")) #use different colours for differnt users
    chosen_amm_teams = team_chooser(possible_amm_teams)

    # Create matchups: wyn team 1 vs amm team 1 etc
    for i, team in enumerate(chosen_wyn_teams):
        matchups_dict[team] = chosen_amm_teams[i]
    
    matchup_number = 0    
    print(colour_green.format("Matchup number {0}: {1}(Wyn) vs. {2}(Amm)".format(matchup_number+1, list(matchups_dict)[matchup_number], matchups_dict[list(matchups_dict)[matchup_number]])))
    matchup_number += 1
    
    '''Next thing to do is dump matchup_dict to a pickle, and then let it loop through all teams until all teams gone'''