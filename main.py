from random import shuffle
import sys
import os

cards_dict = {"Color": ["hearths", "diamonds", "clubs", "spades"], "Value": [6, 7, 8, 9, 10, 11, 12, 13, 14],
              "ValSymbol": ["6", "7", "8", "9", "10", "J", "D", "K", "A"], "ColSymbol": ["<3", "<>", "8-", "<)"]}
deck = [0] * 36
idx = -1

for col in cards_dict.get("Color"):
    for val in cards_dict.get("Value"):
        idx = idx + 1
        idx_of_col = cards_dict["Color"].index(col)
        idx_of_val = cards_dict["Value"].index(val)
        deck[idx] = {"Color": col, "Value": val,
                     "Name": cards_dict["ValSymbol"][idx_of_val] + " " + cards_dict["ColSymbol"][idx_of_col]}

shuffle(deck)
gl_card = deck[35]
gl_col = gl_card["Color"]
# print(gl_col)
for i in range(len(deck)):
    if deck[i]["Color"] == gl_col:
        deck[i]["Value"] = deck[i]["Value"] + 10
        deck[i]["Name"] = deck[i]["Name"] + "*"
# print(deck)

players_hand = []
bobbys_hand = []

table_atk = []
table_def = []

cards_to_counter = []

who_atkd = 0
breaker = 0

p_atk_phase = False
p_def_phase = False


# Function that realizes an operation of moving "what" card from "from_p" list to "to_p" list
def cardTransfer(what, from_p, to_p):
    from_p.remove(what)
    to_p.append(what)


# Function that grants us vision of our cards and the table via cmd
def vision():
    # print("\033[H\033[J", end="")
    print("\nTrump card: " + gl_col)
    print("Table:")
    print("D: ", [p["Name"] for p in table_def])
    print("A: ", [p["Name"] for p in table_atk])
    print("Your hand: ")
    print([p["Name"] for p in players_hand])
    print("Bobby: ", [p["Name"] for p in bobbys_hand])


# Function that enables us to start a game
def startGame():
    shuffle(deck)
    [cardTransfer(deck[0], deck, players_hand) for _ in range(6)]
    [cardTransfer(deck[0], deck, bobbys_hand) for _ in range(6)]
    players_hand.sort(key=lambda x: x["Value"])
    print("Trump card: " + gl_col)
    print("Your hand: ")
    print([p["Name"] for p in players_hand])

    #print("Bobby: ", [p["Name"] for p in bobbys_hand])
    # print(len(deck))



# Function that realizes an attack sequence for a player or Bobby
def attack(who):
    breaker = False
    global who_atkd  # player is True, Bobby is False
    p_atk_phase = True
    while p_atk_phase == True:
        if who == False:  # PLAYER
            picked_atk = int(
                input("\nPick a number of a card you want to play (from 1 to " + str(len(players_hand)) + "): "))
            if picked_atk in list(range(1, len(players_hand) + 1)):
                cardTransfer(players_hand[picked_atk - 1], players_hand, table_atk)
                who_atkd = True
                p_atk_phase = False
            else:
                print("\nWrong value, pick a number between 1 and " + str(len(players_hand)) + " ")
        elif who == True:  # BOBBY
            bobbys_hand.sort(key=lambda x: x["Value"])
            cardTransfer(bobbys_hand[0], bobbys_hand, table_atk)
            print("\n++ Bobby attacked with: " + table_atk[len(table_atk) - 1]["Name"] + "! ++")
            who_atkd = False
            p_atk_phase = False
    vision()
    if p_atk_phase == False:
        defense()
    if breaker: return


# Function that checks if countering "card_table" is possible with "card_hand"
def checkCard(card_table, card_hand):
    global can_def
    if card_hand["Color"] == card_table["Color"] and card_hand["Value"] > card_table["Value"]:
        can_def = True
    elif card_hand["Color"] == gl_col and card_table["Color"] != card_hand["Color"]:
        can_def = True
    elif card_hand["Color"] != card_table["Color"] and card_hand["Color"] != gl_col:
        can_def = False
    else:
        can_def = False


