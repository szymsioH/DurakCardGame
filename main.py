from random import shuffle


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

def cardTransfer(what, from_p, to_p):
    from_p.remove(what)
    to_p.append(what)

players_hand = []
bobbys_hand = []

gone_cards = []

def startGame():
    shuffle(deck)
    [cardTransfer(deck[0], deck, players_hand) for _ in range(6)]
    [cardTransfer(deck[0], deck, bobbys_hand) for _ in range(6)]
    print([p["Name"] for p in players_hand])
    print([p["Name"] for p in bobbys_hand])
    print(len(deck))

startGame()




