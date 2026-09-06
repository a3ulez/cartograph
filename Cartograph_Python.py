#IMPORTS
import itertools, random
import json
from datetime import datetime
#imports dialog box option
import tkinter as tk
from tkinter import filedialog
# Prevent an empty Tkinter window from popping up
root = tk.Tk()
root.withdraw()

#CLASSES
class Game:
    
    #Current time variable for creation of unique file name at Game object creation
    now = datetime.now()

    def __init__(self, file_name = now.strftime("%Y-%m-%d_%H-%M") + ".json",
                 deck=None, discard=None, red_jokers=0,
                 black_jokers=0,cards_remaining = 54, current_card = None,
                 var_save=None, last_saved="Unsaved"):

        self.file_name = file_name
        self.deck = deck if deck is not None else ["Ace of Hearts", "Ace of Diamonds", "Ace of Spades",
                                                   "Ace of Clubs", "King of Hearts", "King of Diamonds",
                                                   "King of Spades", "King of Clubs", "Queen of Hearts",
                                                   "Queen of Diamonds", "Queen of Spades", "Queen of Clubs",
                                                   "Jack of Hearts", "Jack of Diamonds", "Jack of Spades",
                                                   "Jack of Clubs", "10 of Hearts", "10 of Diamonds",
                                                   "10 of Spades", "10 of Clubs", "9 of Hearts", "9 of Diamonds",
                                                   "9 of Spades", "9 of Clubs", "8 of Hearts", "8 of Diamonds",
                                                   "8 of Spades", "8 of Clubs", "7 of Hearts", "7 of Diamonds",
                                                   "7 of Spades", "7 of Clubs", "6 of Hearts", "6 of Diamonds",
                                                   "6 of Spades", "6 of Clubs", "5 of Hearts", "5 of Diamonds",
                                                   "5 of Spades", "5 of Clubs", "4 of Hearts", "4 of Diamonds",
                                                   "4 of Spades", "4 of Clubs", "3 of Hearts", "3 of Diamonds",
                                                   "3 of Spades", "3 of Clubs", "2 of Hearts", "2 of Diamonds",
                                                   "2 of Spades", "2 of Clubs", "Red Joker", "Black Joker"]
        self.discard = discard if discard is not None else []
        self.red_jokers = int(red_jokers)
        self.black_jokers = int(black_jokers)
        self.cards_remaining = int(cards_remaining)
        self.current_card = current_card if current_card is not None else "Empty"
        self.var_save = var_save if var_save is not None else {}
        self.last_saved = last_saved
        random.shuffle(self.deck)

    #----CLASS METHODS----
   
    #RENAME GAME FILE - Default file_name is the YYYY-MM-DD_HH-MM.json
    #Gives the player the option to change the name to something recognizable
    def rename_game(self):
        print(f"Your current file is {self.file_name}. Keep name?\n")
        rename = int(input("1 = Yes    2 = No, rename it\n"))
        if rename == 2:
            self.file_name = input("\nType a name for your save file with no spaces.\n")
            self.file_name += ".json"
        else:
            pass
        print(f"\nYour game file is named {self.file_name}\n")


    #SAVE GAME - Write current variable settings to a JSON file with current
    #game file_name
    def save_game(self):
        self.var_save = {
            "file_name": self.file_name,
            "deck": self.deck,
            "discard": self.discard,
            "red_jokers": self.red_jokers,
            "black_jokers": self.black_jokers,
            "cards_remaining": self.cards_remaining,
            "curent_card": self.current_card,
            "last_saved": self.last_saved
        }
    
        with open(self.file_name, "w", encoding="utf-8") as file:
            json.dump(self.var_save, file, indent=4)

        self.last_saved = self.now.strftime("%Y-%m-%d %H:%M")
    
        print(f"Successfully saved game to {self.file_name}\n")

    #QUIT GAME - checks for last save point and gives option to save, quits game
    def quit_game(self):
        #Check for last save point
        print(f"\nGame last saved {self.last_saved}\n")
        print("Save game?\n")
        while is_save not in [1,2]:
            is_save = int(input("1 = Save   2 = Quit\n"))
        if is_save == 1:
            save_game(self)
        else:
            print("\n\nQuitting Game\n\n")
        
    #EXPAND DECK - Adds a full, shuffled deck to the existing deck and shuffles deck.
    #This will add 2 more jokers, increasing the risk of continuing a game
    def expand_deck(self):
        default_deck = ["Ace of Hearts","Ace of Diamonds","Ace of Spades","Ace of Clubs","King of Hearts","King of Diamonds",
                        "King of Spades","King of Clubs","Queen of Hearts","Queen of Diamonds","Queen of Spades","Queen of Clubs",
                        "Jack of Hearts", "Jack of Diamonds", "Jack of Spades","Jack of Clubs", "10 of Hearts", "10 of Diamonds",
                        "10 of Spades", "10 of Clubs", "9 of Hearts", "9 of Diamonds","9 of Spades", "9 of Clubs", "8 of Hearts",
                        "8 of Diamonds","8 of Spades", "8 of Clubs", "7 of Hearts", "7 of Diamonds","7 of Spades", "7 of Clubs",
                        "6 of Hearts","6 of Diamonds","6 of Spades", "6 of Clubs", "5 of Hearts", "5 of Diamonds","5 of Spades",
                        "5 of Clubs", "4 of Hearts", "4 of Diamonds","4 of Spades", "4 of Clubs", "3 of Hearts", "3 of Diamonds",
                        "3 of Spades", "3 of Clubs", "2 of Hearts", "2 of Diamonds","2 of Spades", "2 of Clubs",
                        "Red Joker", "Black Joker"]
        for card in self.deck:
            default_deck.append(card)
        self.deck = default_deck
        self.cards_remaining = len(self.deck)
        random.shuffle(self.deck)
        print("Deck refreshed - continuing now\n\n")


    #DRAW CARD - checks if there are enough non-jokers to draw a card and gives
    #option to expand deck. Resolves joker if drawn, displays drawn card,
    #discards drawn non-joker and decrements cards remaining for each
    def draw_card(self, num_draws):
        #variable to error check user input
        game_status = 0
        #Check that there are enough cards and give option to expand deck
        if self.cards_remaining < 5:
            while game_status not in [1,2]:
                print(f"You're running out of cards. Current cards remaining: {self.cards_remaining}")
                game_status = int(input("\nPress 1 to shuffle in a new deck. Press 2 to save and quit\n"))
            if game_status == 1:
                self.expand_deck()
            else:
                self.save_game()
                self.quit_game()

        #Loop to draw card while draws remain
        while num_draws > 0:
            #Set current card to top of deck
            self.current_card = self.deck[0]

            #If Joker, resolve, shuffle, and redraw, check if new card is joker
            while self.current_card in ["Red Joker","Black Joker"]:
                to_resolve = True
                self.resolve_joker()
                #Shuffle Joker back in
                random.shuffle(self.deck)
                to_resolve = False
                self.current_card = self.deck[0]

            #Remove drawn card from deck and add it to the discard pile
            self.discard.append(self.deck.pop(0))
            #Decrement cards remaining
            self.cards_remaining -= 1
        
            #Display drawn card
            print(self.current_card)
            
            #Decrement number of draws
            num_draws -= 1


    #RESOLVE JOKER: When a joker has been drawn, the sum of jokers will update. 
    #When the sum of either joker reaches 3, the game ends, or the player has
    #the option to reduce the number of jokers to continue playing
    def resolve_joker(self):
        continue_game = 0

        print(f"\n{self.current_card} drawn! Catastrophe strikes!\n\n")
        
        #update joker sum
        if self.current_card == "Red Joker":
            self.red_jokers += 1
            print(f"Red Joker total now {self.red_jokers}\n")
            input("Discuss what happened. Then, press Enter to continue\n\n")
        else:
            self.black_jokers += 1
            print(f"Black Joker total now {self.black_jokers}\n")
            input("Discuss what happened. Then, press Enter to continue\n\n")
        
        #3 Jokers = Game Over?
        if self.red_jokers > 2:
            print("Captured! Continue Game?\n\n")
            while continue_game not in [1,2]:
                continue_game = int(input("Press 1 to Continue   OR    Press 2 to Save and Quit\n\n"))
            if continue_game == 1:
                print("Red Jokers reduced to 2. The game goes on!\n\n")
                self.red_jokers = 2
                return

            else:
                self.save_game()
                self.quit_game()

        
        if self.black_jokers > 2:
            print("Fatality! Continue Game?\n\n")
            while continue_game not in [1,2]:
                continue_game = int(input("Press 1 to Continue   OR    Press 2 to Save and Quit\n\n"))
            if continue_game == 1:
                print("Black Jokers reduced to 2. The game goes on!\n\n")
                self.black_jokers = 2
                return

            else:
                self.save_game()
    


