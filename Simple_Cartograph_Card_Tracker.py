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
                 var_save=None, day_number=1, to_resolve=None, last_saved="Unsaved"):

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
        self.discard = discard if discard is not None else {}
        self.red_jokers = int(red_jokers)
        self.black_jokers = int(black_jokers)
        self.cards_remaining = int(cards_remaining)
        self.current_card = current_card if current_card is not None else "Empty"
        self.var_save = var_save if var_save is not None else {}
        self.day_number = int(day_number)
        self.to_resolve = to_resolve if to_resolve is not None else []
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
            "day_number": self.day_number,
            "last_saved": self.last_saved
        }
    
        with open(self.file_name, "w", encoding="utf-8") as file:
            json.dump(self.var_save, file, indent=4)

        self.last_saved = self.now.strftime("%Y-%m-%d %H:%M")
    
    #QUIT GAME - checks for last save point and gives option to save, quits game
    def quit_game(self):
        print("\n\nQuitting Game\n\n")
        exit()
        
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

    #PRINT DRAWN CARDS BY DAY
    def print_draws(self):
        for day, card in self.discard.items():
            print(f"Day {day}: {card}\n")


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
                self.to_resolve.append(self.current_card)
                self.resolve_joker()
                self.deck.pop(0) #Pop joker from deck
                self.current_card = self.deck[0]
                
            #Display drawn card
            print(self.current_card)
            
            #Remove drawn card from deck
            self.deck.pop(0)
            #Add current card to drawn cards/discard pile
            if self.day_number in self.discard: #Check if current day is already listed in the drawn cards
                self.discard[self.day_number].append(self.current_card)
            else:
                self.discard[self.day_number] = [self.current_card]

            #Return Jokers to deck
            for card in self.to_resolve:
                self.deck.append(card)
                random.shuffle(self.deck)
            #Empty to_resolve
            self.to_resolve.clear()

            #Decrement cards remaining
            self.cards_remaining -= 1
            
            #Decrement number of draws
            num_draws -= 1




    #RESOLVE JOKER: When a joker has been drawn, the sum of jokers will update. 
    #When the sum of either joker reaches 3, the game ends, or the player has
    #the option to reduce the number of jokers to continue playing
    def resolve_joker(self):
        continue_game = 0

        print(f"\n{self.current_card} drawn! Catastrophe strikes!\n\n")
        #Add joker to dictionary of drawn cards
        if self.day_number in self.discard: #Check if current day is already listed in the drawn cards
            self.discard[self.day_number].append(self.current_card)
        else:
            self.discard[self.day_number] = [self.current_card]
            
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
    user_option = 0
    num_cards = 0
    update_day = 0
    

    print(f"\n\nSTARTING JOURNEY\n\n")
    print(f"1 = Draw One or More Cards\n")
    print(f"2 = Update Day of Journey\n")
    print(f"3 = Print All Cards Drawn by Day\n")
    print(f"4 = Quit\n\n")
    user_option = int(input("Type the number of your choice: "))
    print("\n\n")

    while user_option not in [4]:
        match user_option:
            case 1:
                num_cards = 0
                while num_cards == 0:
                    num_cards = int(input("Enter number of cards you want to draw: "))
                    current_game.draw_card(num_cards)
                    if current_game.to_resolve in ["Red Joker","Black Joker"]:
                        current_game.deck.append(to_resolve)
                        current_game.to_resolve = "Empty"
                current_game.save_game()
                
            case 2:
                update_day = 0
                while update_day == 0:
                    print(f"The current day is {current_game.day_number}\n")
                    update_day = int(input("Enter the next day number for your journey: "))
                    current_game.day_number = update_day
                    update_day = 1
                current_game.save_game()
                    
            case 3:
                current_game.print_draws()
        print("\n\n")

        print(f"1 = Draw \t 2 = Update Day of Journey \t 3 = Print All Cards Drawn by Day \t 4 = Quit\n\n")
        user_option = int(input("Type the number of your choice: "))
        print("\n\n")

    is_play = 0

    current_game.save_game()
        
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
                day_number = saved_vars.get("day_number")
                to_resolve = saved_vars.get("to_resolve")
                last_saved = saved_vars.get("last_saved")
                var_save = {
                    "file_name": file_name,
                    "deck": deck,
                    "discard": discard,
                    "red_jokers": red_jokers,
                    "black_jokers": black_jokers,
                    "cards_remaining": cards_remaining,
                    "curent_card": current_card,
                    "day_number": day_number,
                    "to_resolve": to_resolve,
                    "last_saved": last_saved
                }

                #Create Game object from saved variables
                current_game = Game(file_name, deck, discard, red_jokers,
                                    black_jokers, cards_remaining, current_card,
                                    var_save, day_number, to_resolve, last_saved)

            
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
