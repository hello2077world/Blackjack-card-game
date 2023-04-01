from random import shuffle
import os

# Clean terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Initial message
print("\n♥*♦*♣*♠ Welcome to BlackJack! ♥*♦*♣*♠ \nGet as close to 21 as you can without going over! \nDealer hits until he reaches 17. Aces count as 1 or 11. The minimum bet is 5. You start with 120 chips.")

###################### GLOBAL VARIABLES ###########################
# Suits from highest to lowest ♥>♦>♣>♠
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
# Ranks of the cards, from high to low
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
# Values of the cards, from high to low
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

######################## CLASSESS #################################

# Creates an object with a total amount of chips
class Chips:
    def __init__(self) -> None:
        self.total = 120
    #Place bet until the input is invalid (greather than total, total is less than minimum bet etc.)
    def place_bet(self):
        self.bet = 0
        self.minimum_bet = 5
        while True:
            try:
                self.bet = int(input(f"\nHow many chips would you like to bet? (you currently have {self.total} chips): "))
            except ValueError:
                print('Sorry, a bet must be an integer!')
            except:
                print('Sorry, something is wrong!')
            else:
                if self.bet > self.total:
                    print(f"Sorry, you don't have enough chips!")
                elif self.bet == self.total:
                    print("You play va banque!")
                    self.total = 0
                    break
                elif self.total < self.minimum_bet:
                    if self.bet <= 0:
                        print(f"Sorry, but a bet must be greater than zero!")
                        continue
                    else:
                        print("You play va banque!")
                        self.bet = self.total
                        self.total = 0
                        break
                elif self.bet < self.minimum_bet:
                    print(f"Sorry, but the minimum bet is {self.minimum_bet}!")
                else:
                    self.total -= self.bet
                    break
        return self.bet
    #Adds or subtracts chips depending on whether player win or lose, the player gets 150% of the bet
    def add_chips(self, chips):
        self.total += chips

# Creates a deck of cards
class Deck:
    def __init__(self) -> None:
        self.cards = []
        for i in ranks:
            for j in suits:
                self.cards.append(i + ' of ' + j)
    #Mixes the cards
    def shuffle(self):
        shuffle(self.cards)   
    #Deal cards to the players
    def deal_card(self):
        return self.cards.pop(0)

# Creates 2 cards for each and counts their value
class Hand:
    def __init__(self, deck, name) -> None:
        self.name = name
        self.hand = [deck.deal_card(), deck.deal_card()]
        if self.hand[0].split(' ')[0] == 'Ace' and self.hand[1].split(' ')[0] == 'Ace':
            self.value = values[self.hand[0].split(' ')[0]] + 1
        else:
            self.value = values[self.hand[0].split(' ')[0]] + values[self.hand[1].split(' ')[0]]
    #Player and Dealer decide whether to hit or stand
    def hit_or_stand(self):
        self.choice = ''
        if self.name == 'Dealer':
            if self.value < 17:
                card = deck.deal_card()
                self.hand.append(card)
                if card.split(' ')[0] == 'Ace':
                    self.value += self.check_value_of_ace()
                else:
                    self.value += values[self.hand[-1].split(' ')[0]]
                return 'h'
            else:
                return 's'
        elif self.name == 'Player':
            while True:
                choice = input("\nWould you like to Hit or Stand? Enter 'h' or 's': ")
                if len(choice) > 0 and choice[0].lower() == 'h':
                    card = deck.deal_card()
                    self.hand.append(card)
                    if card.split(' ')[0] == 'Ace':
                        self.value += self.check_value_of_ace()
                    else:
                        self.value += values[self.hand[-1].split(' ')[0]]
                    return 'h'
                elif len(choice) > 0 and choice[0].lower() == 's':
                    return 's'
                else:
                    print("Sorry, please try again.")
                    continue
    #Checks if ace should be 11 or 1 and return
    def check_value_of_ace(self):
        if self.value + 11 <= 21:
            return 11
        else:
            return 1
                
######################## GAME LOGIC ###############################

# Creates chips for player
player_chips = Chips()

# GAME ON! = creates and shuffles the deck, asks for a bet, creates two cards and value of them for the Player and the Dealer until player wants to play
game_on = True
while game_on:     
    deck = Deck()
    deck.shuffle()

    players_bet = player_chips.place_bet()

    player = Hand(deck, 'Player')
    dealer = Hand(deck, 'Dealer')

    round = 0
    player_decision = 'h'
    dealer_decision = 'h'
    
    # Duel! The loop runs until the game or the dealer busts or loses
    while True:
        round += 1
        print(f'\n------------ROUND {round}------------\n')
        #Hide dealer's first card during round 1
        if round == 1:
            print("Dealer's hand: \n <card hidden>\n", '\n '.join(dealer.hand[1:]))
            print("Dealer's value:", dealer.value - values[dealer.hand[0].split(' ')[0]])
        else:
            print("Dealer's hand: \n", '\n '.join(dealer.hand))
            print("Dealer's value:", dealer.value)
        print("\nPlayer's hand: \n", '\n '.join(player.hand))
        print("Player's value:", player.value)
        #Check if player or dealer is not busted or if player has blackjack
        if player.value >= 21:
            if player.value == 21:
                if len(player.hand) == 2:
                    print("\nPlayer hits ♥*♦ BLACKJACK ♣*♠ and gets 150% of the placed bet!")
                    player_chips.add_chips(int(players_bet + players_bet*1.5))
                    break
                player_decision = 's'
            else:
                print("\n* Player busts! *")
                break
        if dealer.value >= 21:
            if dealer.value == 21:
                dealer_decision = 's'
            else:
                print("\n* Dealer busts! *")
                player_chips.add_chips(players_bet*2)
                break  
        #Player and Dealer decide whether to hit or stand (Decisions 'h' for hit, 's' for stand)
        if player_decision == 'h':
            player_decision = player.hit_or_stand()
        if dealer_decision == 'h':
            dealer_decision = dealer.hit_or_stand()
        #Check who win if player and dealer stand
        if player_decision == 's' and dealer_decision == 's':
            if player.value == dealer.value:
                print("\n* Dealer and Player tie! It's a push. *")
                player_chips.add_chips(players_bet)
            elif player.value > 21 and dealer.value > 21:
                print("\n* Double bust! It's a push. *") 
            elif player.value > dealer.value:
                print("\n* Player wins! *")
                player_chips.add_chips(players_bet*2)
            elif dealer.value > player.value:
                print("\n* Dealer wins! *")
                if round == 1:
                    print(f"Dealer's <card hidden> is {dealer.hand[0]} and dealer's value is {dealer.value}.\n")
            break
        
    # After duel
    print(f"Player's currently has {player_chips.total} chips.")
    print('\n_______________________________')
    
    # Game over if player has no chips
    if player_chips.total == 0:
        print('\nSorry, but you are out of chips!')
        game_on = False
        break
    
    # Asks to play again
    while True:
        play_again = input("\nWould you like to play another hand? Enter 'y' or 'n': ")[0].lower()
        if play_again == 'y':
            game_on = True
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        elif play_again == 'n':
            game_on = False
            break

# Final message    
print('\n♥*♦*♣*♠ Thank you for playing! :) ♥*♦*♣*♠\n')    
