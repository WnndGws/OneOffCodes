'''wynammBracket - script to setup and track fef tournaments'''

#Wynand Starting again

# Imports from Python Standard Library
import os.path
import pickle
import sys
from random import shuffle

# Set colors for terminal output
colour_red = "\033[01;31m{0}\033[00m"  # Wyn colour
colour_green = "\033[1;36m{0}\033[00m"  # Amm colour


def team_list_edit(teams):
    ''' Step through default teams list and ask whether to remove or keep.'''
    num_teams = len(teams)
    for i, team in enumerate(teams):
        user_input = input('Team no {0}/{1}: {2}.\n'
                           '(1) Keep\n'
                           '(2) Edit\n'
                           '(3) Remove\n'
                           '(4) Exit\n'
                           'Choice:'.format(i+1, num_teams, team))
        if user_input == '3':
            teams.remove(team)
            num_teams -= 1
        elif user_input == '4':
            return teams

    return teams


def team_list_add(teams):
    ''' Add team to default team list.'''
    user_input = input("Type team name, or 'e' to exit: ")
    if user_input == 'e':
        return teams
    else:
        teams.append(user_input)

    return teams


def team_chooser(team_list):
    '''Team chooser helper function.'''
    chosen_teams = []
    for i, team in enumerate(team_list):
        if i % 2 == 0:
            while True:
                selection = input('Press either "1" or "2" to choose your team\n'
                                  '(1) {0}\n'
                                  '(2) {1}\n'
                                  'Choice:'.format(team_list[i], team_list[i+1]))
                if selection not in ('1', '2'):
                    print("Please only enter 1 or 2")
                    continue
                elif selection == '1':
                    chosen_teams.append(team_list[i])
                    break
                elif selection == '2':
                    chosen_teams.append(team_list[i+1])
                    break
    return chosen_teams


def new_tournament():
    '''Load teams from file, otherwise load default teams.'''
    # Get absolute path of the dir script resides in.
    # os.getcwd() only returns dir script is invoked from.
    cwd = sys.path[0]
    if os.path.isfile(cwd + '/wynammBracket_possible_teams.txt'):
        with open(cwd + '/wynammBracket_possible_teams.txt', 'r') as file:
            teams = file.read().splitlines()
    else:  # Add default values when no config file is found
        print(colour_red.format('***NO TEAMS LIST FILE FOUND***'))
        print('Loading default teams.........')
        teams = ['FC Bayern', 'FC Barcelona', 'Real Madrid', 'PSG', 'Chelsea',
                 'Man City', 'Arsenal', 'Juventus', 'Bor Dortmund',
                 'Atletico Madrid', 'Man Utd.', 'Valencia', 'Napoli', 'Spurs',
                 'Liverpool', 'Roma', 'Sevilla FC', 'Villarreal CF', 'Bayer 04',
                 'Vfl Wolfsburg', 'Inter', 'Athletic Bilbao', 'SL Benfica',
                 'Sporting CP', 'Zenit', 'FC Schalke 04', 'Milan', 'Everton',
                 'Lazio', 'FC Porto', "Bor. M'gladbach", 'Besiktas', 'Fenerbahce',
                 'Fiorentina', 'Olym Lyonnais', 'AS Monaco', 'Real Sociedad',
                 'Newcastle Utd.', 'Stoke', 'West Ham', 'Celta Vigo', 'Swansea',
                 'Olym. Marseille', 'Torino', 'Real Betis', 'Leicester City',
                 'Southampton', 'Malaga CF', 'Crystal Palace', 'PSV',
                 '1899 Hoffenheim', 'Shakhtar Donetsk', 'Ajax', 'AS Saint-Etienne',
                 'CSKA Moscow', 'RC Deportivo', 'Sunderland', 'Watford',
                 'Stade Rennais', 'RCD Espanyol']
    shuffle(teams)  # Randomly order the teams

    # Create random list of 16 teams each
    possible_wyn_teams = teams[:16]
    possible_amm_teams = teams[16:32]

    while True:
    # Keep looping until user explicitly chooses to proceed.
    # Allows user as many chances as they want to edit/add teams.
        print("WARNING: This will overwrite any saved tournament you have!\n")
        user_input = input('(1) Proceed\n'
                           '(2) Edit teams\n'
                           '(3) Add teams\n'
                           '(4) Print teams that will be currently be randomised\n\n'
                           'Choice: ')
        if user_input == '1':
            if len(teams) < 32:
                print('Minimum of 32 teams required to proceed!')
            else:
                break
        elif user_input == '2':
            possible_teams = team_list_edit(teams)
        elif user_input == '3':
            possible_teams = team_list_add(teams)
        elif user_input == '4':
            print('No. teams: {0}'.format(len(teams)))
            print(possible_teams)

    #now to assign teams
    wyn_teams = []
    chosen_amm_teams = []
    print(colour_red.format("\n***Choosing Wyn teams***"))
    wyn_teams = team_chooser(possible_wyn_teams)
    print(colour_green.format("\n***Choosing Amm teams***"))
    amm_teams = team_chooser(possible_amm_teams)

    # Create matchups: wyn team 1 vs amm team 1 etc
    matchups_dict = {}
    scores_dict = {}

    for i, team in enumerate(wyn_teams):
        matchups_dict[team] = amm_teams[i]
        scores_dict[team] = "00+00 = 00"
        scores_dict[amm_teams[i]] = "00+00 = 00"
        if len(scores_dict) == 0:
            scores_dict[team] = 0
            scores_dict[chosen_amm_teams[i]] = 0
        print(colour_green.format('Matchup number {0}: '
                                  '{1} (Wyn) vs. {2} (Amm)'.format(i+1,
                                                                   team,
                                                                   amm_teams[i])))

    ''' Save tournament to file.'''
    with open('fef.pickle', 'wb') as file:
        pickle.dump((matchups_dict, scores_dict, wyn_teams, amm_teams),
                    file,
                    protocol=pickle.HIGHEST_PROTOCOL)

