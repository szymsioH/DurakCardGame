from random import shuffle
import random
import sys

cards_dict = {"Color": ["hearths", "diamonds", "clubs", "spades"], "Value": [6, 7, 8, 9, 10, 11, 12, 13, 14],
              "ValSymbol": ["6", "7", "8", "9", "10", "J", "D", "K", "A"], "ColSymbol": ["<3", "<>", "8-", "<)"]}

deck = [0] * 36
idx = 0
for col in cards_dict.get("Color"):
    for val in cards_dict.get("Value"):
        idx_of_col = cards_dict["Color"].index(col)
        idx_of_val = cards_dict["Value"].index(val)
        deck[idx] = {"Color": col, "Value": val,
                     "Name": cards_dict["ValSymbol"][idx_of_val] + " " + cards_dict["ColSymbol"][idx_of_col]}
        idx = idx + 1

shuffle(deck)
gl_card = deck[-1]
gl_col = gl_card["Color"]

for i in range(len(deck)):
    if deck[i]["Color"] == gl_col:
        deck[i]["Value"] = deck[i]["Value"] + 10
        deck[i]["Name"] = deck[i]["Name"] + "*"


players_hand = []
bobbys_hand = []
dannys_hand = []

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


# Function that enables us to start a game
def startGame():
    #deck.sort(key=lambda x: x["Value"]) #POTEM WYWALIĆ!!
    for i in range(0, 6):
        cardTransfer(deck[0], deck, players_hand)
        cardTransfer(deck[0], deck, bobbys_hand)
        cardTransfer(deck[0], deck, dannys_hand)
    players_hand.sort(key=lambda x: x["Value"])
    bobbys_hand.sort(key=lambda x: x["Value"])
    dannys_hand.sort(key=lambda x: x["Value"])
    print("\nTrump card: |" + gl_card.get("Name") + "|")
    if who_starts == 3:
        print("\n=+= YOU ATTACK FIRST!!! +=+\n",)
    elif who_starts == 1:
        print("\n=+= BOBBY ATTACKS FIRST!!! +=+\n", )
    elif who_starts == 2:
        print("\n=+= DANNY ATTACKS FIRST!!! +=+\n", )


# Function that grants us vision of our cards and the table via cmd
def vision_full():
    print("\nTrump card: |" + gl_card.get("Name") + "|")
    print("Table:")
    print("D: ", [p["Name"] for p in table_def])
    print("A: ", [p["Name"] for p in table_atk])
    print("Your hand: ", [p["Name"] for p in players_hand])
    print("Bobby: ", [p["Name"] for p in bobbys_hand])
    # print("Bobby has ", len(bobbys_hand), " cards")
    print("Danny: ", [p["Name"] for p in dannys_hand])
    # print("Danny has ", len(dannys_hand), " cards")


# Function that grants us vision of our cards via cmd
def vision_hand():
    print("\nYour hand: ", [p["Name"] for p in players_hand])
    print("Bobby: ", [p["Name"] for p in bobbys_hand])
    # print("Bobby has ", len(bobbys_hand), " cards")
    print("Danny: ", [p["Name"] for p in dannys_hand])
    # print("Danny has ", len(dannys_hand), " cards")


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


# Function that checks for cards of similar value
def checkForSim(hand, table):
    global sim_card_list
    sim_card_list = []
    sim_card_list.clear()
    for t in range(1, len(table) + 1):
        for c in range(1, len(hand) + 1):
            if hand[c - 1]["Value"] == table[t - 1]["Value"] or \
                    (hand[c - 1]["Color"] == gl_col and hand[c - 1]["Value"] == table[t - 1]["Value"] + 10) or \
                    (table[t - 1]["Color"] == gl_col and hand[c - 1]["Value"] == table[t - 1]["Value"] - 10):
                sim_card_list.append(hand[c - 1])
    if len(sim_card_list) != 0:
        sim_card_list.sort(key=lambda x: x["Value"])
        return True


