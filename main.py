from random import shuffle
import sys
import os

cards_dict = {"Color": ["hearths", "diamonds", "clubs", "spades"], "Value": [6, 7, 8, 9, 10, 11, 12, 13, 14], "ValSymbol": ["6", "7", "8", "9", "10", "J", "D", "K", "A"], "ColSymbol": ["<3", "<>", "8-", "<)"]}
deck = [0]*36
idx = -1

for col in cards_dict.get("Color"):
    for val in cards_dict.get("Value"):
        idx = idx + 1
        idx_of_col = cards_dict["Color"].index(col)
        idx_of_val = cards_dict["Value"].index(val)
        deck[idx] = {"Color": col, "Value": val, "Name": cards_dict["ValSymbol"][idx_of_val] + " " + cards_dict["ColSymbol"][idx_of_col]}

shuffle(deck)
gl_card = deck[35]
gl_col = gl_card["Color"]
#print(gl_col)
for i in range(len(deck)):
    if deck[i]["Color"] == gl_col:
        deck[i]["Value"] = deck[i]["Value"] + 10
        deck[i]["Name"] = deck[i]["Name"] + "*"
#print(deck)

players_hand = []
bobbys_hand = []

table_atk = []
table_def = []
gone_cards = []

p_atk_phase = False
p_def_phase = False

# Function that realizes an operation of moving "what" card from "from_p" list to "to_p" list
def cardTransfer(what, from_p, to_p):
    from_p.remove(what)
    to_p.append(what)

# Function that grants us vision of our cards and the table via cmd
def vision():
    print("\033[H\033[J", end="")
    print("\nTrump card: " + gl_col)
    print("Table:")
    print("D: ", [p["Name"] for p in table_def])
    print("A: ", [p["Name"] for p in table_atk])
    print("Your hand: ")
    print([p["Name"] for p in players_hand])

# Function that enables us to start a game
def startGame():
    shuffle(deck)
    [cardTransfer(deck[0], deck, players_hand) for _ in range(6)]
    [cardTransfer(deck[0], deck, bobbys_hand) for _ in range(6)]
    players_hand.sort(key=lambda x: x["Value"])
    print("Trump card: " + gl_col)
    print("Your hand: ")
    print([p["Name"] for p in players_hand])
    #print([p["Name"] for p in bobbys_hand])
    #print(len(deck))

# Function that realizes an attack sequence for a player or Bobby
def attack(who):
    global who_was #player is True, Bobby is False
    p_atk_phase = True
    while p_atk_phase == True:
        if who == 1: #PLAYER
            picked_atk = int(input("\nPick a number of a card you want to play (from 1 to " + str(len(players_hand)) + "): "))
            if picked_atk in list(range(1, len(players_hand) + 1)):
                cardTransfer(players_hand[picked_atk - 1], players_hand, table_atk)
                who_was = True
                p_atk_phase = False
            else:
                print("\nWrong value, pick a number between 1 and " + str(len(players_hand)) + " ")
        elif who == 2: #BOBBY
            bobbys_hand.sort(key=lambda x: x["Value"])
            cardTransfer(bobbys_hand[0], bobbys_hand, table_atk)
            who_was = False
            p_atk_phase = False
    vision()
    if p_atk_phase == False:
        defense()

# Function that checks if countering "card_table" is possible with "card_hand"
def checkCard(card_table, card_hand):
    global can_def
    if (card_hand["Color"] == card_table["Color"] or card_hand["Color"] == gl_col) and card_hand["Value"] > card_table["Value"]:
        can_def = True
    else:
        can_def = False

