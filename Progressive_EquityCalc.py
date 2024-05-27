
from deck_of_cards import deck_of_cards
import sys
import os
from colorama import Fore, Back, Style, init
import time
import os

from Functions import hand_evaluator

init()
global spade,heart,diamond,club,gamesettings,convert_val_to_icon
spade = Style.DIM + "♠️" + Style.RESET_ALL
club = Style.DIM + "♣️" + Style.RESET_ALL
heart  = Fore.RED + "♥️" + Style.RESET_ALL
diamond = Fore.RED + "♦️" + Style.RESET_ALL
print(spade,heart,diamond,club)
convert_val_to_icon = {
    '0' : spade,
    '1' : heart,
    '2' : diamond,
    '3' : club,
    2 : 2,
    3 : 3,
    4 : 4,
    5 : 5,
    6 : 6,
    7 : 7,
    8 : 8,
    9 : 9,
    10 : 10,
    11 : 'J',
    12 : 'Q',
    13 : 'K',
    14 : 'A',
    }
class Game:
    def __init__(self, players, random_cards, stage,communitycards):
        self.players = players
        self.random_cards = random_cards
        self.stage = stage
        self.communitycards = communitycards
        
    def update_players(self, new_players):
        self.players = new_players

    def update_random(self, new_random_cards):
        self.random_cards = new_random_cards

    def update_stage(self, new_stage):
        self.stage = new_stage

    def get_players(self):
        return self.players

    def get_random(self):
        return self.random_cards

    def get_stage(self):
        return self.stage
    
    def get_communitycards(self):
        return self.communitycards
    def update_communitycards(self,new_communitycards):
        self.communitycards = new_communitycards
gamesettings = Game(players=6, random_cards=True, stage=0,communitycards=[])
class Player:
    def __init__(self, card1, card2, winodds,showwinodds,besthand):
        self.card1 = card1
        self.card2 = card2
        self.winodds = winodds
        self.showwinodds = showwinodds
        self.besthand = besthand
        
    
    
    def get_card1(self):
        return self.card1

    def get_card2(self):
        return self.card2
    
    def get_winodds(self):
        return self.winodds
    def update_winodds(self, new_winodds):
        self.winodds = new_winodds
        
    def get_showwinodds(self):
        return self.showwinodds
    def update_showwinodds(self, new_showwinodds):
        self.showwinodds = new_showwinodds
        
    def get_besthand(self):
        return self.besthand
    def update_besthand(self,new_besthand):
        self.besthand = new_besthand 

def startmenu():
    os.system('cls')
    print('',spade,club,heart,diamond,"\nPoker Hand Win Odds Calculator\n",spade,club,heart,diamond)
    print("Menu Options: \n 1/ Start Game",spade,"  \n 2/ Customise Game Settings",heart," \n 3/ Exit",diamond," \n Select Respective Number for Setting: \n")
    while True:
        menuselection = input("= ")
        if menuselection == "1":
            startgame()
            break
        elif menuselection == "2":
            changegamesettings()
            break
        elif menuselection == "3":
            sys.exit()
        else:
            print("Ensure Entry is a Valid Number")
    sys.exit()

def givecard() -> deck_of_cards:
    if gamesettings.get_random() == True:
        while True:
            card = deck_obj.give_random_card()
            if card.value == 1:
                card.value = 14
            takencards.append(str(card.value)+str(card.suit))
            suits[card.suit] -= 1
            vals[card.value-2] -= 1
            return card
    else:
        while True:
            wantedval = enterval()
            wantedsuit = entersuit()
            if str(wantedval) + str(wantedsuit) not in takencards:
                while True:
                    card = deck_obj.give_random_card()
                    if card.value == 1:
                        card.value = 14
                    if card.suit == wantedsuit and card.value == wantedval:
                        takencards.append(str(wantedval) + str(wantedsuit))
                        return card
                    else:
                        if card.value == 14:
                            card.value = 1
                        deck_obj.take_card(card)
            else:
                print("Card Already Taken from Deck")

def changegamesettings():
    os.system('cls')
    print(spade,club,heart,diamond)
    print("Current Game Settings: \n Players:", gamesettings.get_players(), "\n Random Cards:", gamesettings.get_random(), "\n Stage of game:", gamesettings.get_stage())
    print("Change: \n 1/ Players",heart," \n 2/ Random Cards",spade," \n 3/ Stage of Game",diamond," \n4/ Exit",club," \n")
    change = input("= ")
    if change == "1":
        gamesettings.update_players(validateplayers("~~~ Enter Number of Players (Min 2 : Max 23) ~~~ \n",0,24))
    elif change == "2":
        validaterandom()
    elif change == "3":
        gamesettings.update_stage(validatestage())
    else:
        startmenu()
    changegamesettings()