# Function that specifies when it is not worth to perform an action by bots
def betterBots(atk_or_def, added_card, compare_card):
    if atk_or_def == 'attack':
        if added_card.get("Value") - compare_card.get("Value") > 9 and len(table_atk) < 3 < len(deck):
            return False
        elif added_card.get("Value") - compare_card.get("Value") > 15 and len(table_atk) < 4 and len(deck) > 1:
            return False
        else:
            return True
    elif atk_or_def == 'defense':
        if len(table_atk) + len(table_def) < 4 and added_card.get("Value") - compare_card.get("Value") > 10 and len(
                deck) > 3:
            return False
        elif len(table_atk) + len(table_def) < 6 and added_card.get("Value") - compare_card.get("Value") > 15 and len(
                deck) > 1:
            return False
        else:
            return True
    # return True #SWITCH OFF for this function


# Functions that enables attacks with multiple cards at once
def someMore(bot_or_not, hand, opponent_hand):
    if bot_or_not == 'player':
        if (any(d.get("Value") == table_atk[-1]["Value"] for d in sim_card_list) or
            any((d.get("Value") - 10) == table_atk[-1]["Value"] for d in sim_card_list) or
            any((d.get("Value") + 10) == table_atk[-1]["Value"] for d in sim_card_list)) and \
                len(opponent_hand) > len(sim_card_list) + (len(table_atk) - len(table_def)):
            vision_hand()
            one_more = input("\nDo you want to attack with more cards? Type 'no' or the number of a card (1 to "
                             + str(len(hand)) + "): ")
            if one_more == 'no' or one_more == 'n':
                return False
            elif one_more.isdigit() is True and (int(one_more) in list(range(1, len(hand) + 1))) and \
                    hand[int(one_more) - 1] in sim_card_list:
                cardTransfer(hand[int(one_more) - 1], hand, table_atk)
                sim_card_list.remove(sim_card_list[sim_card_list.index(table_atk[-1])])
                return True
            else:
                return True
        else:
            return False
    elif bot_or_not == 'bot':
        while len(sim_card_list) > 0 and len(table_atk) < len(players_hand) + 1:
            if (table_atk[-1]["Value"] == sim_card_list[0].get("Value")) or \
                    (table_atk[-1]["Value"] == sim_card_list[0].get("Value") - 10) or \
                    (table_atk[-1]["Value"] == sim_card_list[0].get("Value") + 10) and \
                    len(opponent_hand) > len(table_atk) + len(table_def) + 1 and \
                    betterBots('attack', sim_card_list[0], table_atk[-1]) is True:
                #vision_full()
                cardTransfer(hand[hand.index(sim_card_list[0])], hand, table_atk)
                sim_card_list.remove(sim_card_list[0])
            else:
                sim_card_list.remove(sim_card_list[0])


# Function that realizes an attack sequence for a player or Bobby
def attack(who):
    breaker = False
    global p_atk_phase
    global who_atkd  # player 1, bobby 2, danny 3
    who_atkd = who
    p_atk_phase = True
    while p_atk_phase:
        if who_atkd == 3:
            attackPlayer()
            if not p_atk_phase:
                break
        elif who_atkd == 1:
            attackSI(bobbys_hand, "Bobby")
            who_atkd = 2
            p_atk_phase = False
        elif who_atkd == 2:
            attackSI(dannys_hand, "Danny")
            who_atkd = 3
            p_atk_phase = False
    vision_full()
    if not p_atk_phase:
        defense()
    if breaker: return


def attackSI(hand_si, si_name):
    global p_atk_phase
    global who_atkd
    hand_si.sort(key=lambda x: x["Value"])
    cardTransfer(hand_si[0], hand_si, table_atk)
    checkForSim(hand_si, table_atk)
    if who_atkd == 1:
        someMore('bot', hand_si, dannys_hand)
    elif who_atkd == 2:
        someMore('bot', hand_si, players_hand)
    if len(table_atk) == 1:
        print("\n++ " + si_name + " attacked with:", table_atk[0]["Name"], "! ++")
    else:
        print("\n++ " + si_name + " attacked with:", [d.get("Name") for d in table_atk], "! ++")