#FUNCTIONS
#Function to play a round
def PlayRound(current_game, is_play):
    #Variables to error check user input
    can_shop = 0
    is_quit = 0
    is_save = 0

    print("\n\n\nSTARTING ROUND!\n\n\n")
    #Draw Journey Card
    print("Draw a card to describe your journey to the next destination\n")
    Game.draw_card(current_game,1)
    input("\nPress enter to continue\n")

    #Weather
    print("\n\nDon't forget about the weather!")
    if len(current_game.discard) > 1:
        #If more than 1 card is in the discard pile, give current and previous card
        print(f"Your first weather card is {current_game.discard[-2]}, and your other weather card is {current_game.current_card}.\n")
    elif len(current_game.discard) <=1:
        print(f"Your only weather card is {current_game.current_card}.\n")
    input("\nPress enter to continue\n")

    #Draw setting card for destination
    print("\nDraw a card to describe your destination\n\n")
    Game.draw_card(current_game,1)
    input("\nPress enter to continue\n")

    #Shopping
    while can_shop not in [1,2]:
        can_shop = int(input('Enter 1 if you are in a city and can shop. Otherwise enter 2 to continue.'))
    if can_shop == 1:
        Game.draw_card(current_game,4)

    #Continue or Save and Quit
    print("\n\nEnd of the Round - Continue to Next Round or Save?")
    while is_save not in [1,2]:
        is_save = int(input('\nPress 1 to Continue    OR     Press 2 to Save\n\n'))
    if is_save == 2:
        current_game.save_game()
        while is_quit not in [1,2]:
            is_quit = int(input('\nPress 1 to Continue    OR     Press 2 to Quit\n\n'))
            if is_quit == 2:
                is_play = 0
        
    return(is_play)


