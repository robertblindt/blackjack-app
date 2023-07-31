import tkinter as tk
from random import shuffle
import copy

# Functions for blackjack stuff go here
class Deck():
    suits = ["\u2663", "\u2665","\u2666", "\u2660"]
    values = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
    def __init__(self, quant = 1): 
        deck = [f'{value} {suit}' for value in self.values for suit in self.suits for q in range(quant)]
        shuffle(deck) 
        self.deck = deck
        self.quant = quant
        
    def __str__(self):
        return f'{len(self.deck)} cards in this deck!'
    
    def __repr__(self):
        return f'<Deck | {len(self.deck)} cards | from {self.quant} decks>'
    
    def pass_card(self):
        return self.deck.pop()


class Person():
    player_id = 1
    
    def __init__(self,money = 0):
        self.money = money
        self.hand = []
        self.hand_vals = []
        self.player_id = Person.player_id
        Person.player_id += 1
        self.in_game = True
        
        
    def __str__(self):
        return f"{' ~ '.join(self.hand)}"
    
    def __repr__(self):
        return f'<Person| {self.player_id}>'
    
    def _convert_hand(self):
        self.hand_vals = []
        for card in self.hand:
            try:
                int(card.split()[0])
                self.hand_vals.append(int(card.split()[0]))
            except:
                if card.split()[0] == 'J' or card.split()[0] == 'Q' or card.split()[0] == 'K':
                    self.hand_vals.append(10)
                elif card.split()[0] == 'A':
                    if sum(self.hand_vals) <= 10:
                        self.hand_vals.append(11)
                    else:
                        self.hand_vals.append(1)
        if sum(self.hand_vals) > 21:
            if 11 in self.hand_vals:
                self.hand_vals[self.hand_vals.index(11)] = 1
      
    
    def draw_card(self, deck):
        self.hand.append(deck.pass_card())
        self._convert_hand()
        self.hand_tot = sum(self.hand_vals)

    
    def print_dealer(self):
        obscured_hand = copy.deepcopy(self.hand)
        obscured_hand[0] = 'HIDDEN'
        return f"{' ~~~ '.join(obscured_hand)}"
            
    def check_for_blackjack(self):
        if self.hand_tot == 21:
            # print('You got Blackjack!')
            return True    
    
    def player_condition(self):
        if self.hand_tot == 21 and len(self.hand_vals) == 2:
            self.in_game = False
            return 'Blackjack'
        elif self.hand_tot == 21:
            self.in_game = False
            return '21'
        elif self.hand_tot > 21:
            self.in_game = False
            return 'Bust'
        else:
            self.in_game = True
            return True


class Blackjack():
    def __init__(self):#, num_players = 1):
        # self.num_players = num_players
        self.players = []
        
    def add_player(self, money_in = 0):
        self.players.append(Person(money_in))
        
    def game_draw(self, player, deck):
        player.hand.append(deck.pass_card())
        
        
    def deck_and_board_setup(self, deck):
        for player in self.players:
            player.draw_card(deck)
            player.draw_card(deck)
            if player.player_id == len(self.players):
                add_to_dealerbox(player.print_dealer())
            else:
                add_to_player_box(player)


# Create the deck and blackjack instance and add the 2 players
deck = Deck()                
blackjack_game = Blackjack()
for i in range(2):
    blackjack_game.add_player()

# Create dealer and start game
blackjack_game.add_player()