def validateplayers(statement,sub,bound) -> int:
    global newplayers
    while True:
        try:
            print(statement)
            newplayers = int(input("= "))
            if 1 + sub < newplayers < bound:
                return newplayers
            else:
                print("Ensure Valid Number of Players")
        except Exception as e:
            print("Ensure Valid Number of Players")

def validaterandom():
    while True:
        try:
            print("~~~ Enter 1 for Random Cards, 0 for Custom Cards ~~~")
            newrandom = int(input("= "))
            if newrandom == 0:
                gamesettings.update_random(False)
                break
            elif newrandom == 1:
                gamesettings.update_random(True)
                break
            else:
                print("Ensure Valid Boolean 0 or 1")
        except Exception as e:
            print("Ensure Correct Input Type 0 or 1")

def validatestage():
    while True:
        try:
            print("~~~ Enter stage of the game (0-3) ~~~")
            newstage = int(input("= "))
            if 0 <= newstage < 7:
                return newstage
            else:
                print("Ensure Valid Stage Number")
        except Exception as e:
            print("Ensure Valid Stage Number")          

def enterval():
    print("\nEnter Card Value (2-14)(For J = 11, Q = 12, K = 13, A = 14):")
    while True:
        try:
            val = int(input("= "))
            if 1 < val < 15:
                return val
            else:
                print("Ensure Valid Card Value")
        except Exception as e:
            print("Ensure Valid Card Value")

def entersuit() -> int:
    print("Enter Card Suit (0:S,1:H,2:D,3:C):")
    while True:
        try:
            suit = int(input("= "))
            if 0 <= suit < 4:
                return suit
            else:
                print("Ensure Valid Card Suit")
        except Exception as e:
            print("Ensure Valid Card Suit")   

def fixcardval(val : int) -> int:
    return 14 if val == 1 else val

def validatechoice(lowerbound,upperbound) -> int:
    while True:
        try:
            choice = int(input("= "))
            if lowerbound <= choice <= upperbound:
                return choice
            else:
                print("\nEnter a Valid Choice\n")
        except:
            print("\nEnter a Valid Choice\n")

def startgame():
    global suits,vals,takencards, communitycards,Players
    takencards = []
    communitycards = []
    suits = [13,13,13,13]
    vals = [
    4,4,4,4,4,4,4,4,4,4,4,4,4]
    os.system('cls')
    print(spade,club,heart,diamond)
    global deck_obj, Players
    deck_obj = deck_of_cards.DeckOfCards()
    Players = initialiseplayercards()
    simulatestage(gamesettings.get_stage())

def print_currentplayercards():
    print(spade,heart,diamond,club)
    print("~~ Current Player Cards : \n")
    for i in range(0,gamesettings.get_players()):
        if Players[i].get_showwinodds() == False:
            show = ''
        else:
            show = "👑 Win Odds : "+ str(Players[i].get_winodds())
        print("Player",i+1,"cards:",convert_val_to_icon[Players[i].get_card1().value],convert_val_to_icon[str(Players[i].get_card1().suit)],",",convert_val_to_icon[Players[i].get_card2().value],convert_val_to_icon[str(Players[i].get_card2().suit)],show)
def initialiseplayercards() -> list[Player]:
    chosefor = 0
    Players = []
    temp = gamesettings.get_random()
    if gamesettings.get_random() == False:
        chosefor = validateplayers("~~~ Select How Many Players Cards you would like to Chose: ~~~",-2,gamesettings.get_players()+1)
    for i in range(0,gamesettings.get_players()):
        gamesettings.update_random(True)
        if i < chosefor:    
            print("~~~ Enter Player",i + 1,"Card 1 and Card 2")
            gamesettings.update_random(False)
        card1 = givecard()
        card2 = givecard()
        Players.append(Player(card1,card2,0.000,False,False))
    gamesettings.update_random(temp)
    return Players

def ViewHideallwinrates(View : bool):
    for i in range(0,gamesettings.get_players()):
        Players[i].update_showwinodds(View)

def ViewHidewinrate(View : bool):
    show = {
        True : 'Show',
        False : 'Hide'}
    while True:
        try:
            x = gamesettings.get_players()
            playertoShowHide = int(input("\nWhich Player's Win Rate would you like to "+show[View]+" (1 - "+str(x)+"):\n= "))
            if 0 < playertoShowHide < gamesettings.get_players()+1:
                break
            else:
                print("\n~~ Select a Player in the Correct Range ~~")
        except:
            print("\n~~ Select a Player ~~")
    Players[playertoShowHide-1].update_showwinodds(View)

