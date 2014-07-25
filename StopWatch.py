# template for "Stopwatch: The Game"

import simplegui

# define global variables

count = 0
status, last_status = False, False
x, y = 0, 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    tsec = t % 10
    min = t // 10 // 60
    sec = t // 10 % 60
    time = ""
    time += str(min) + ":"
    if sec < 10:
        time += "0" + str(sec)
    else:
        time += str(sec)
    time += "." + str(tsec)
    return time    
    
# define event handlers for buttons; "Start", "Stop", "Reset"

def start():
    global status, last_status
    status, last_status = True, True
def stop():
    global status, x, y, last_status
    status = False
    if last_status:
        if count % 10 == 0:
            x += 1
            y += 1
        else:
            y += 1
    last_status = False
def reset():
    global count, status, last_status, x, y
    status, last_status = False, False
    count, x, y = 0, 0, 0

# define event handler for timer with 0.1 sec interval

def timer_handler():
    global count
    if status:
        count += 1

# define draw handler

def draw_handler(canvas):
    canvas.draw_text(format(count), (45, 110), 40, "White")
    canvas.draw_text(str(x) + "/" + str(y), (150, 40), 30, "Green")
# create frame

frame = simplegui.create_frame("Stopwatch: The Game", 200, 200)
start = frame.add_button("Start", start, 60)
stop = frame.add_button("Stop", stop, 60)
reset = frame.add_button("Reset", reset, 60)
timer = simplegui.create_timer(100, timer_handler)

# register event handlers

frame.set_draw_handler(draw_handler)

# start frame

frame.start()
timer.start()

# Please remember to review the grading rubric
