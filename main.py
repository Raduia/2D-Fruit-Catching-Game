
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math
import sys


WIDTH = 900
HEIGHT = 650

basket_x = 450
basket_y = 65

score = 0
lives = 3

game_state = "MENU"
difficulty = "MEDIUM"

fruits = []
particles = []
popups = []

spawn_counter = 0
animation_time = 0

fruit_speed = 4
spawn_rate = 45

cloud_positions = [100, 350, 600]

# BASIC DRAWING
def rectangle(x1, y1, x2, y2, color):
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()

def gradient_rect(x1, y1, x2, y2, bottom, top):
    glBegin(GL_QUADS)

    glColor3f(*bottom)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)

    glColor3f(*top)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)

    glEnd()

def circle(x, y, radius, color, alpha=1.0):
    glColor4f(color[0], color[1], color[2], alpha)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)

    for i in range(101):
        angle = 2 * math.pi * i / 100
        glVertex2f(
            x + radius * math.cos(angle),
            y + radius * math.sin(angle)
        )

    glEnd()

def ellipse(x, y, rx, ry, color, alpha=1.0):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glScalef(rx, ry, 1)
    circle(0, 0, 1, color, alpha)
    glPopMatrix()

def text(x, y, message, color=(1, 1, 1),
         font=GLUT_BITMAP_HELVETICA_18):

    glColor3f(*color)
    glRasterPos2f(x, y)

    for ch in message:
        glutBitmapCharacter(font, ord(ch))

# SUN
def draw_sun():

    for i in range(8, 0, -1):
        circle(
            750, 535,
            42 + i * 12,
            (1.0, 0.85, 0.25),
            0.035
        )

    circle(750, 535, 43, (1.0, 0.82, 0.12))

    circle(
        737, 549, 13,
        (1.0, 0.97, 0.65),
        0.85
    )


# CLOUDS
def draw_cloud(x, y):

    color = (1, 1, 1)

    ellipse(x, y, 35, 17, color, 0.95)
    ellipse(x + 25, y + 10, 25, 24, color, 0.95)
    ellipse(x + 52, y, 35, 18, color, 0.95)
    ellipse(x + 25, y - 5, 38, 16, color, 0.95)

# BIRDS
def draw_birds():

    glColor3f(0.12, 0.18, 0.25)
    glLineWidth(2)

    for x, y in [
        (180, 480),
        (240, 455),
        (300, 490),
        (400, 465)
    ]:

        glBegin(GL_LINE_STRIP)
        glVertex2f(x - 10, y)
        glVertex2f(x, y + 7)
        glVertex2f(x + 10, y)
        glEnd()

# BEAUTIFUL TREES
def draw_tree(x, y, size=1):

    glPushMatrix()

    glTranslatef(x, y, 0)
    glScalef(size, size, 1)

    # Tree shadow
    ellipse(0, 0, 48, 10, (0.02, 0.12, 0.02), 0.35)

    # Tree trunk
    gradient_rect(
        -11, 0, 11, 125,
        (0.30, 0.10, 0.02),
        (0.72, 0.40, 0.13)
    )

    # Tree branches
    glColor3f(0.38, 0.17, 0.04)
    glLineWidth(8)

    glBegin(GL_LINES)
    glVertex2f(0, 65)
    glVertex2f(-35, 120)
    glVertex2f(0, 80)
    glVertex2f(35, 125)
    glVertex2f(-5, 95)
    glVertex2f(-15, 140)
    glEnd()

    # Dark green leaves
    circle(-35, 125, 34, (0.04, 0.34, 0.08))
    circle(30, 130, 36, (0.04, 0.38, 0.08))
    circle(0, 155, 43, (0.05, 0.45, 0.09))
    circle(-35, 165, 29, (0.08, 0.52, 0.10))
    circle(35, 165, 30, (0.07, 0.48, 0.09))
    circle(0, 190, 30, (0.10, 0.57, 0.12))

    # Light green highlights
    circle(-15, 175, 15, (0.28, 0.75, 0.18))
    circle(25, 150, 13, (0.25, 0.72, 0.16))
    circle(-42, 140, 11, (0.30, 0.78, 0.20))
    circle(5, 195, 10, (0.35, 0.82, 0.22))

    glPopMatrix()