def winoddssettings():
    while True:
        try:    
            selection = int(input(
        "\nSelect an Option:\n"
        "1/ View all Win Rates {}\n"
        "2/ View a Selected Win Rate {}\n"
        "3/ Hide all Win Rates {}\n"
        "4/ Hide a Selected Win Rate {}\n"
        "5/ Exit {}\n= ".format(spade, heart, diamond, club, spade)
    ))
            if 0 < selection < 5:
                function_map = {
                1: lambda : ViewHideallwinrates(True),
                2: lambda : ViewHidewinrate(True),
                3: lambda : ViewHideallwinrates(False),
                4: lambda : ViewHidewinrate(False),
                5: lambda : sys.exit()
                }

                selected_function = function_map.get(selection)
                selected_function()
                break
            else:
                print("\n~~ Select a Valid Option ~~")

        except:
            print("\n~~ Select a Valid Option ~~")

def Foldplayer():
    x = gamesettings.get_players()    
    while True:
        if x < 3:
            print("\n~~~ Cannot Fold Any More Players (Enter to Continue) ~~~\n")
            input()
            break
        try:
            x = gamesettings.get_players()
            playertofold = int(input("\nWhich Player would you like to fold (1 - "+str(x)+")(0 for No Fold):\n= "))
            if playertofold == 0:
                break
            elif 0 < playertofold < gamesettings.get_players()+1:
                gamesettings.update_players(x-1)
                del Players[playertofold-1]
                break
            else:
                print("\n~~ Select a Player in the Correct Range ~~")
        except:
            print("\n~~ Select a Player ~~")

def makeallcardsarray(player : Player) -> list:
    C = [player.get_card1(),player.get_card2()]
    for i in range(0,len(gamesettings.get_communitycards())):
        C.append(gamesettings.get_communitycards()[i])
    return C

def putcards_backindeck():
    for i in range(0,len(gamesettings.get_communitycards())):
        x = gamesettings.get_communitycards().pop()
        takencards.remove(str(x.value) + str(x.suit))
        deck_obj.take_card(x)

def simulatestage(stage : int):
    os.system('cls')
    global communitycards
    print("~~Current Stage :",stage)
    print_currentplayercards()
    if stage == -1:
        return startmenu()
    elif stage == 0:
        putcards_backindeck()
        gamesettings.update_communitycards([])
    else:
        if len(gamesettings.get_communitycards()) == 0:
            gamesettings.update_communitycards([givecard(),givecard(),givecard()])
        
        while len(gamesettings.get_communitycards())-2 > stage:
            x = gamesettings.get_communitycards().pop()
            deck_obj.take_card(x)
            takencards.remove(str(x.value) + str(x.suit))
        while len(gamesettings.get_communitycards())-2 < stage:
           gamesettings.get_communitycards().append(givecard())
    playerscards_array = []
    for p in Players:
        playerscards_array.append(makeallcardsarray(p))

    #getwinodds(stage)


    if gamesettings.get_random() == False:
       os.system('cls')
       print("~~Current Stage :",stage)
       print_currentplayercards()
    if stage == 3:
        print("The winner is Player: ",hand_evaluator.evaluate_hand(playerscards_array))
    if stage != 0:
        print("\n~~ Community Cards ~~\n")
        comprint = '        |'
        for i in range(0,len(gamesettings.get_communitycards())):
            comprint = comprint + str(convert_val_to_icon[gamesettings.get_communitycards()[i].value]) +convert_val_to_icon[str(gamesettings.get_communitycards()[i].suit)] + '|' 
        print(comprint,"\n")
              

 

    print("\nMenu Options: \n 1/ Finish Stage(Continue)",spade,"  \n 2/ View Current Win Odds",heart," \n 3/ BackTrack",diamond," \n 4/ Fold a Player",club," \n 5/ Change Random Cards",club," \n 6/ End Program",spade," \n Select Respective Number for Setting: \n")
    
    choice = validatechoice(1,6)
    if choice == 1 and stage == 3:
        sys.exit()
    
    function_map = {
        1: lambda : simulatestage(stage+1),
        2: winoddssettings,
        3: lambda : simulatestage(stage-1),
        4: Foldplayer,
        5: validaterandom,
        6 : sys.exit
        }

    selected_function = function_map.get(choice)
    selected_function()
    
    if choice == 5 or choice == 4 or choice == 2:
        return simulatestage(stage)
    
def getwinodds(stage : int):
    pass
    
def testing():
    pass

startmenu()
#print(testing())