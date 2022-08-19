from random import shuffle  #To shuffle the deck
from time import sleep  #To add delays to the game
import itertools   #To use the .product method

class Player:
    '''
    A class to represent a player playing the game of Blackjack

    Attributes:
    ------------

    self, name, game, ishuman = True, isdealer = False
        
    name: string
    Stores the name of the player

    game: object
    an instance of the class Game

    ishuman : boolean
    A boolean that indicates whether a player is a human
    ishuman = True by default

    isdealer : boolean
    A boolean that indicates whether a player is a dealer
    isdealer = False by default

    Methods:
    --------
    get_card(self, card, visible):
        This function gets card as a parameter and adds them to the list of cards. 
    
    cardnametostring(self): 
        This function changes the representation of the cards in a hand to a string with the help of to_string() function
    
    Hit_or_Stay(self):
        This function prompts the human players to choose whether to hit or stay.
    
    bust(self):  
        This function declares the player a loser. This function is called when points > 21.
    
    win(self):   
        This function declares the player a winner. This function is called when points == 21.
    
    hit(self):
        This function deals a card to the player's hand based on the player's game strategy. 
    
    stay(self):
        This function makes no changes to the hand or deck. 
    
    play(self):
        This function is responsible for deciding the logic of the game based on whether the user is a dealer, a humanplayer, or a computer.
    
    '''

    def __init__(self, name, game, ishuman = True, isdealer = False):
        """  
        The function initializes the parameters of class Player

        Parameters
        ----------
        self, name, game, ishuman = True, isdealer = False
        
        name: string
        The name of the player
    
        game: object
        an instance of the class Game

        ishuman : boolean
        A boolean that indicates whether a player is a human
        ishuman = True by default

        isdealer : boolean
        A boolean that indicates whether a player is a dealer
        isdealer = False by default
 
        Variables
        -----------

        self.cards : list
        a list that contains all the cards in a player's hand

        self.name : name
        name passed is saved to instance variable self.name

        self.busted: boolean
        A boolean that indicates whether a player has busted or not
        Set to False by default

        self.winflag : boolean
        A boolean that indicates whether a player has won or not
        Set to False by default

        self.ishuman : boolean
        ishuman passed is saved to instance variable self.ishuman

        self.isdealer : boolean
        isdealer passed is saved to instance variable self.isdealer

        """
        self.cards = []
        self.name = name
        self.busted = False
        self.winflag = False
        self.game = game
        self.ishuman = ishuman
        self.isdealer = isdealer

    def get_card(self, card, visible = True):
        """  
        Function get_card(self, card, visible):
        
        This function gets card as a parameter and adds them to the list of cards. 
        Also stores whether a given card is visible or not. 

        Parameter:
        -----------
        self, card, visible = True

        card: card instance containing the suit and rank of the cards
        This card instance is to be appended to list self.cards

        visible = Boolean
        Stores boolean value representing whether a card is visible or not.

        Return:
        ----------
        None
        """ 
        card.visible = visible
        self.cards.append(card)

    def cardsnamesinstring(self):
        """  
        Function cardnametostring(self):
        
        This function changes the representation of the cards in a hand to a string with the help of to_string() function, 
        and returns them in a list form.

        Return:
        ---------
        [card.to_string() for card in self.cards]: list
        Returns the list containing string representation of all cards in the hand 

        """ 
        return [card.to_string() for card in self.cards]

    def pointcalc(self):
        """  
        Function pointcalc(self):
        
        This function calculates the total summation of points of all the cards in the hand and returns it.
        
        Return:
        ---------
        sum(card.points() for card in self.cards): int
        Returns the integer sum of cards post summation of individual values

        """ 
        return sum(card.points() for card in self.cards)

    def points(self):
        """  
        Function points(self):
        
        This function calculates the pounts of the player at a given time, adjusting for aces
        Calls the function pointcalc() to store the total points without adjusting for aces

        Functionality:
        ---------------
        if total>21:
            the value of ace is adjusted from 11 to 1. The conversion takes place for each occurenc of an ace.
            the total is now recalculated and returned.
        else:
            return total as it is.
        
        Variables:
        -----------
        total : int
        Stores the sum of points before ajusting for the ace

        no_of_aces: int
        stores the value for the number of aces in hand

        Return:
        ---------
        total: int
        The total of all card values without the need for ace adjusting

        self.pointcalc(): Function
        The total after adusting for ace

        """  
        total = self.pointcalc()
        # Check if we should reduce the value of aces
        if total > 21:
            no_of_aces = [index for index, card in enumerate(self.cards) if card.rank == 'A']
            for ace_index in no_of_aces:
                self.cards[ace_index].alternate_value = True
                if self.pointcalc() <= 21:
                    return self.pointcalc()

        return total

    def Hit_or_stay(self):
        """  
        Function Hit_or_Stay(self):
        
        This function prompts the human players to choose whether to hit or stay.

        Variables:
        ------------

        decision: string
        Stores user's decision (hit) or (stay)

        Return:
        ---------

        decision: string
        Returns the decision string
        """  
        decision = input("\n{},\nYour hand: {}. This totals {} points.\nWould you like to 'hit' or 'stay'? \t".format(self.name, self.cardsnamesinstring(), self.points()))
        return decision

    def bust(self):
        """  
        Function bust(self):
        
        This function declares the player a loser. This function is called when points > 21.
        Changes self.busted = True to register that the player is busted, and outputs accordingly in the final results.

        """  
        print("\n{}, you have busted with the hand: {}. This totals {}!\n".format(self.name, self.cardsnamesinstring(), self.points()))
        self.busted = True

    def win(self):
        """  
        Function win(self):
        
        This function declares the player a winner. This function is called when points == 21.
        Changes self.winflag = True to register that the player is a winner, and outputs accordingly in the final results.

        """  
        print("\n{}, you have won the game with the hand: {}.\nThis totals {}. Congratualtions!\n".format(self.name, self.cardsnamesinstring(), self.points()))
        self.winflag = True
    
    def hit(self):
        """  
        Function hit(self):
        
        This function deals a card to the player's hand. 
        if points<21:
            Function then calls the function play()
        else if points == 21:
            calls function win()
        else:
            calls function bust()
      
        """  
        self.game.deck.dealcard(self)
        if self.points() < 21:
            self.play()
        elif self.points() == 21:
            self.win()
        else:
            self.bust()
    
    def stay(self):
        """  
        Function stay(self):
        
        This function makes no changes to the hand or deck. 
        Prints the player's current hand, and points.

        """  
        print ("{} is staying with the hand: {}".format(self.name, self.points()))

    def play(self):
        """  
        Function play(self):

        This function is responsible for deciding the logic of the game based on whether the user is a dealer, a humanplayer, or a computer.
        
        Sample
        -----------

        (i) If player is a dealer:
                print("Dealer is playing their turn")
                check whether cards need to be visible using self.cards.visible attribute
                Display dealer's hand
                if points>17: stay()
                else if points<17: hit()
        (ii)If player is not a dealer, not a human:
                print("Computer is playing their turn")
                Display computer's hand
                if points>17: stay()
                else if points<17: hit()
                else if points == 21: win()
        (iii)If player is not a dealer, but is a human:
                print("Human Player is playing their turn")
                Display Player's hand
                if points<21: Let human choose between function hit() and stay()
                else if points == 21: win()
                
        Returns
        -------
        
        None

        """   
        if self.isdealer == True:
            print("\nDealer is playing their turn:")
            sleep(1.5)
            self.cards[0].visible = True
            print("Dealer's hand is {} for a total of {}".format(self.cardsnamesinstring(), self.points()))
            if self.points() <= 17:
                print("Dealer is hitting.")
                sleep(1.5)
                self.hit()
            else:
                print("Dealer is staying.")
                sleep(1.5)
                self.stay()
        else:
            if self.points() == 21:
                self.win()
            else:
                if self.ishuman == True:
                    response = self.Hit_or_stay()

                    while response.lower() != 'hit' and response.lower() != 'stay':
                        print("Not an acceptable response. You must 'hit' or 'stay'")
                        response = self.Hit_or_stay()

                    if response.lower() == 'hit':
                        self.hit()
                    else:
                        self.stay()
                else:
                    print("\n"+self.name+" is playing their turn:")
                    sleep(0.5)
                    print("{} has hand:{}. This totals {} points".format(self.name, self.cardsnamesinstring(), self.points()))
                    if self.points() <= 17:
                        print("{} is hitting.".format(self.name))
                        sleep(1.5)
                        self.hit()
                    else:
                        print("{} is staying.".format(self.name))
                        sleep(1.5)
                        self.stay()