# Function that realizes a defense sequence
def defense():
    p_def_phase = True
    global who_atkd
    global if_odbit
    while p_def_phase:
        if not who_atkd:  # PLAYER DEFENDS
            p_hand_no_trump = players_hand.copy()
            for c in p_hand_no_trump:
                if c["Color"] == gl_col: p_hand_no_trump.remove(c)
            if all(d.get("Value") < table_atk[len(table_atk) - 1]["Value"] for d in players_hand) or (
                    all(d.get("Color") != table_atk[len(table_atk) - 1]["Color"] for d in p_hand_no_trump) and len(p_hand_no_trump) == len(players_hand)):
                for j in range(1, len(table_atk)+1):
                    cardTransfer(table_atk[0], table_atk, players_hand)
                for j in range(1, len(table_def)+1):
                    cardTransfer(table_def[0], table_def, players_hand)
                print("\n== You have to take the cards! ==")
                players_hand.sort(key=lambda x: x["Value"])
                vision()
                if_odbit = False
                p_def_phase = False
                who_atkd = True
                endOfTurn()
            else:
                picked_def = input("\nPick a card to defend, or take the table (from 1 to " + str(
                    len(players_hand)) + ", or \'take\'): ")
                if picked_def == 'take' or picked_def == 't':
                    for j in range(1, len(table_atk) + 1):
                        cardTransfer(table_atk[0], table_atk, players_hand)
                    for j in range(1, len(table_def) + 1):
                        cardTransfer(table_def[0], table_def, players_hand)
                    print("\n== You have taken the cards! ==")
                    players_hand.sort(key=lambda x: x["Value"])
                    #vision()
                    if_odbit = False
                    p_def_phase = False
                    who_atkd = True
                    endOfTurn()
                elif picked_def.isdigit() == True and int(picked_def) in range(1, len(players_hand) + 1):
                    checkCard(table_atk[len(table_atk) - 1], players_hand[int(picked_def) - 1])
                    if can_def:
                        cardTransfer(players_hand[int(picked_def) - 1], players_hand, table_def)
                        vision()
                        if_odbit = True
                        p_def_phase = False
                    else:
                        print("\n== Can't defend with that card, pick correct one or \'take\' ==")
                        vision()
                else:
                    print("== Wrong value, pick a card to defend, or take the table (from 1 to " + str(
                        len(players_hand)) + ", or \'take\') ==")
                    vision()
        elif who_atkd == True:  # BOBBY DEFENDS
            p_hand_no_trump = bobbys_hand.copy()
            for c in p_hand_no_trump:
                if c["Color"] == gl_col: p_hand_no_trump.remove(c)
            if all(d.get("Value") < table_atk[len(table_atk) - 1]["Value"] for d in bobbys_hand) or (
                    all(d.get("Color") != table_atk[len(table_atk) - 1]["Color"] for d in p_hand_no_trump) and all(
                d.get("Color") != gl_col for d in bobbys_hand)):
                print("\nAAAAAAA ", table_atk)
                for j in range(1, len(table_atk)): cardTransfer(table_atk[0], table_atk, bobbys_hand)
                for j in range(1, len(table_def)): cardTransfer(table_def[0], table_def, bobbys_hand)
                print("\n++ Bobby took the card! ++")
                #vision()
                if_odbit = False
                who_atkd = False
                endOfTurn()
            else:
                can_def_cards = []
                for p in bobbys_hand:
                    checkCard(table_atk[len(table_atk) - 1], p)
                    if can_def:
                        can_def_cards.append(p)
                        can_def_cards.sort(key=lambda x: x["Value"])
                if len(can_def_cards) != 0:
                    cardTransfer(bobbys_hand[bobbys_hand.index(can_def_cards[0])], bobbys_hand, table_def)
                print("\n++ Bobby defended with " + table_def[len(table_def) - 1]["Name"] + "! ++")
                vision()
                if_odbit = True
            p_def_phase = False
    if if_odbit:
        discards()
    elif not if_odbit:
        endOfTurn()
    if breaker: return

def checkForSim(hand, table):
    for c in range(1, len(hand)):
        for t in range(1, len(table)):
            if hand[c-1]["Value"] == table[t-1]["Value"] or \
                    (hand[c-1]["Color"] == gl_col and hand[c-1]["Value"] == table[t-1]["Value"] + 10) or \
                    (table[t-1]["Color"] == gl_col and hand[c-1]["Value"] == table[t-1]["Value"] - 10):
                return True
            else:
                return False