def attackPlayer():
    global who_atkd
    global p_atk_phase
    vision_hand()
    picked_atk = (
        input("\nPick a number of a card you want to play (from 1 to " + str(len(players_hand)) + "): "))
    if picked_atk.isdigit() and int(picked_atk) in list(range(1, len(players_hand) + 1)):
        cardTransfer(players_hand[int(picked_atk) - 1], players_hand, table_atk)
        checkForSim(players_hand, table_atk)
        while someMore('player', players_hand, bobbys_hand):
            if not someMore('player', players_hand, bobbys_hand):
                break
            someMore('player', players_hand, bobbys_hand)
        who_atkd = 1
        p_atk_phase = False
        #return p_atk_phase
    else:
        print("\nWrong value, pick a number between 1 and " + str(len(players_hand)) + " ")
    if breaker: return


def defensePlayer():
    global p_def_phase
    global who_atkd
    global if_odbit
    global took_cards
    took_cards = False
    p_hand_no_trump = players_hand.copy()
    for c in p_hand_no_trump:
        if c["Color"] == gl_col: p_hand_no_trump.remove(c)
    if all(d.get("Value") < table_atk[-1]["Value"] for d in players_hand) or (
            all(d.get("Color") != table_atk[-1]["Color"] for d in p_hand_no_trump)
            and len(p_hand_no_trump) == len(players_hand)):
        for j in range(0, len(table_atk)):
            cardTransfer(table_atk[0], table_atk, players_hand)
        for j in range(0, len(table_def)):
            cardTransfer(table_def[0], table_def, players_hand)
        print("\n== You have to take the cards! ==")
        players_hand.sort(key=lambda x: x["Value"])
        vision_full()
        took_cards = True
        if_odbit = False
        p_def_phase = False
        who_atkd = 1
    else:
        while len(table_atk) > len(table_def):
            picked_def = input("\nPick a card to defend against " + table_atk[len(table_def)]["Name"] +
                               ", or take the table (from 1 to " + str(len(players_hand)) + ", or \'take\'): ")
            if picked_def == 'take' or picked_def == 't':
                for j in range(0, len(table_atk)):
                    cardTransfer(table_atk[0], table_atk, players_hand)
                for j in range(0, len(table_def)):
                    cardTransfer(table_def[0], table_def, players_hand)
                print("\n== You have taken the cards! ==")
                players_hand.sort(key=lambda x: x["Value"])
                took_cards = True
                if_odbit = False
                p_def_phase = False
                who_atkd = 1
                break
            elif picked_def.isdigit() == True and int(picked_def) in range(1, len(players_hand) + 1):
                checkCard(table_atk[len(table_def)], players_hand[int(picked_def) - 1])
                if can_def:
                    cardTransfer(players_hand[int(picked_def) - 1], players_hand, table_def)
                    vision_full()
                    if len(table_atk) == len(table_def):
                        if_odbit = True
                        p_def_phase = False
                        who_atkd = 3
                else:
                    print("\n== Can't defend with that card, pick correct one or \'take\' ==")
                    vision_full()
            else:
                print("\n== Wrong value, pick a card to defend, or take the table (from 1 to " + str(
                    len(players_hand)) + ", or \'take\') ==")
                vision_full()
    if breaker: return


def defenseSI(si_hand, si_name):
    global p_def_phase
    global if_odbit
    global took_cards
    took_cards = False
    si_hand.sort(key=lambda x: x["Value"])
    can_def_cards = []
    if len(table_atk) == len(table_def):
        if_odbit = True
        p_def_phase = False
    else:
        for p in si_hand:
            checkCard(table_atk[len(table_def)], p)
            if can_def:
                can_def_cards.append(p)
                can_def_cards.sort(key=lambda x: x["Value"])
        if len(can_def_cards) == 0 or not betterBots('defense', can_def_cards[0], table_atk[len(table_def)]):
            for j in range(0, len(table_atk)): cardTransfer(table_atk[0], table_atk, si_hand)
            for j in range(0, len(table_def)): cardTransfer(table_def[0], table_def, si_hand)
            print("\n++ " + si_name + " took the cards! ++")
            si_hand.sort(key=lambda x: x["Value"])
            took_cards = True
            if_odbit = False
            p_def_phase = False
        elif len(can_def_cards) != 0 and betterBots('defense', can_def_cards[0], table_atk[len(table_def)]):
            cardTransfer(si_hand[si_hand.index(can_def_cards[0])], si_hand, table_def)
            print("\n++ " + si_name + " defended with " + table_def[-1]["Name"] + "! ++")
            vision_full()
            if_odbit = False
            p_def_phase = True
    if breaker: return