def play_blackjack(deck):
    blackjack_game.deck_and_board_setup(deck)

    game_complete = False
    while game_complete != True:
        players_in_game = 0
        blackjack_game.players[-1].player_condition()
        game_complete = blackjack_game.players[-1].in_game

        for player in blackjack_game.players:
            player.player_condition()
            players_in_game += player.in_game

        if players_in_game <= 1:
            game_complete = True
        else:
            for player in blackjack_game.players:
                if player.player_id == len(blackjack_game.players):
                    if players_in_game <= 1:
                        pass_turn = 'ez-win'
                    else:
                        while player.hand_tot < 17:
                            player.draw_card(deck)
                            # print('Dealer is Drawing Card')
                            player.print_dealer()
                            if player.hand_tot > 21:
                                player.hand_tot = 0
                                break
                        pass_turn = 'house rule reached'

                else:
                    change_guide_text(f'It is player {player.player_id} turn!')
                    pass_turn = False
                    while pass_turn == False:

                        # Make buttons hit or stand for you!
                        draw_btn.wait_variable(button_pressed) or stand_btn.wait_variable(button_pressed)

                        if button_pressed.get()[0] == 'h':
                            player.draw_card(deck)
                            # print(player.hand, player.hand_vals)
                            add_to_player_box(player)
                            if player.hand_tot >= 21:
                                print_results(player, f'Player {player.player_id} busted with {player}')
                                pass_turn = True
                        #elif h_or_s[0].lower() == 's':
                        elif button_pressed.get()[0] == 's':
                            print_results(player, f'You chose to stand with {player}')
                            pass_turn = True
                            break
                        # THIS CAUSES A BUST ON PLAYER 1 AND A BLACKJACK ON PLAYER 2 TO STOP THE DEALER FROM PLAYING! 
                        # if player.player_condition() == 'Bust':
                        #     players_in_game -= 1
                        
                        pass_turn == player.player_condition()
                        
        game_complete = True                                        
            
    print_results(player, f'The dealer had: \n{blackjack_game.players[-1]}')
    for player in blackjack_game.players:
        if player.player_id == len(blackjack_game.players):
            pass
        else:
            if player.hand_tot > 21:
                print_results(player, f'Player {player.player_id} Busted! \n    Dealer had {blackjack_game.players[-1].hand_tot}')
            elif player.hand_tot == blackjack_game.players[-1].hand_tot:
                print_results(player, f'Player {player.player_id} Tied the dealer! You get your money back! \n    Dealer had {blackjack_game.players[-1].hand_tot}')
            elif player.hand_tot > blackjack_game.players[-1].hand_tot:
                print_results(player, f'Player {player.player_id} BEAT THE DEALER!!!! \n    Dealer had {blackjack_game.players[-1].hand_tot}')
            else:
                print_results(player, f'Player {player.player_id} Lost to the Dealer! D,8 \n    Dealer had {blackjack_game.players[-1].hand_tot}')
    change_guide_text('Press the "Restart" button to play another game!')
                            
            


# Functions for doing stuff in tkinter go here
text_box_content = f''
p1_box = f''
p2_box = f''
h_or_s = ''
guide_text = ''
def add_to_dealerbox(player):
    global text_box_content
    text_box_content += f'{player} \n'
    dealer_result.delete(1.0,"end")
    dealer_result.insert(1.0, text_box_content)

def add_to_player_box(player):
    if player.player_id == 1:
        global p1_box
        p1_box += f'{player} \n'
        p1_cards.delete(1.0,"end")
        p1_cards.insert(1.0, p1_box)
        p1_total.delete(1.0,"end")
        p1_total.insert(1.0, str(player.hand_tot))
    elif player.player_id == 2:
        global p2_box
        p2_box += f'{player} \n'
        p2_cards.delete(1.0,"end")
        p2_cards.insert(1.0, p2_box)
        p2_total.delete(1.0,"end")
        p2_total.insert(1.0, str(player.hand_tot))

def change_guide_text(input_text):
    global guide_text
    guide_text = f'{input_text}'
    guide_text_box.delete(1.0,"end")
    guide_text_box.insert(1.0, guide_text)

    

def print_results(player, message):
    if player.player_id == 1:
        global p1_box
        p1_box += f'{message} \n'
        p1_cards.delete(1.0,"end")
        p1_cards.insert(1.0, p1_box)
    elif player.player_id == 2:
        global p2_box
        p2_box += f'{message} \n'
        p2_cards.delete(1.0,"end")
        p2_cards.insert(1.0, p2_box)
    elif player.player_id == 3:
        global text_box_content
        text_box_content += f'{player} \n'
        dealer_result.delete(1.0,"end")
        dealer_result.insert(1.0, text_box_content)