def discards():
    global if_odbit
    global who_atkd
    while if_odbit:
        if who_atkd == True and (len(table_atk) != 0 and len(table_def) != 0):  # PLAYER DISCARDS
            if (not checkForSim(players_hand, table_atk) and not checkForSim(players_hand, table_def)) or len(table_atk) == 5:
                table_atk.clear()
                table_def.clear()
                print("\n== Cards are discarded, can't counter ==")
                vision()
                if_odbit = False
                endOfTurn()
            else:
                #cards_to_counter.clear
                cards_to_counter = []

                for c in players_hand:
                    for t in table_atk:
                        if c["Value"] == t["Value"] or c["Value"] == t["Value"] + 10 or c["Value"] == t["Value"] - 10:
                            cards_to_counter.append(c)
                    for t in table_def:
                        if (c["Value"] == t["Value"] or c["Value"] == t["Value"] + 10 or c["Value"] == t["Value"] - 10) and (c not in cards_to_counter):
                            cards_to_counter.append(c)

                odbit = input("\nYou discard or counter attack? (type 'odbit' or a number of a card to play): ")
                if odbit == "odbit" or odbit == "o":
                    table_atk.clear()
                    table_def.clear()
                    vision()
                    if_odbit = False
                    who_atkd = True
                    endOfTurn()
                elif (odbit.isdigit() == True) and (int(odbit) in range(1, len(players_hand) + 1)) and \
                        (len(cards_to_counter) > 0) and (players_hand[int(odbit) - 1] in cards_to_counter):
                    cardTransfer(players_hand[int(odbit) - 1], players_hand, table_atk)
                    vision()
                    who_atkd = True
                    defense()
                else:
                    print("\n== You can't do that! ==")
                    vision()
        elif not who_atkd:  # BOBBY DISCARDS
            if (not checkForSim(players_hand, table_atk) and not checkForSim(players_hand, table_def)) or len(table_atk) <= 5:
                table_atk.clear()
                table_def.clear()
                print("\n++ Cards are discarded, can't counter ++")
                vision()
                if_odbit = False
                who_atkd = False
                endOfTurn()
            else:
                #cards_to_counter.clear
                cards_to_counter = []

                for c in bobbys_hand:
                    for t in table_atk:
                        if c["Value"] == t["Value"] or c["Value"] == t["Value"] + 10 or c["Value"] == t["Value"] - 10:
                            cards_to_counter.append(c)
                    for t in table_def:
                        if (c["Value"] == t["Value"] or c["Value"] == t["Value"] + 10 or c["Value"] == t["Value"] - 10) and (c not in cards_to_counter):
                            cards_to_counter.append(c)

                cards_to_counter.sort(key=lambda x: x["Value"])
                cardTransfer(bobbys_hand[bobbys_hand.index(cards_to_counter[0])], bobbys_hand, table_atk)
                print("\n++ Bobby counter attacked with " + table_atk[len(table_atk) - 1]["Name"] + "! ++")
                vision()
                who_atkd = False
                defense()
    if breaker: return

def endOfTurn():
    deck_empty = False
    global breaker
    p_draw = 6 - len(players_hand)
    b_draw = 6 - len(bobbys_hand)
    if (p_draw > 0) and (not deck_empty):
        for _ in range(p_draw):
            if len(deck) > 0:
                cardTransfer(deck[0], deck, players_hand)
            elif len(deck) == 0:
                deck_empty = True
        players_hand.sort(key=lambda x: x["Value"])
    if b_draw > 0 and (not deck_empty):
        for _ in range(b_draw):
            if len(deck) > 0:
                cardTransfer(deck[0], deck, bobbys_hand)
            elif len(deck) == 0:
                deck_empty = True
        bobbys_hand.sort(key=lambda x: x["Value"])
    print("\n== End of turn. You drew " + str(max(p_draw, 0)) + " cards ==")
    vision()
    breaker = True
    return


startGame()
# table_atk = [{"Color": 'clubs', "Value": 24, "Name": "A 8-*"}]
attack(True)
while len(players_hand) > 0 and len(bobbys_hand) > 0:
    if breaker: attack(who_atkd)
if len(players_hand) == 0 and len(bobbys_hand) != 0:
    print("\n\n=== YOU WON!!! CONGRATULATIONS!!! ===\n")
    sys.exit()
elif len(bobbys_hand) == 0 and len(players_hand) != 0:
    print("\n\n+++ BOBBY WON!!! BETTER LUCK NEX TIME! +++\n")
    sys.exit()
# defense()