# SMALL FLOWERS
def draw_flower(x, y, color):

    # Stem
    glColor3f(0.04, 0.35, 0.05)
    glLineWidth(2)

    glBegin(GL_LINES)
    glVertex2f(x, y)
    glVertex2f(x, y + 12)
    glEnd()

    # Leaves
    ellipse(x - 4, y + 6, 4, 2, (0.10, 0.60, 0.12))
    ellipse(x + 4, y + 9, 4, 2, (0.15, 0.72, 0.15))

    # Petals
    circle(x - 4, y + 15, 3, color)
    circle(x + 4, y + 15, 3, color)
    circle(x, y + 19, 3, color)
    circle(x, y + 11, 3, color)

    # Center
    circle(x, y + 15, 2, (1.0, 0.78, 0.02))

# FENCE
def draw_fence():

    glColor3f(0.48, 0.25, 0.08)
    glLineWidth(7)
    glBegin(GL_LINES)
    for x in range(0, 901, 80):
        glVertex2f(x, 70)
        glVertex2f(x, 125)

    glVertex2f(0, 85)
    glVertex2f(900, 85)
    glVertex2f(0, 110)
    glVertex2f(900, 110)
    glEnd()

# BACKGROUND
def draw_background():

    # Sky
    gradient_rect(
        0, 0, WIDTH, HEIGHT,
        (0.12, 0.38, 0.72),
        (0.42, 0.82, 0.98)
    )

    draw_sun()

    # Clouds
    for x in cloud_positions:
        draw_cloud(x, 510)

    draw_birds()

    # Mountains
    glBegin(GL_TRIANGLES)

    glColor3f(0.40, 0.68, 0.67)

    glVertex2f(0, 130)
    glVertex2f(160, 330)
    glVertex2f(350, 130)
    glVertex2f(250, 130)
    glVertex2f(520, 350)
    glVertex2f(780, 130)
    glVertex2f(650, 130)
    glVertex2f(820, 310)
    glVertex2f(900, 130)
    glEnd()

    # Green hills
    ellipse(120, 100, 240, 90, (0.20, 0.58, 0.28))
    ellipse(500, 95, 300, 105, (0.16, 0.53, 0.23))
    ellipse(850, 100, 230, 95, (0.22, 0.60, 0.27))

    # Trees
    draw_tree(45, 25, 1.15)
    draw_tree(145, 25, 1.30)
    draw_tree(270, 25, 1.05)
    draw_tree(390, 25, 0.90)

    draw_tree(570, 25, 1.00)
    draw_tree(690, 25, 1.25)
    draw_tree(800, 25, 1.15)
    draw_tree(880, 25, 1.30)

    # Ground
    gradient_rect(
        0, 0, WIDTH, 85,
        (0.03, 0.25, 0.05),
        (0.25, 0.68, 0.16)
    )

    # Fence
    draw_fence()

    # Flowers only on lower ground
    flower_colors = [
        (1.0, 0.12, 0.25),
        (1.0, 0.35, 0.75),
        (1.0, 0.85, 0.05),
        (0.65, 0.20, 1.0),
        (1.0, 0.50, 0.10),
        (0.95, 0.95, 1.0),
        (0.10, 0.65, 1.0)
    ]

    positions = [
        (75, 5),
        (125, 20),
        (205, 8),
        (245, 25),
        (335, 6),
        (375, 20),
        (455, 8),
        (495, 24),
        (585, 6),
        (625, 20),
        (705, 8),
        (745, 24),
        (825, 6)
    ]

    for i, (x, y) in enumerate(positions):
        draw_flower(
            x, y,
            flower_colors[i % len(flower_colors)]
        )


