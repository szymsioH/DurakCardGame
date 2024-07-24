# DurakCardGame
My attempt at creating simple code in Python simulating a Durak card game.

## Concept of a program:
I want to create a simple script that would simualte a single Durak card game round between two players - one human, and one AI (called Bobby). Game should simulate all basic rules like the ones specyfying the defense, order of drawing cards, the power of the trump cards etc. For now, Bobby will make random decisions, but his moves must be compliant with the rules. The game would proceed till the victory of one of the players. Also, for now the game will be played via command window inputs.

## Goals and Plans
Here are my plans for this project. Start with the bare minimum, end with a very ambitious plans for the future!

**Minimum:**
- [x]  Game is played entirelly via cmd.
- [x]  Easiest version of the game - you can attack with only one card, first player to empty his hand wins.
- [x]  One human player can play against one bot player - Bobby. Bobby would make simple decisions, he'll always attack with his weakest card, and will always try to defend himself from taking additional cards.

**Simple Go To:**
- [x]  Adding a possibility to attack with more than 1 card of the same value.
- [x]  Adding a possibility to attack again if the card on the table has the same value as our new attacking card.
- [ ]  Adding more SI players.
- [ ]  SI players will make smarter decisions (not defending with a too strong card).

**Ambitious Plans:**
- [ ]  Create a simple GUI.
- [ ]  Make the SI even better - look for some algorithms for most optimised Durak game.
- [ ]  Implement mashine learning into SI's decision making.