def main():
#-------- START GAME --------

    #---VARIABLES---
    current_game = None
    is_new_game = 0
    is_play = 1
    var_save = None
    saved_vars = None

    #Check if new game or loaded game
    while is_new_game not in [1,2]:
        is_new_game = int(input('\nEnter 1 for New Game. Enter 2 to Load Game\n'))

    #If new game is chosen, create a new Game object
    if is_new_game == 1:
        current_game = Game()
        print("\nGive your game session a name.\n\n")
        Game.rename_game(current_game)
        Game.save_game(current_game)
        input("\nPress enter to continue...\n")


    #If existing game is chosen, load game variables from file into current_game object
    if is_new_game == 2:

        #Open the file browser dialog window
        file_path = filedialog.askopenfilename(
            title="Select a .JSON File",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )

        #Check if the user selected a file or cancelled
        if file_path:
            try:
                #Load in variables from file
                with open(file_path, "r") as file:
                    saved_vars = json.load(file)
                file_name = saved_vars.get("file_name")
                deck = saved_vars.get("deck")
                discard = saved_vars.get("discard")
                red_jokers = saved_vars.get("red_jokers")
                black_jokers = saved_vars.get("black_jokers")
                cards_remaining = saved_vars.get("cards_remaining")
                current_card = saved_vars.get("current_card")
                last_saved = saved_vars.get("last_saved")
                var_save = {
                    "file_name": file_name,
                    "deck": deck,
                    "discard": discard,
                    "red_jokers": red_jokers,
                    "black_jokers": black_jokers,
                    "cards_remaining": cards_remaining,
                    "curent_card": current_card,
                    "last_saved": last_saved
                }

                #Create Game object from saved variables
                current_game = Game(file_name, deck, discard, red_jokers,
                                    black_jokers, cards_remaining, current_card,
                                    var_save, last_saved)

            
                print(f"\n\nGame data loaded:{saved_vars}\n")
                input("\nPress enter to continue...\n")

            #Error checking for file issue
            except Exception as e:
                print(f"An error occurred: {e}")

        else:
            print("No file was selected.")

    #While player chooses to continue, loop PlayRound method.
    #PlayRound ends with option to stop playing, which updates is_play
    while is_play == 1:
        is_play = PlayRound(current_game,is_play)

    #Save game after PlayRound finishes, exit
    current_game.save_game()
    exit()

#Activate main()
if __name__ == "__main__":
    main()