def print_bracket():
    ''' Return spaces matching length of longest team name.'''
    matchup_number = 0
    longest_length = 0
    while matchup_number < len(matchups_dict):
        wyn_team = list(matchups_dict)[matchup_number]
        amm_team = matchups_dict[list(matchups_dict)[matchup_number]]
        matchup_number += 1
        if len(wyn_team) > longest_length:
            longest_length = len(wyn_team)
        elif len(amm_team) > longest_length:
            longest_length = len(amm_team)

    if len(matchups_dict) > 4:
        lines = {}
        line_number = 1
        for x in range(0, 8):
            line = "_"*(longest_length+25)
            line = line.replace(line[:len(wyn_teams[x])], wyn_teams[x], 1)
            line = line.replace(line[len(wyn_teams[x]):(len(wyn_teams[x])+5)], "(Wyn)", 1)
            line = line[:-20]+"(Scores: {0})".format(scores_dict[wyn_teams[x]])
            lines["line{0}".format(line_number)] = line
            line_number += 1

        line_number = 9
        for x in range(0, 8):
            line = "_"*(longest_length+25)
            line = line.replace(line[:len(amm_teams[x])], amm_teams[x], 1)
            line = line.replace(line[len(amm_teams[x]):(len(amm_teams[x])+5)], "(Amm)", 1)
            line = line[:-20]+"(Scores: {0})".format(scores_dict[amm_teams[x]])
            lines["line{0}".format(line_number)] = line
            line_number += 1

        print(lines)

#def main(): #Commented out, will add in at end, otherwise makes debugging hard
''' Main function.'''
while True:
    try:
        action = input("Do you want to (s)tart a new tournament, or (c)ontinue a current tournament? "
                        "\nChoice: ")      
        if action in ('start', 's','1'):
            new_tournament()
            with open('fef.pickle', 'rb') as file:
                matchups_dict, scores_dict, wyn_teams, amm_teams = pickle.load(file)
            break
        elif action in ('continue', 'cont', 'c','2'):
            with open('fef.pickle', 'rb') as file:
                matchups_dict, scores_dict, wyn_teams, amm_teams = pickle.load(file)
            break
    except FileNotFoundError:
        print ("There doesnt seem to be a fif.pickle file saved...\nPlease move it into"
                "the correct folder, or start a new tournament")
                
    
    #No matter which way we went, we now have a dict with matchups and a dict with scores
    #Now need to present it nicely to the user

print_bracket()
    
#if __name__ == '__main__':
#    main()