class Deck:
    '''
    A class to represent a deck used in the game of Blackjack

    Attributes:
    ------------

    self, no_of_sets = 1
        
    no_of_sets: int
    the number of sets of cards (each set has 52) to be shuffled with the deck

    Methods:
    --------
    shuffle_cards:
        This function shuffles the entire deck of cards.
    
    dealcard:
        This function deals a card from the deck to a player instance. 
    
    '''
    def __init__(self, no_of_sets = 1):
        """  
        The function initializes the parameters of class Deck

        Parameters
        ----------
        self, no_of_sets
        
        no_of_sets: int
        Gets the number of sets of cards (each set has 52) to be shuffled with the deck
        no_of_sets is 1 by default
 
        Variables
        -----------

        self.no_of_suits : int
        no_of_suits passed is saved to instance variable self.no_of_suits

        self.suits : list
        a list containing all the suits present in the deck: Diamonds, Hearts, Clubs, Spades

        self.ranks: list
        a list containing all the ranks present in the deck: 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'

        self.cards: list
        a list containing all the cards in the deck

        """
        self.no_of_sets = no_of_sets
        self.suits = ['Diamonds', 'Hearts', 'Clubs', 'Spades']
        self.ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.cards = []
        for i in range(self.no_of_sets):
            for suit, rank in itertools.product(self.suits, self.ranks):
                self.cards.append(Card(suit, rank))

    def shuffle_cards(self):
        """
        Function shuffle_cards:

        This function shuffles the entire deck of cards.

        Return:
        --------

        None 
        """
        shuffle(self.cards)

    def dealcard(self, player, visible = True):
        '''
        Function dealcard:

        This function deals a card from the deck to a player instance. 

        Parameters:
        ------------

        self, player, visible

        player: object
        player is an instance of the class Player

        visible: boolean
        a boolean variable that tells whether a card is to be visible or not (dealer's first hand)
        
        Functionality:
        ---------------
        A card is popped from the list self.cards. 
        This card is then sent as a parameter to the function get_card() to be instantiated with the player's hand.

        Return:
        --------
        
        None
        '''
        card = self.cards.pop()
        player.get_card(card, visible)