def restart_game():
    for player in blackjack_game.players:
        player.hand = []
    global text_box_content, p1_box, p2_box
    text_box_content = f''
    p1_box = f''
    p2_box = f''
    h_or_s = ''

    play_blackjack(deck)

def return_h_or_s(btn_id):
    global h_or_s
    if btn_id == 'hit':
        h_or_s = 'h'
    else:
        h_or_s = 's'


def return_h():
    global h_or_s
    h_or_s = 'h'

def return_s():
    global h_or_s
    h_or_s = 's'


# App Goes here
root = tk.Tk()
root.geometry('1070x550')
root.title('Blackjack App')

root.columnconfigure

label = tk.Label(root, text="Welcome to Blackjack!",  font=("Helvetica",22,'bold','italic'))
label.grid(row = 1, column=1, columnspan = 2)

dealer_result = tk.Text(root, height=6, width=10, font=("Helvetica",12), wrap = tk.WORD)
dealer_result.grid(columnspan=4, row = 2, sticky=tk.W+tk.E, padx=10)

# Label
p1_total_label = tk.Label(root, text="Player 1 Total:",  font=("Helvetica",14,'italic'))
p1_total_label.grid(columnspan=2, column = 0, row = 3, sticky=tk.W+tk.E, padx=10)
# Total Score
p1_total = tk.Text(root, height=1,width=6, font=("Helvetica",12), wrap = tk.WORD)
p1_total.grid(columnspan=2, column = 0, row = 4, sticky=tk.W+tk.E, padx=10)
# Cards
p1_cards = tk.Text(root, height=6,width=6, font=("Helvetica",12), wrap = tk.WORD)
p1_cards.grid(columnspan=2, column = 0, row = 5, sticky=tk.W+tk.E, padx=10, pady =10)

# L
p2_total_label = tk.Label(root, text="Player 2 Total:",  font=("Helvetica",14,'italic'))
p2_total_label.grid(columnspan=2, column = 2, row = 3, sticky=tk.W+tk.E, padx=10)
# TS
p2_total = tk.Text(root, height=1,width=6, font=("Helvetica",12), wrap = tk.WORD)
p2_total.grid(columnspan=2, column = 2, row = 4, sticky=tk.W+tk.E, padx=10)
# C
p2_cards = tk.Text(root, height=6,width=6, font=("Helvetica",12), wrap = tk.WORD)
p2_cards.grid(columnspan=2, column = 2, row = 5, sticky=tk.W+tk.E, padx=10, pady =10)


# Play the game buttons
button_pressed = tk.StringVar()
draw_btn = tk.Button(root, text="Hit", command=lambda: button_pressed.set("hit"),  width=5, font=("Helvetica",18))

# draw_btn = tk.Button(root, text="Hit", command=return_h_or_s('hit'),  width=5, font=("Helvetica",18))

draw_btn.grid(column=0, row = 6, columnspan=2, pady = 10, padx = 10, sticky=tk.W+tk.E)

#button_pressed = tk.StringVar()
stand_btn = tk.Button(root, text="Stand", command=lambda: button_pressed.set("stand"), width=5, font=("Helvetica",18))

# stand_btn = tk.Button(root, text="Stand", command=return_h_or_s('stand'), width=5, font=("Helvetica",18))

stand_btn.grid(column=2, row = 6, columnspan=2, pady = 10, padx = 10, sticky=tk.W+tk.E)

guide_text_box = tk.Text(root, height=1, font=("Helvetica",18), wrap = tk.WORD)
guide_text_box.grid(columnspan=4, row = 7, sticky=tk.W+tk.E, padx=10, pady=10)
change_guide_text('Press the "Restart" button to start your first game!')

# Restart the game because I dont know how to make the page change through a process
restart_btn = tk.Button(root, text="Restart", command=restart_game, width=5, font=("Helvetica",18))
restart_btn.grid(columnspan=4, row = 8, sticky=tk.W+tk.E, padx=10, pady=20)

root.mainloop()