# Function that realizes a defense sequence
def defense():
    p_def_phase = True
    global who_was
    global if_odbit
    while p_def_phase == True:
        if who_was == False: #PLAYER DEFENDS
            p_hand_no_trump = players_hand.copy()
            for c in p_hand_no_trump:
                if c["Color"] == gl_col: p_hand_no_trump.remove(c)
            if all(d.get("Value", 0) < table_atk[0]["Value"] for d in players_hand) or (all(d.get("Color") != table_atk[0]["Color"] for d in p_hand_no_trump) and all(d.get("Color") != gl_col for d in players_hand)):
                print("\n== You have to take the card! ==")
                cardTransfer(table_atk[0], table_atk, players_hand)
                players_hand.sort(key=lambda x: x["Value"])
                vision()
                if_odbit = False
                p_def_phase = False
            else:
                picked_def = input("\nPick a card to defend, or take the table (from 1 to " + str(len(players_hand)) + ", or \'take\'): ")
                if picked_def == 'take' or picked_def == 't':
                    cardTransfer(table_atk[0], table_atk, players_hand)
                    players_hand.sort(key=lambda x: x["Value"])
                    vision()
                    if_odbit = False
                    p_def_phase = False
                elif picked_def.isdigit() == True and int(picked_def) in range(1, len(players_hand)+1):
                    checkCard(table_atk[0], players_hand[int(picked_def) - 1])
                    if can_def == True:
                        cardTransfer(players_hand[int(picked_def)-1], players_hand, table_def)
                        vision()
                        if_odbit = True
                        p_def_phase = False
                        who_was = True
                    else:
                        print("\n== Can't defend with that card, pick correct one or \'take\' ==")
                        vision()
                else:
                    print("== Wrong value, pick a card to defend, or take the table (from 1 to " + str(len(players_hand)) + ", or \'take\') ==")
                    vision()
        elif who_was == True: #BOBBY DEFENDS
            p_hand_no_trump = bobbys_hand.copy()
            for c in p_hand_no_trump:
                if c["Color"] == gl_col: p_hand_no_trump.remove(c)
            if all(d.get("Value", 0) < table_atk[0]["Value"] for d in bobbys_hand) or (all(d.get("Color") != table_atk[0]["Color"] for d in p_hand_no_trump) and all(d.get("Color") != gl_col for d in bobbys_hand)):
                cardTransfer(table_atk[0], table_atk, bobbys_hand)
                print("\n++ Bobby took the card! ++")
                vision()
                if_odbit = False
            else:
                can_def_cards = []
                for p in bobbys_hand:
                    checkCard(table_atk[0], p)
                    if can_def == True:
                        can_def_cards.append(p)
                        can_def_cards.sort(key=lambda x: x["Value"])
                if len(can_def_cards) != 0:
                    cardTransfer(bobbys_hand[bobbys_hand.index(can_def_cards[0])], bobbys_hand, table_def)
                print("\n++ Bobby defended with " + table_def[0]["Name"] + "! ++")
                vision()
                if_odbit = True
                who_was = False
            p_def_phase = False
    if if_odbit == True:
        odbitCheck()
    elif if_odbit == False:
        attack(who_was)

def odbitCheck():
    global if_odbit
    global who_was
    while if_odbit == True:
        if who_was == False: #PLAYER DISCARDS
            if all(d.get("Value", 0) != table_def[0]["Value"] for d in players_hand) and all(d.get("Value", 0) != table_atk[0]["Value"] for d in players_hand):
                print("\n== Cards are discarded, can't counter ==")
                if_odbit = False
            else:
                cards_to_counter = players_hand.copy()
                for c in cards_to_counter:
                    if (c["Value"] != table_def[0]["Value"]) and (c["Value"] != table_atk[0]["Value"]):
                        cards_to_counter.remove(c)
                odbit = input("\nYou discard or counter attack? (type 'odbit' or a number of a card to play)")
                if odbit == "odbit" or odbit == "o":
                    cardTransfer(table_atk[0], table_atk, gone_cards)
                    cardTransfer(table_def[0], table_def, gone_cards)
                    vision()
                    if_odbit = False
                elif (odbit.isdigit() == True) and (int(odbit) in range(1, len(players_hand)+1)) and (len(cards_to_counter) > 0) and (players_hand[int(odbit) - 1] in cards_to_counter):
                    cardTransfer(players_hand[int(odbit)], players_hand, table_atk)
                    vision()
                    who_was = True
                    defense()
                    if_odbit = False
                else:
                    print("\n== You can't do that! ==")
                    vision()
        elif who_was == True: #BOBBY DISCARDS
            if all(d.get("Value", 0) != table_def[0]["Value"] for d in bobbys_hand) and all(d.get("Value", 0) != table_atk[0]["Value"] for d in bobbys_hand):
                print("\n== Cards are discarded, can't counter ==")
                if_odbit = False
            else:
                cards_to_counter = bobbys_hand.copy()
                for c in cards_to_counter:
                    if (c["Value"] != table_def[0]["Value"]) and (c["Value"] != table_atk[0]["Value"]):
                        cards_to_counter.remove(c)
                        #UNFINISHED!!!



startGame()
#table_atk = [{"Color": 'clubs', "Value": 24, "Name": "A 8-*"}]
attack(1)
#defense()