# BEAUTIFUL WOVEN BASKET
def draw_basket():

    # Basket shadow
    ellipse(
        basket_x, basket_y - 5,
        75, 12,
        (0.02, 0.05, 0.02), 0.4
    )

    # Curved handle
    glColor3f(0.45, 0.20, 0.04)
    glLineWidth(10)

    glBegin(GL_LINE_STRIP)

    for i in range(51):
        angle = math.pi * i / 50

        x = basket_x + 48 * math.cos(angle)
        y = basket_y + 45 + 48 * math.sin(angle)

        glVertex2f(x, y)

    glEnd()

    # Handle highlight
    glColor3f(0.90, 0.58, 0.22)
    glLineWidth(3)

    glBegin(GL_LINE_STRIP)

    for i in range(51):
        angle = math.pi * i / 50

        x = basket_x + 48 * math.cos(angle)
        y = basket_y + 45 + 48 * math.sin(angle)

        glVertex2f(x, y)

    glEnd()

    # Basket body
    gradient_rect(
        basket_x - 60,
        basket_y,
        basket_x + 60,
        basket_y + 48,
        (0.35, 0.12, 0.02),
        (0.95, 0.55, 0.12)
    )

    # Vertical weaving
    glColor3f(0.55, 0.25, 0.04)
    glLineWidth(4)

    glBegin(GL_LINES)

    for x in range(-48, 49, 16):
        glVertex2f(basket_x + x, basket_y + 4)
        glVertex2f(basket_x + x, basket_y + 44)

    glEnd()

    # Horizontal weaving
    glColor3f(1.0, 0.72, 0.28)
    glLineWidth(3)

    glBegin(GL_LINES)

    for y in [12, 24, 36]:
        glVertex2f(basket_x - 55, basket_y + y)
        glVertex2f(basket_x + 55, basket_y + y)

    glEnd()

    # Top rim
    glColor3f(0.95, 0.68, 0.22)
    glLineWidth(8)

    glBegin(GL_LINES)
    glVertex2f(basket_x - 62, basket_y + 47)
    glVertex2f(basket_x + 62, basket_y + 47)
    glEnd()

    # Bottom border
    glColor3f(0.38, 0.15, 0.02)
    glLineWidth(5)

    glBegin(GL_LINES)
    glVertex2f(basket_x - 52, basket_y + 3)
    glVertex2f(basket_x + 52, basket_y + 3)
    glEnd()

    # Basket shine
    ellipse(
        basket_x - 40, basket_y + 35,
        5, 4,
        (1, 0.9, 0.55), 0.8
    )


# FRUIT DRAWING
def draw_fruit(f):

    x = f["x"]
    y = f["y"]

    kind = f["kind"]

    if kind == "APPLE":
        base = (0.85, 0.02, 0.03)
        light = (1.0, 0.25, 0.25)

    elif kind == "ORANGE":
        base = (0.95, 0.30, 0.0)
        light = (1.0, 0.70, 0.15)

    else:
        base = (0.95, 0.70, 0.0)
        light = (1.0, 0.95, 0.25)

    ellipse(x + 5, y - 8, 20, 7, (0, 0, 0), 0.25)

    circle(x, y, 18, base)
    circle(x - 5, y + 6, 10, light, 0.8)

    ellipse(x - 7, y + 10, 4, 7, (1, 1, 1), 0.7)

    glColor3f(0.25, 0.12, 0.02)
    glLineWidth(3)

    glBegin(GL_LINES)
    glVertex2f(x, y + 15)
    glVertex2f(x + 3, y + 26)
    glEnd()

    ellipse(x + 9, y + 22, 8, 4, (0.05, 0.65, 0.08))

# FRUIT SPAWNING
def spawn_fruit():

    fruits.append({
        "x": random.randint(30, WIDTH - 30),
        "y": HEIGHT - 70,
        "kind": random.choice([
            "APPLE",
            "ORANGE",
            "MANGO"
        ])
    })

# PARTICLES
def create_particles(x, y):

    for i in range(15):

        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 4)

        particles.append({
            "x": x,
            "y": y,
            "vx": math.cos(angle) * speed,
            "vy": math.sin(angle) * speed,
            "life": 25,
            "color": random.choice([
                (1, 0.9, 0.1),
                (1, 1, 1),
                (1, 0.4, 0.1)
            ])
        })


def draw_particles():

    for p in particles:

        alpha = max(0, p["life"] / 25)

        circle(
            p["x"], p["y"],
            3,
            p["color"],
            alpha
        )


# SCORE POPUP
def create_popup(x, y):

    popups.append({
        "x": x,
        "y": y,
        "life": 35
    })


