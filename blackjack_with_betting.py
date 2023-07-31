from random import shuffle
import copy

class Deck():
    suits = ['Clubs','Hearts','Spades','Diamonds']
    values = ['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King']
    def __init__(self, quant = 1): 
        deck = [f'{value} of {suit}' for value in self.values for suit in self.suits for q in range(quant)]
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
        return f"{' ~~~ '.join(self.hand)} ~~~~~~ Total: {self.hand_tot}"
    
    def __repr__(self):
        return f'<Person| {self.player_id}>'
    
    def _convert_hand(self):
        self.hand_vals = []
        for card in self.hand:
            try:
                int(card.split()[0])
                self.hand_vals.append(int(card.split()[0]))
            except:
                print()
                if card.split()[0] == 'Jack' or card.split()[0] == 'Queen' or card.split()[0] == 'King':
                    self.hand_vals.append(10)
                elif card.split()[0] == 'Ace':
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
        print('The Dealer has: ')
        print(f"{' ~~~ '.join(obscured_hand)}")
            
    def check_for_blackjack(self):
        if self.hand_tot == 21:
            print('You got Blackjack!')
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
                player.print_dealer()
            else:
                print(player)
                


def play_blackjack():
    print('Welcome to my Blackjack game! I hope you have fun!')
    while True:
        desire = input('Would you like to play a game of Blackjack? \n')[0].lower()
        while desire not in {'y','n'}:
            desire = input("Im sorry, I didn't understand that! Would you like to play a game of Blackjack? (Y/N}) \n")[0].lower()
        if desire == 'n':
            print('Thanks for checking out my Blackjack app!')
            break
        elif desire == 'y':

            blackjack_game = Blackjack()
            deck = Deck()

            # Set player count
            # This type handler isnt working for some reason --------------------------------------------------
            player_count = input('How many players do you want to play with?\n')
            while not player_count.isdigit() and int(player_count) < 4:
                player_count = input("Please only enter an integer equal or less than 3. \n")
            
            # Create real people
            for i in range(int(player_count)):
                money_in = int(input('How much money would you like to enter the table with?\n'))
                blackjack_game.add_player(money_in)
            
            # Create dealer and start game
            blackjack_game.add_player()
            print('Game starting!')

            req = 'yes'
            while req.lower()[0] != 'n':
                req = input('Would you like to start a hand?\n')
                while req.lower()[0] not in ['y','n']:
                    req = input('Please enter Yes or No. Would you like to start a hand?\n')
                if req.lower()[0] == 'y':
                    for player in blackjack_game.players:
                        player.hand = []
                    
                    for player in blackjack_game.players:
                        if player.player_id == len(blackjack_game.players) or player.money == 0:
                            pass
                        else:
                            bet = input(f'Player {player.player_id}, how much would you like to bet on this hand? \n')
                            while not bet.isdigit() or int(bet) > player.money:
                                bet = input(f'Please only enter integers less than or equal to {player.money}. Player {player.player_id}, how much would you like to bet on this hand? \n')
                            player.bet = int(bet)
                        

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
                                            print('Dealer is Drawing Card')
                                            player.print_dealer()
                                            if player.hand_tot > 21:
                                                player.hand_tot = 0
                                                break
                                        pass_turn = 'house rule reached'

                                else:
                                    print(f'Player {player.player_id} turn\n{player}')
                                    pass_turn = False
                                    while pass_turn == False:
                                        h_or_s = input('Would you like to Hit or Stand? \n').lower()
                                        while h_or_s[0].lower() not in {'h','s'}:
                                            h_or_s = input('That was an invalid input. Would you like to Hit or Stand? (H/S): \n').lower()
                                        if h_or_s[0].lower() == 'h':
                                            player.draw_card(deck)
                                            # print(player.hand, player.hand_vals)
                                            print('Drawing Card')
                                            print(player)
                                            if player.hand_tot >= 21:
                                                pass_turn = True
                                        else:
                                            print(f'You chose to stand with {player}')
                                            pass_turn = True
                                            break
                                        if player.player_condition() == 'Bust':
                                            players_in_game -= 1
                                        
                                        pass_turn == player.player_condition()
                                        
                        game_complete = True                                        
                            
                    print(f'The dealer had: \n{blackjack_game.players[-1]}')
                    for player in blackjack_game.players:
                        if player.player_id == len(blackjack_game.players):
                            pass
                        else:
                            if player.hand_tot > 21:
                                print(f'Player {player.player_id} Busted!')
                                player.money -= player.bet
                            elif player.hand_tot == blackjack_game.players[-1].hand_tot:
                                print(f'Player {player.player_id} Tied the dealer! You get your money back!')
                            elif player.hand_tot > blackjack_game.players[-1].hand_tot:
                                print(f'Player {player.player_id} BEAT THE DEALER!!!!')
                                player.money += player.bet
                            else:
                                print(f'Player {player.player_id} Lost to the Dealer! D,8 ')
                                player.money -= player.bet
                            
                            player.bet = 0

                            if player.money == 0:
                                print(f'Sorry {player.player_id}! You are out of funds! Sucks to suck!')
                            else:
                                print(f'Player {player.player_id}s new total is {player.money}!')
                                        
                            
                else:
                    for player in blackjack_game.players:
                        if player.player_id == len(blackjack_game.players):
                            pass
                        elif player.money > 0:
                            print(f'Player {player.player_id} is leaving with {player.money}')
                        else:
                            print(f'Player {player.player_id} is a loser and lost all their money.')

play_blackjack()