class Card:
    '''
    A class to define a single card in a deck

    Attributes:
    ------------

    self, suit, rank
    
    suit: char
    Refers to the suit of a card: Hearts, Diamonds, Clubs, Spades 
    
    rank: char
    Refers to the rank of the card: A,2,3,4,5,6,7,8,9,10,J,Q,K
    
    Variable:
    ----------

    values: list
    Contains the list of aall the ranks in a deck

    Methods:
    --------
    to_string(self):
        Displays the card in terms of a string. ie. [4,Spades] will be 4 of Spades
    points(self):
        If a particular card has two values associated (Ace), then this function switches the values as appropriate

    '''
    values = {
        'A': [11, 1],
        'K': [10],
        'Q': [10],
        'J': [10],
        '10': [10],
        '9': [9],
        '8': [8],
        '7': [7],
        '6': [6],
        '5': [5],
        '4': [4],
        '3': [3],
        '2': [2]
    }

    def __init__(self, suit, rank):
        """  
        The function initializes the parameters of class Card

        Parameters
        ----------
        self, suit, rank
        
        suit: char
        Refers to the suit of a card: Hearts, Diamonds, Clubs, Spades 
    
        rank: char
        Refers to the rank of the card: A,2,3,4,5,6,7,8,9,10,J,Q,K
 
        Variables
        -----------

        self.suit : char
        suit passed is saved to instance variable self.suit

        self.rank : char
        rank passed is saved to instance variable self.rank

        self.visible: boolean
        Decides whether to make a card visible or not

        self.alternate_value: boolean
        Checks whether a particular rank has an alternate value (eg. Ace)

        """
        self.suit = suit
        self.rank = rank
        self.visible = None
        self.alternate_value = False

    def to_string(self):
        '''
        Function to_string(self):
        If self.visible is true 
            Displays the card in terms of a string. ie. [4,Spades] will be 4 of Spades
        else
            Displays "*Hidden*"
        '''
        if not self.visible:
            return "*Hidden*"
        else:
            return self.rank+" of "+self.suit

    def points(self):
        '''
        Function points(self):
        
        If a particular card has two values associated (Ace), then this function switches the values as appropriate

        '''
        if self.alternate_value:
            return Card.values[self.rank][-1]
        else:
            return Card.values[self.rank][0]


