'''Tasks:
1) save it all in a dictionary?
2) present us each with 2 options for teams
3) once 16 teams (8 each) have been chosen, progress to second round
    a) print out score from 1st round so we know who won etc.
4) once 2 legs have been played, halve the bracket, if one player has more than 4 teams go through they choose 1 team to keep and 1 team to eliminate
5) repeat'''

import random

opponentsDict = {}
scoresDict = {}

possibleTeams = ['FC Bayern', 'FC Barcelona', 'Real Madrid', 'PSG', 'Chelsea', 'Man City', 'Arsenal', 'Juventus',
                 'Bor Dortmund', 'Atletico Madrid', 'Man Utd.', 'Valencia', 'Napoli', 'Spurs', 'Liverpool', 'Roma', 'Sevilla FC',
                 'Villarreal CF', 'Bayer 04', 'Vfl Wolfsburg', 'Inter', 'Athletic Bilbao', 'SL Benfica', 'Sporting CP', 'Zenit',
                 'FC Schalke 04', 'Milan', 'Everton', 'Lazio', 'FC Porto', "Bor. M'gladbach", 'Besiktas', 'Fenerbahce' 'Fiorentina',
                 'Olym Lyonnais', 'AS Monaco', 'Real Sociedad', 'Newcastle Utd.', 'Stoke', 'West Ham', 'Celta Vigo', 'Swansea', 
                 'Olym. Marseille', 'Torino', 'Real Betis', 'Leicester City', 'Southampton', 'Malaga CF', 'Crystal Palace', 'PSV',
                 '1899 Hoffenheim', 'Shakhtar Donetsk', 'Ajax', 'AS Saint-Etienne', 'CSKA Moscow', 'RC Deportivo', 'Sunderland',
                 'Watford', 'Stade Rennais', 'RCD Espanyol']
           
shuffledTeams = []
for item in possibleTeams:
    shuffledTeams.append(item)
random.shuffle(shuffledTeams)

#next step: present each with two teams, and save the choice to teams list, and the matchup to opponentsDict
                 
wynTeams = []
ammTeams = []