def draw_popups():

    for p in popups:
        text(
            p["x"], p["y"],
            "+10",
            (1, 1, 0.1)
        )

# DIFFICULTY SETTINGS
def set_difficulty(level):

    global difficulty
    global fruit_speed, spawn_rate

    difficulty = level

    if level == "EASY":
        fruit_speed = 3
        spawn_rate = 65

    elif level == "MEDIUM":
        fruit_speed = 4
        spawn_rate = 45

    else:
        fruit_speed = 6
        spawn_rate = 30


# START GAME
def start_game():

    global score, lives
    global basket_x, game_state
    global spawn_counter

    score = 0
    lives = 3

    basket_x = WIDTH // 2

    fruits.clear()
    particles.clear()
    popups.clear()

    spawn_counter = 0

    game_state = "PLAYING"

# UPDATE GAME
def update(value):

    global score, lives
    global game_state
    global spawn_counter
    global animation_time

    animation_time += 1

    # Cloud animation
    for i in range(len(cloud_positions)):

        cloud_positions[i] += 0.3

        if cloud_positions[i] > WIDTH + 70:
            cloud_positions[i] = -70

    # Particle animation
    for p in particles[:]:

        p["x"] += p["vx"]
        p["y"] += p["vy"]

        p["vy"] -= 0.08
        p["life"] -= 1

        if p["life"] <= 0:
            particles.remove(p)

    # Popup animation
    for p in popups[:]:

        p["y"] += 1
        p["life"] -= 1

        if p["life"] <= 0:
            popups.remove(p)

    # Main game
    if game_state == "PLAYING":

        spawn_counter += 1

        if spawn_counter >= spawn_rate:
            spawn_fruit()
            spawn_counter = 0

        for f in fruits[:]:

            f["y"] -= fruit_speed

            # Collision detection
            if (
                basket_x - 55 < f["x"] < basket_x + 55
                and basket_y < f["y"] < basket_y + 55
            ):

                score += 10

                create_particles(f["x"], f["y"])
                create_popup(f["x"], f["y"])

                fruits.remove(f)

            # Missed fruit
            elif f["y"] < 20:

                lives -= 1
                fruits.remove(f)

                if lives <= 0:
                    game_state = "GAMEOVER"

    glutPostRedisplay()
    glutTimerFunc(30, update, 0)

# HUD
def draw_hud():

    rectangle(
        0, HEIGHT - 65,
        WIDTH, HEIGHT,
        (0.04, 0.12, 0.25)
    )

    text(
        20, HEIGHT - 38,
        "FRUIT CATCHER",
        (1, 0.85, 0.1)
    )

    text(
        320, HEIGHT - 38,
        "SCORE: " + str(score)
    )

    text(
        510, HEIGHT - 38,
        "LIVES: " + str(lives)
    )

    text(
        720, HEIGHT - 38,
        difficulty
    )

# GAME MODE MENU
def draw_menu():

    draw_background()

    rectangle(
        180, 165,
        720, 490,
        (0.02, 0.10, 0.18)
    )

    glColor3f(0.95, 0.75, 0.20)
    glLineWidth(4)

    glBegin(GL_LINE_LOOP)

    glVertex2f(180, 165)
    glVertex2f(720, 165)
    glVertex2f(720, 490)
    glVertex2f(180, 490)

    glEnd()

    text(
        285, 440,
        "FRUIT CATCHING GAME",
        (1, 0.9, 0.1),
        GLUT_BITMAP_TIMES_ROMAN_24
    )

    text(
        345, 390,
        "SELECT GAME MODE",
        (1, 1, 1)
    )

    modes = [
        ("1. EASY", "EASY", 330, (0.15, 0.65, 0.20)),
        ("2. MEDIUM", "MEDIUM", 270, (0.85, 0.55, 0.05)),
        ("3. HARD", "HARD", 210, (0.75, 0.12, 0.12))
    ]

    for label, level, y, color in modes:

        if difficulty == level:
            button_color = color
            text_color = (1, 1, 1)
        else:
            button_color = (0.12, 0.20, 0.27)
            text_color = (0.75, 0.85, 0.90)

        rectangle(
            300, y - 12,
            600, y + 25,
            button_color
        )

        if difficulty == level:

            glColor3f(1, 0.9, 0.25)
            glLineWidth(3)

            glBegin(GL_LINE_LOOP)

            glVertex2f(300, y - 12)
            glVertex2f(600, y - 12)
            glVertex2f(600, y + 25)
            glVertex2f(300, y + 25)

            glEnd()

        text(
            390, y,
            label,
            text_color
        )

    text(
        325, 175,
        "PRESS ENTER TO START",
        (1, 0.9, 0.2)
    )