# Function that realizes a defense sequence
def defense():
    global breaker
    global p_def_phase
    global took_cards
    p_def_phase = True
    global who_atkd
    global if_odbit
    while p_def_phase:
        if who_atkd == 3:  # PLAYER DEFENDS
            defensePlayer()
        elif who_atkd == 1:  # BOBBY DEFENDS
            defenseSI(bobbys_hand, "Bobby")
            if took_cards: who_atkd = 2
            else: who_atkd = 1
        elif who_atkd == 2:  # DANNY DEFENDS
            defenseSI(dannys_hand, "Danny")
            if took_cards:
                who_atkd = 3
            else:
                who_atkd = 2
    if if_odbit:
        discards()
    elif not if_odbit:
        endOfTurn()
    if breaker: return


def discardsPlayer():
    global if_odbit
    global discard_flag
    if (not checkForSim(players_hand, table_atk) and not checkForSim(players_hand, table_def)) \
            or len(table_atk) == 5 or len(bobbys_hand) <= 1:
        table_atk.clear()
        table_def.clear()
        print("\n== Cards are discarded, can't counter ==")
        if_odbit = False
        discard_flag = 0
    else:
        '''cards_to_counter = []
        for c in players_hand:
            for t in table_atk:
                if c["Value"] == t["Value"] or c["Value"] == t["Value"] + 10 or c["Value"] == t["Value"] - 10:
                    cards_to_counter.append(c)
            for t in table_def:
                if (c["Value"] == t["Value"] or c["Value"] == t["Value"] + 10 or c["Value"] == t["Value"] - 10) \
                        and (c not in cards_to_counter):
                    cards_to_counter.append(c)'''

        checkForSim(players_hand, table_atk)
        cards_to_counter = []
        cards_to_counter = sim_card_list.copy()
        checkForSim(players_hand, table_def)
        cards_to_counter.extend(sim_card_list)
        cards_to_counter.sort(key=lambda x: x["Value"])

        odbit = input("\nYou discard or counter attack? (type 'o' or a number of a card to play): ")
        if odbit == "odbit" or odbit == "o" or odbit == "n" or odbit == "d":
            discard_flag = 0
        elif (odbit.isdigit() is True) and (int(odbit) in range(1, len(players_hand) + 1)) and \
                (len(cards_to_counter) > 0) and (players_hand[int(odbit) - 1] in cards_to_counter):
            cardTransfer(players_hand[int(odbit) - 1], players_hand, table_atk)
            discard_flag = 1
            vision_full()
        else:
            print("\n== You can't do that! ==")
            vision_full()


def discardsSI(si_hand, si_name):
    global if_odbit
    global discard_flag2
    if (not checkForSim(si_hand, table_atk) and not checkForSim(si_hand, table_def)) \
            or len(table_atk) == 5 or len(players_hand) <= 1 or \
            any([betterBots('attack', d, table_atk[-1]) for d in sim_card_list]) is False or \
            any([betterBots('attack', d, table_def[-1]) for d in sim_card_list]) is False:
        print("\n++ Cards are discarded by " + si_name + " ++")
        discard_flag2 = 0
    else:

        cards_to_counter = []
        '''for c in si_hand:
            for t in table_atk:
                if c["Value"] == t["Value"] or c["Value"] == t["Value"] + 10 or c["Value"] == t["Value"] - 10:
                    cards_to_counter.append(c)
            for t in table_def:
                if (c["Value"] == t["Value"] or c["Value"] == t["Value"] + 10 or c["Value"] == t["Value"] - 10) \
                        and (c not in cards_to_counter):
                    cards_to_counter.append(c)'''

        checkForSim(si_hand, table_atk)
        cards_to_counter = []
        cards_to_counter = sim_card_list.copy()
        checkForSim(si_hand, table_def)
        cards_to_counter.extend(sim_card_list)

        cards_to_counter.sort(key=lambda x: x["Value"])
        cardTransfer(si_hand[si_hand.index(cards_to_counter[0])], si_hand, table_atk)
        print("\n++ " + si_name + " counter attacked with " + table_atk[-1]["Name"] + "! ++")
        vision_full()
        discard_flag2 = 1


