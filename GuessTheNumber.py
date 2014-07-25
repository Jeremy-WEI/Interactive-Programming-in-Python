# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
from random import randrange

# initialize global variables used in your code

num_range = 100
secret_number = randrange(100);
guess_left = 7

# helper function to start and restart the game
def new_game():
    global secret_number, guess_left
    secret_number = randrange(num_range)
    if num_range == 100:
        guess_left = 7
    if num_range == 1000:
        guess_left = 10
    print "New game: Range is from 0 to", num_range
    print "Number of remaining guesses is", guess_left
    print

# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    global num_range
    num_range = 100
    new_game() 

def range1000():
    # button that changes range to range [0,1000) and restarts
    global num_range, guess_left
    num_range = 1000
    new_game() 
    
def input_guess(guess):
    # main game logic goes here
    global guess_left
    guess_left -= 1
    number_guess = int(guess)
    print "Guess was", number_guess
    print "Number of remaining guesses is", guess_left
    if number_guess == secret_number:
        print "Congratulations! You've got the right number!"
        print
        new_game()
    elif number_guess < secret_number:
        print "Higher"
        print
    else:
        print "Lower"
        print
    if guess_left == 0:
        print "You've run out of guesses. You lose!"
        print "The right number is", secret_number
        print
        new_game()
        
# create frame

frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements

frame.add_button("Range: 0 - 100", range100, 200)
frame.add_button("Range: 0 - 1000", range1000, 200)
frame.add_input("Enter a guess", input_guess, 200)

# call new_game and start frame

new_game()
frame.start();

# always remember to check your completed program against the grading rubric