class Game:
    '''
    A class to play the game of Blackjack

    Attributes:
    ------------

    self, human_players, computer_players, no_of_cards
    
    human_players: Integer
    The number of human players that play the game 
    
    computer_players: Integer
    The number of computer players who play the game
    
    no_of_cards: Integer
    The number of sets of cards to mix in the deck

    Methods:
    --------
    display_current(self):
        Displays the current hand of the player, dealer. 
    dealtwocards(self):
        This function calls method dealcard() twice for all users to deal the first two cards. 
        Displays player's hand after each turn
    dealtoall(self, first_card):
        This function calls method dealcard() for all the players' and the dealer's decks
    playround(self):   
        This function calls method play() for all the players who are not busted yet, and for the dealer. 
    PrintResults(self):
        Is responsible for displaying the results of the Game

    '''
    def __init__(self, human_players, computer_players, no_of_cards):
        """  
        The function initializes the parameters of class Game
        Responsible for initializing onjects of players, dealers and card decks 

        Parameters
        ----------
        self, human_players, computer_players, no_of_cards
        
        human_players: Integer
        The number of human players that play the game 
        
        computer_players: Integer
        The number of computer players who play the game
        
        no_of_cards: Integer
        The number of sets of cards to mix in the deck

        Variables
        -----------

        self.players : list 
        list of objects of class Player (contains all the players playing the game)

        alphabet : list
        Contains list of alphabets that are used to name the computer players

        """
        self.players = []
        alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O'] 
        for i in range(0, human_players):
                player = Player("Human Player {}".format(i + 1), self,  ishuman = True)
                self.players.append(player)
        for i in range(0, computer_players): 
                player = Player("Computer Player {}".format(alphabet[i]), self, ishuman = False)
                self.players.append(player)

        self.dealer = Player("Dealer", self, isdealer = True )
        self.deck = Deck(no_of_cards)
        self.deck.shuffle_cards()

    def display_current(self):
        """  
        Function display_current(self):
        
        Displays the current hand of the player, dealer. 

        Sample:
        ---------

        If the player 1's cards are ['A of Hearts', '9 of Diamonds']
        it displays -->  Human Player 1's hand: ['A of Hearts', '9 of Diamonds']
        """
        for player in self.players + [self.dealer]:
            print ("{}'s hand: {}".format(player.name, player.cardsnamesinstring()))
            sleep(1.5)

    def dealtwocards(self):
        """  
        Function dealtwocards(self):
        
        This function calls method dealcard() twice for all users to deal the first two cards. 
            self.dealtoall(first_card=True) for first deal, 
            self.dealtoall(first_card=False) for the second deal
        Function displays the player's hand after each turn

        """  
        # Deal one card face up to each player, deal one card face DOWN to himself
        print("\nDealing first card to players:")
        self.dealtoall(first_card=True)
        sleep(1)
        self.display_current()

        # Deal one card face up to each player, deal one card face UP to himself
        print("\nDealing second card to players:")
        self.dealtoall()
        sleep(1)
        self.display_current()

    def dealtoall(self, first_card = False):
        """  
        Function dealtoall(self, first_card):
        
        This function calls method dealcard() for all the players' decks, in other words, it deals cards to all players. 
        Function also calls method dealcard() for the dealer's deck.  

        Parameters
        ----------

        first_card: boolean
        first_card specifies whether the card should be viewable or not (dealer's 1st card is not viewable)
        It is set to True by default
        """      
        for player in self.players:
            self.deck.dealcard(player, visible = True)

        self.deck.dealcard(self.dealer, visible = not first_card)

    def play_round(self):
        """  
        Function playround(self):
        
        This function calls method play() for all the players who are not busted yet. 
        Function also calls method play() for the dealer.        
       
        """   
        for player in [player for player in self.players if not player.busted]:
                player.play()

        self.dealer.play()

    def PrintResults(self):
        """  
        Function PrintResults(self):
        
        A function of class Game.
        Is responsible for displaying the results of the Game, ie. Outputs the busted players, winners, and losers.

        Sample Output
        -----------
        (i) Example 1: Dealer busted, Computer Player A busted, and Human Player 1 wins

        FINAL RESULTS
        Dealer has busted, so everyone still remaining in the game win!
        Winners: Human Player 1
        Busted players: Computer Player A

        (ii) Example 1: Dealer, Human Player 1 both have 19 points. Computer Player 1 has 21 points.
       
        FINAL RESULTS
        Human Player 1 is tied  with the dealer at 19 points.
        Blackjack! Computer Player 1 has won

        Returns
        -------
        
        none

        """   
        print ("\n\t\t\tFINAL RESULTS \n")
        sleep(1.5)

        if self.dealer.busted:
            print ("Dealer has busted, so everyone still remaining in the game wins!")
            print ("Winners: {}".format(", ".join([player.name for player in self.players if not player.busted])))
            print ("Busted players: {}".format(", ".join([player.name for player in self.players if player.busted])))

        else:
            for player in self.players:
                if player.busted:
                    print ("{} has busted".format(player.name))
                elif player.winflag:
                    print("Blackjack! {} has won".format(player.name))
                elif player.points() < self.dealer.points():
                    print ("{} has lost the game with {} points, which is less than the dealer's total of {}.".format(player.name, player.points(), self.dealer.points()))
                elif player.points() == self.dealer.points():
                    if player.points() == 21:
                        print("{} has won the game with 21 points! ".format(player.name))
                    else:
                        print ("{} is tied with the dealer at {} points.".format(player.name, player.points()))
                else:
                    if player.points() == 21:
                        print("Blackjack! {} has won with 21 points".format(player.name))
                    else:
                        print ("{} has won {} points. This is more than the dealer's total of {}. Congrats!".format(player.name, player.points(), self.dealer.points()))