# Function realiseing discard phase (counter attacking or discarding the table)
def discards():
    global who_atkd
    global breaker
    global if_odbit
    while if_odbit:
        if who_atkd == 1 and (len(table_atk) != 0 and len(table_def) != 0):  # PLAYER ATTACKED
            discardsPlayer()
            if len(table_atk) < 5 and len(bobbys_hand) > 1:
                discardsSI(dannys_hand, "Danny")
            who_atkd = 1
        elif who_atkd == 2:  # BOBBY ATTACKED
            discardsSI(bobbys_hand, "Bobby")
            if len(table_atk) < 5 and len(bobbys_hand) > 1:
                discardsPlayer()
            who_atkd = 2
        elif who_atkd == 3:
            discardsSI(dannys_hand, "Danny")
            if len(table_atk) < 5 and len(bobbys_hand) > 1:
                discardsSI(bobbys_hand, "Bobby")
            who_atkd = 3
        if discard_flag + discard_flag2 == 0:
            table_atk.clear()
            table_def.clear()
            vision_full()
            if_odbit = False
            endOfTurn()
        elif discard_flag + discard_flag2 != 0:
            defense()
    if breaker: return


# Function that ends the turn (card draw and killing running nested functions)
def endOfTurn():
    deck_empty = False
    global breaker
    p_draw = 6 - len(players_hand)
    while (len(players_hand) != 6 or len(bobbys_hand) != 6 or len(dannys_hand) != 6) and not deck_empty:
        min_hand = min([players_hand, bobbys_hand, dannys_hand], key=len)
        if len(deck) > 0 and len(min_hand) < 6:
            cardTransfer(deck[0], deck, min_hand)
        elif len(deck) == 0:
            deck_empty = True
        else:
            break
    players_hand.sort(key=lambda x: x["Value"])
    bobbys_hand.sort(key=lambda x: x["Value"])
    dannys_hand.sort(key=lambda x: x["Value"])
    if not deck_empty:
        print("\n== End of turn. You drew " + str(max(p_draw, 0)) + " cards ==\n")
    elif deck_empty:
        print("\n== End of turn. Deck empty. You drew " + str(0) + " cards ==\n")
    print(len(deck), " cards left")
    # vision_hand()
    breaker = True
    return


#who_starts = random.randint(1, 3)
who_starts = 3
#sys.setrecursionlimit(2000)
startGame()
attack(who_starts)
while len(players_hand) > 0 and len(bobbys_hand) > 0 and len(dannys_hand) > 0:
    if breaker: attack(who_atkd)
if len(players_hand) == 0 and len(bobbys_hand) != 0 and len(dannys_hand) != 0:
    print("\n\n=== YOU WON!!! CONGRATULATIONS!!! ===\n")
    sys.exit()
elif len(bobbys_hand) == 0 and len(players_hand) != 0 and len(dannys_hand) != 0:
    print("\n\n+++ BOBBY WON!!! BETTER LUCK NEXT TIME! +++\n")
    sys.exit()
elif len(dannys_hand) == 0 and len(players_hand) != 0 and len(bobbys_hand) != 0:
    print("\n\n+++ DANNY WON!!! BETTER LUCK NEXT TIME! +++\n")
    sys.exit()
else:
    if len(players_hand) == 0 and len(bobbys_hand) == 0 and len(dannys_hand) == 0:
        print("\n\n=+= IT'S A TIE!!! BETTER LUCK NEXT TIME! +=+\n")
        sys.exit()
    elif max(players_hand, bobbys_hand, dannys_hand) == players_hand:
        loser = "YOU"
    elif max(players_hand, bobbys_hand, dannys_hand) == bobbys_hand:
        loser = "BOBBY"
    elif max(players_hand, bobbys_hand, dannys_hand) == dannys_hand:
        loser = "DANNY"
    print("\n\n=+= TWO PLAYERS TIE, THE LOSER - " + loser)
    sys.exit()

