"""order of operations:
roll 4 dice to see how many black and red to remove
assign each day a red or a black
roll dice to see how many times to go through deck
remove all dayColours if draw a black from fullDeck
"""

import itertools
import random

numberOfDays = int(input("How many days this month? "))
diceNumber = ("1", "2", "3", "4", "5", "6")
diceColour = ("r", "b")
cardNumber = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
cardSuite = ("r", "b", "w", "b")

dayslist = []
cardsInDeck = []

for a, b in itertools.product(cardNumber, cardSuite):
    cardsInDeck.append(a + b)

diceRolls = 0
blackRolls = 0
redRolls = 0
while diceRolls < 4:
    roll = random.choice(diceNumber) + random.choice(diceColour)
    if roll[1] == "b":
        blackRolls += int(roll[0])
    else:
        redRolls += int(roll[0])
    diceRolls = diceRolls + 1

redCards = []
blackCards = []
for c in cardsInDeck:
    if c[1] == "s" or "c":
        blackCards.append(c)
    else:
        redCards.append(c)

random.shuffle(redCards)
random.shuffle(blackCards)

while blackRolls > 0:
    del blackCards[0]
    blackRolls = blackRolls - 1

while redRolls > 0:
    del redCards[0]
    redRolls = redRolls - 1

shuffledDeck = redCards + blackCards
random.shuffle(shuffledDeck)

dayColours = []
while numberOfDays > 0:
    dayColours.append(str(numberOfDays) + shuffledDeck[numberOfDays][-1])
    del shuffledDeck[numberOfDays]
    numberOfDays = numberOfDays - 1

while len(dayColours) > 11:
    possibleDeletions = len(dayColours)
    while possibleDeletions > 0:
        c = random.choice(diceColour)
        if c == "r":
            possibleDeletions = possibleDeletions - 1
        else:
            del dayColours[possibleDeletions - 1]
            possibleDeletions = possibleDeletions - 1

print(dayColours)
