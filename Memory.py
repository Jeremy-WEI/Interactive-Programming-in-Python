# implementation of card game - Memory

import simplegui
import random

game_state = 0
turns = 0
difficulty = 8
card_list = []
exposed_list = []
index_list=[]
width = 50.
color_dictionary = {0: "Aqua", 1: "Blue", 2: "Fuchsia", 3: "Green", 4: "Lime", 5: "Maroon", 6: "Navy", 7: "Olive", \
                    8: "Orange", 9: "Purple", 10: "Red", 11: "Silver", 12: "White", 13: "Yellow"}

def new_game():
    global card_list, exposed_list, index_list, game_state, turns, width, difficulty
    turns = 0
    game_state = 0
    width = 400. / difficulty
    index_list = []
    card_list = range(difficulty) * 2
    random.shuffle(card_list)
    exposed_list = [False] * difficulty * 2

def increase_difficulty():
    global difficulty
    if difficulty <= 13:
        difficulty += 1
    label1.set_text("Difficulty = %d" % difficulty)
    
def decrease_difficulty():
    global difficulty
    if difficulty >= 6:
        difficulty -= 1
    label1.set_text("Difficulty = %d" % difficulty)
    
def mouseclick(pos):
    global exposed_list, index_list, game_state, turns
    if game_state == 2:
        if card_list[index_list[0]] != card_list[index_list[1]]:
            exposed_list[index_list[0]], exposed_list[index_list[1]] = False, False
        game_state = 0
        index_list = []
    i = pos[0] // width
    if not exposed_list[i]:
        exposed_list[i] = True
        game_state += 1
        index_list.append(i)   
        if game_state == 2:
            turns += 1
      
def draw(canvas):
    i = 0
    for n in card_list:
        if exposed_list[i]:
            canvas.draw_polygon([(i * width, 0), ((i + 1) * width, 0), ((i + 1) * width, 180), \
                                 (i * width, 180)], 1, color_dictionary[n], color_dictionary[n])
        canvas.draw_line((width * i, 0), (width * i, 180), 3, "Black")
        i += 1
    canvas.draw_line((800,0), (800, 180), 3, "Black")
    label2.set_text("Turns = %d" % turns)
    
frame = simplegui.create_frame("Memory", 800, 180)
frame.set_canvas_background("Gray")
frame.add_button("Reset", new_game)
label1 = frame.add_label("Difficulty = 8")
frame.add_button("Increase Difficulty", increase_difficulty)
frame.add_button("Decrease Difficulty", decrease_difficulty)
label2 = frame.add_label("Turns = 0")

frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

new_game()
frame.start()