# PAUSE SCREEN
def draw_pause():

    rectangle(
        220, 250,
        680, 410,
        (0.03, 0.08, 0.18)
    )

    text(
        365, 345,
        "GAME PAUSED",
        (1, 0.85, 0.1),
        GLUT_BITMAP_TIMES_ROMAN_24
    )

    text(
        325, 295,
        "PRESS SPACE TO RESUME"
    )

# GAME OVER
def draw_gameover():

    rectangle(
        200, 180,
        700, 460,
        (0.03, 0.08, 0.18)
    )

    glColor3f(0.95, 0.75, 0.20)
    glLineWidth(4)

    glBegin(GL_LINE_LOOP)
    glVertex2f(200, 180)
    glVertex2f(700, 180)
    glVertex2f(700, 460)
    glVertex2f(200, 460)
    glEnd()

    text(
        355, 400,
        "GAME OVER!",
        (1, 0.15, 0.15),
        GLUT_BITMAP_TIMES_ROMAN_24
    )

    text(
        355, 350,
        "FINAL SCORE: " + str(score)
    )

    text(
        315, 305,
        "PRESS R TO RESTART",
        (1, 1, 1)
    )

    text(
        285, 260,
        "PRESS M TO CHANGE GAME MODE",
        (1, 0.85, 0.1)
    )

    text(
        330, 215,
        "PRESS ESC TO EXIT",
        (1, 1, 1)
    )

# DISPLAY
def display():

    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    if game_state == "MENU":

        draw_menu()

    else:

        draw_background()

        # Fruits
        for f in fruits:
            draw_fruit(f)

        # Basket
        draw_basket()

        # Effects
        draw_particles()
        draw_popups()

        # HUD
        draw_hud()

        if game_state == "PAUSED":
            draw_pause()

        elif game_state == "GAMEOVER":
            draw_gameover()

    glutSwapBuffers()

# KEYBOARD
def keyboard(key, x, y):

    global game_state

    # Exit
    if key == b'\x1b':
        sys.exit()

    # MENU
    if game_state == "MENU":

        if key == b'1':
            set_difficulty("EASY")

        elif key == b'2':
            set_difficulty("MEDIUM")

        elif key == b'3':
            set_difficulty("HARD")

        elif key == b'\r':
            start_game()

    # PAUSE / RESUME
    elif key == b' ':

        if game_state == "PLAYING":
            game_state = "PAUSED"

        elif game_state == "PAUSED":
            game_state = "PLAYING"

    # GAME OVER OPTIONS
    elif game_state == "GAMEOVER":

        if key in (b'r', b'R'):
            start_game()

        elif key in (b'm', b'M'):
            game_state = "MENU"

    glutPostRedisplay()

# SPECIAL KEYS
def special_keys(key, x, y):

    global basket_x

    if game_state != "PLAYING":
        return

    if key == GLUT_KEY_LEFT:
        basket_x -= 35

    elif key == GLUT_KEY_RIGHT:
        basket_x += 35

    basket_x = max(
        60,
        min(WIDTH - 60, basket_x)
    )
    glutPostRedisplay()

# OPENGL INITIALIZATION
def init():
    glClearColor(0, 0, 0, 1)
    glEnable(GL_BLEND)
    glBlendFunc(
        GL_SRC_ALPHA,
        GL_ONE_MINUS_SRC_ALPHA
    )
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(
        0, WIDTH,
        0, HEIGHT
    )

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# MAIN
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutInitWindowPosition(100, 50)
    glutCreateWindow(b"2D Fruit Catching Game - Cartoon Garden")
    set_difficulty("MEDIUM")
    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutTimerFunc(30, update, 0)
    glutMainLoop()
if __name__ == "__main__":
    main()
