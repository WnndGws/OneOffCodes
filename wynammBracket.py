'''wynammBracket - script to setup and track fef tournaments'''

# To do:
# once 16 teams (8 each) have been chosen, progress to second round
# print out score from 1st round so we know who won etc.
# once 2 legs have been played, halve the bracket, if one player has more
# than 4 teams go through they choose 1 team to keep and 1 team to eliminate
# make this into a Class object

# Imports from Python Standard Library
import os.path
import pickle
import sys
from random import shuffle

# Set colors for terminal output
colour_red = "\033[01;31m{0}\033[00m"  # Wyn colour
colour_green = "\033[1;36m{0}\033[00m"  # Amm colour


def load_teams():
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
    return teams


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
                    continue
                elif selection == '1':
                    chosen_teams.append(team_list[i])
                    break
                elif selection == '2':
                    chosen_teams.append(team_list[i+1])
                    break
    return chosen_teams


def save_tournament(matchups_dict, scores_dict):
    ''' Save tournament to file.'''
    with open('fef.pickle', 'wb') as file:
        pickle.dump((matchups_dict, scores_dict),
                    file,
                    protocol=pickle.HIGHEST_PROTOCOL)


def load_tournament(matchups_dict, scores_dict):
    ''' Load tournament from file.'''
    with open('fef.pickle', 'rb') as file:
        matchups_dict, scores_dict = pickle.load(file)


def calc_longest_team(matchups_dict):
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
            longest_length = len(wyn_team)
    return longest_length


def calc_spaces(longest_length, wyn_team, amm_team):
    ''' Calculate no. of spaces to put after team name when printing tournament.'''
    diff_wyn = longest_length - len(wyn_team)
    diff_amm = longest_length - len(amm_team)
    wyn_spaces = ' ' * (diff_wyn+1)
    amm_spaces = ' ' * (diff_amm+1)
    return wyn_spaces, amm_spaces


def print_tournament(matchups_dict, scores_dict):
    ''' Print tournament bracket into terminal.'''
    matchup_number = 0
    longest_team = calc_longest_team(matchups_dict)
    print('        Round16       |     Round8         |       Round4      |     Final  ')
    while matchup_number < len(matchups_dict):
        wyn_team = list(matchups_dict)[matchup_number]
        amm_team = matchups_dict[list(matchups_dict)[matchup_number]]
        wyn_spaces, amm_spaces = calc_spaces(longest_team, wyn_team, amm_team)
        print(colour_red.format('{0}{1}---\\'.format(wyn_team, wyn_spaces)))
        # Test print of next round
        print(colour_green.format('{0}{1}{2}---\\'.format(amm_spaces+' '*(5+len(amm_team)), amm_team, amm_spaces)))
        print(colour_green.format('{0}{1}---/\n\n'.format(amm_team, amm_spaces)))
        matchup_number += 1
        
def match_outcomes(matchups_dict, scores_dict):
    '''Allow user to enter scores for each matchup'''
    matchup_chosen = input('Which matchup do you want to play next (1-{0})?: '.format(len(matchups_dict)))

def main():
    ''' Main function.'''
    matchups_dict = {}
    scores_dict = {}

    possible_teams = load_teams()
#    print("mvy fef tournament-o-matic.\nLoaded the following teams: \n")
#    print(possible_teams)

    while True:
        # Keep looping until user explicitly chooses to proceed.
        # Allows user as many chances as they want to edit/add teams.
        user_input = input('(1) Proceed\n'
                           '(2) Edit teams\n'
                           '(3) Add teams\n'
                           '(4) Print current teams\n'
                           'Choice: ')
        if user_input == '1':
            if len(possible_teams) < 32:
                print('Minimum of 32 teams required to proceed!')
            else:
                break
        elif user_input == '2':
            possible_teams = team_list_edit(possible_teams)
        elif user_input == '3':
            possible_teams = team_list_add(possible_teams)
        elif user_input == '4':
            print('No. teams: {0}'.format(len(possible_teams)))
            print(possible_teams)

    # Create random list of 16 teams each
    possible_wyn_teams = possible_teams[:16]
    possible_amm_teams = possible_teams[16:32]

    # Present 2 teams at a time and have each choose their 8 teams
    chosen_wyn_teams = []
    chosen_amm_teams = []
    print(colour_red.format("***Choosing Wyn teams***"))
    chosen_wyn_teams = team_chooser(possible_wyn_teams)
    print(colour_green.format("***Choosing Amm teams***"))
    chosen_amm_teams = team_chooser(possible_amm_teams)

    # Create matchups: wyn team 1 vs amm team 1 etc
    for i, team in enumerate(chosen_wyn_teams):
        matchups_dict[team] = chosen_amm_teams[i]
        if len(scores_dict) == 0:        
            scores_dict[team] = 0
            scores_dict[chosen_amm_teams[i]] = 0
        print(colour_green.format('Matchup number {0}: '
                                  '{1} (Wyn) vs. {2} (Amm)'.format(i+1,
                                                                   team,
                                                                   chosen_amm_teams[i])))
    # Save tournament to file
    save_tournament(matchups_dict, scores_dict)
    # Print tournament status to terminal
    'print_tournament(matchups_dict, scores_dict)'
    match_outcomes(matchups_dict, scores_dict)

if __name__ == '__main__':
    main()