def get_num_players():
    """  
    Function get_num_players:
    
    The function which is responsible for getting input from the user for the number of human players and the 
    number of computer players in the game 
    
    Variables
    -----------

    num_players_char : string
    Takes input from user for the number of human players in the game

    comp_players_char : string
    Takes input from user for the number of computer players in the game

    
    Returns
    -------
    
    [num_players_char,comp_players_char]: int[list]
    Returns a list with integer values of num_players_char and comp_players_char.

    """   
    num_players_char = input("How many human players are playing today? (int) \t")
    comp_players_char = input("How many computer players are playing today? (int)\t")
    return [int(num_players_char),int(comp_players_char)]

def get_num_of_sets():
    """  
    Function get_num_of_sets:
    
    The function which is responsible for getting input from the user for the number of sets of 52 cards to be 
    included in the deck, to make it more unpredictable.
    
    Variables
    -----------

    num_of_sets : string
    Takes input from user for the number of sets of cards in deck
    
    Returns
    -------
    
    num_of_sets: int
    converts the user input to integer and returns the number of sets in deck back to function ActualGame. 

    """   
    num_of_sets = input("\nHow many sets of cards do you want to play with?\nChoose more than 1 to increase random outcomes. (int)   ")
    return int(num_of_sets)

def ActualGame():
    """  
    Function ActualGame:

    The function which is responsible for beginning the blackjack game, also instantiates the Game class.
    Is also responsible for rerunning the game until the user terminates the game.
    If user terminates, it prints "See you later, alligator!"
    
    Variables
    -----------

    num_players : list
    Gets the number of human (num_players[0]) and computer players (num_players[1]) from the function get_num_players

    no_of_cards : int
    Gets the number of sets of 52 cards that is to be included in deck to increase unpredictability

    game : object
    Instantiates the Game class in order to start the game

    play_again: string of
    Prompts the user to decide whether to play another round or not

    Returns
    -------
    
    ActualGame: Function
    Calls itself recursively if the user chooses to play again

    """   
    num_players = get_num_players()
    print ("\nGreat! Let's play with {} human player(s) and {} computer player(s).".format(num_players[0],num_players[1]))
    no_of_cards = get_num_of_sets()
    game = Game(num_players[0], num_players[1], no_of_cards)
    game.dealtwocards()
    game.play_round()
    game.PrintResults()

    play_again = str(input("\nWould you like to play again? ('yes' or 'no'): "))
    if play_again != 'yes':
        print ("\nSee you later, alligator!")
        quit()
    else:
        print("\n\n\n")
        ActualGame()

if __name__ == '__main__':
    #main function (where the game actually starts)
    ActualGame()
    
    
        
