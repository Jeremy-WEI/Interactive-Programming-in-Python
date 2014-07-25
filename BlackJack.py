# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
message = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.card_list = []

    def __str__(self):
        # return a string representation of a hand
        representation = "Hands contains "
        for card in self.card_list:
            representation += str(card) + " "
        return representation
    
    def add_card(self, card):
        # add a card object to a hand
        self.card_list.append(card)
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        has_ace = False
        for card in self.card_list:
            value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                has_ace = True;
        if has_ace:
            if value <= 11:
                value += 10
        return value
    
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for i in range(len(self.card_list)):
            self.card_list[i].draw(canvas, (pos[0]+100 * i, pos[1]))
            
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck_list = []
        for i in SUITS:
            for j in RANKS:
                self.deck_list.append(Card(i, j))

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.deck_list)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck_list.pop()
    
    def __str__(self):
        # return a string representing the deck
        representation = "Deck contains "
        for card in self.deck_list:
            representation += str(card) + " "
        return representation

#define event handlers for buttons
def deal():
    global message, outcome, in_play, deck, player_hand, dealer_hand, score
    # your code goes here
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()
    deck.shuffle()
    for i in range(2):
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
    if in_play:
        outcome = "Redeal Loses 1 score."
        score -= 1
    else:
        outcome = ""
    in_play = True
    message = "Hit Or Stand?"

def hit():
    # replace with your code below
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    global outcome, score, message, in_play
    if in_play:
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            in_play = False
            outcome = "Busted. YOU LOSE!" 
            score -= 1
            message = "New Deal?"
        
def stand():
    # replace with your code below
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    global outcome, score, message, in_play
    if in_play:
        in_play = False
        message = "New Deal?"
        while dealer_hand.get_value() < 17 and dealer_hand.get_value() < player_hand.get_value():
            dealer_hand.add_card(deck.deal_card())
        if (dealer_hand.get_value() > 21):
            outcome = "Dealer has busted, YOU WIN!"
            score += 1
        elif dealer_hand.get_value() >= player_hand.get_value():
            outcome = "YOU LOSE!"
            score -= 1
        else:
            outcome = "YOU WIN!"
            score += 1
            
# draw handler    
def draw(canvas):
    global in_play
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("BLACKJACK", (80, 100), 50, "Red", "sans-serif")
    canvas.draw_text("Dealer", (80, 180), 25, "Black", "sans-serif")
    canvas.draw_text("Player", (80, 380), 25, "Black", "sans-serif")
    canvas.draw_text(outcome, (200, 180), 25, "Black", "sans-serif")
    canvas.draw_text(message, (200, 380), 25, "Black", "sans-serif")
    canvas.draw_text("SCORE: " + str(score), (400, 100), 30, "Black", "sans-serif")
    dealer_hand.draw(canvas, (85.5, 210))
    player_hand.draw(canvas, (85.5, 410))
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (121, 258), CARD_BACK_SIZE)

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)
deck = Deck()
player_hand = Hand()
dealer_hand = Hand()

# get things rolling
deal()
frame.start()


# remember to review the gradic rubric