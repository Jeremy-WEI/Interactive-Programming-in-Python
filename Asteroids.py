# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def draw(self,canvas):
        if self.thrust == False:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        if self.thrust:
            forward = angle_to_vector(self.angle)
        else:
            forward = [0, 0]
        self.vel[0] = 0.95 * self.vel[0] + forward[0]
        self.vel[1] = 0.95 * self.vel[1] + forward[1]
            
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
    def thruston(self):
        self.thrust = True
        ship_thrust_sound.play()
        
    def thrustoff(self):
        self.thrust = False
        ship_thrust_sound.rewind()
    
    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_group.add(Sprite([self.pos[0] + forward[0] * 45, self.pos[1] + forward[1] * 45], [self.vel[0] + 10 * forward[0], self.vel[1] + 10 * forward[1]], self.angle, 0, missile_image, missile_info, missile_sound))
        
    def keydown(self, key):
        if key == simplegui.KEY_MAP['left']:
            self.angle_vel -= 0.1
        if key == simplegui.KEY_MAP['right']:
            self.angle_vel += 0.1
        if key == simplegui.KEY_MAP['up']:
            self.thruston()
        if key == simplegui.KEY_MAP['space']:
            self.shoot()

    def keyup(self, key):
        if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['right']:
            self.angle_vel = 0
        if key == simplegui.KEY_MAP['up']:
            self.thrustoff()
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.time = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self, canvas):
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + self.time * self.image_size[0], self.image_center[1]], self.image_size, self.pos, self.image_size)
            self.time += 1
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
            
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.age += 1
        if self.age >= self.lifespan:
            return True
        return False
        
    def collide(self, other_object):
        if dist(self.get_position(), other_object.get_position()) < self.get_radius() + other_object.get_radius():
           return True
        return False
    
def draw(canvas):
    global time, lives, score, started, missile_group, rock_group, explosion_group, soundtrack
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text('LIVES:', (40, 40), 20, 'White', 'sans-serif')
    canvas.draw_text(str(lives), (40, 70), 20, 'White', 'sans-serif')
    canvas.draw_text('SCORE:', (650, 40), 20, 'White', 'sans-serif')
    canvas.draw_text(str(score), (650, 70), 20, 'White', 'sans-serif')
    
    # draw ship and sprites
    my_ship.draw(canvas)
    if started:
    # update ship and sprites
        my_ship.update()
        process_sprite_group(rock_group, canvas)
        process_sprite_group(missile_group, canvas)
        process_sprite_group(explosion_group, canvas)
        if group_collide(rock_group, my_ship):
            lives -= 1
        score += 10 * group_group_collide(missile_group, rock_group)
        if lives <= 0:
            started = False
            lives = 3
            score = 0
            missile_group = set([])
            rock_group = set([])
            explosion_group = set([])
            soundtrack.rewind()
            soundtrack.play()
    else: 
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())

def keydown_handler(key):
    my_ship.keydown(key)

def keyup_handler(key):
    my_ship.keyup(key)

def mouseclick_handler(position):
    global started
    if not started:
        started = True
    
def process_sprite_group(sprite_group, canvas):
    for sprite in list(sprite_group):
        if sprite.update():
            sprite_group.remove(sprite)
        else:
            sprite.draw(canvas)
        
def group_collide(sprite_group, other_object):
    global explosion_group
    remove_group = set([])
    for sprite in list(sprite_group):
        if sprite.collide(other_object):
            sprite_group.remove(sprite)
            explosion_group.add(Sprite(sprite.get_position(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound))
            return True
    return False

def group_group_collide(first_group, second_group):
    num = 0
    for first_sprite in list(first_group):
        if group_collide(second_group, first_sprite):
            num += 1
            first_group.discard(first_sprite)
    return num
    
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, started
    vel_index = score // 100 + 1
    if started:
        if len(rock_group) < 12:
            new_rock = Sprite([random.random() * WIDTH, random.random() * HEIGHT], [vel_index * random.choice([1, -1]) * random.random(), vel_index * random.choice([1, -1]) * random.random()], 0, random.choice([1, -1]) * random.random() / 30, asteroid_image, asteroid_info)
            if dist(new_rock.get_position(), my_ship.get_position()) > my_ship.get_radius() + new_rock.get_radius() + 10:
                rock_group.add(new_rock)
 
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)
frame.set_mouseclick_handler(mouseclick_handler)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
soundtrack.play()