import pygame
from pygame import locals

# Window Settings
WIN_WIDTH = 1400
WIN_HEIGHT = 850
FPS = 60
SPEED = 1
Running = True

# Pads Settings
PAD_WIDTH = 20
PAD_HEIGHT = 100
PAD_LEFT = [PAD_WIDTH, 0]
PAD_RIGHT = [WIN_WIDTH-PAD_WIDTH*2, 0]

# Ball Settings
BALL_RADIUS = 5
BALL = [WIN_WIDTH/2 - BALL_RADIUS/2, WIN_HEIGHT/2 - BALL_RADIUS/2]
BALL_vX = 1
BALL_vY = 1

# Colors
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)

points = 0

screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
clock = pygame.time.Clock()

def keys():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION: #easier than with keys
            if WIN_HEIGHT - PAD_HEIGHT >= event.pos[1]:
                PAD_LEFT[1] = event.pos[1]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                global Running
                Running = False

def checkBall():
    global BALL, BALL_vX, BALL_vY, points, SPEED

    if BALL[0] <= 0 or BALL[0] >= WIN_WIDTH: #Left & Right bounce (without pad)
        BALL = [WIN_WIDTH/2 - BALL_RADIUS/2, WIN_HEIGHT/2 - BALL_RADIUS/2]
        points -= 1
        SPEED = 1
    if BALL[1] <= 0+BALL_RADIUS or BALL[1] >= WIN_HEIGHT-BALL_RADIUS: #Top & Bottom bounce 
        BALL_vY = -BALL_vY

    if BALL[0] <= PAD_WIDTH*2+BALL_RADIUS: #Left bounce 
        if BALL[1] >= PAD_LEFT[1] and BALL[1] <= PAD_LEFT[1]+PAD_HEIGHT: #Left & Right bounce (with pad)
            BALL_vX = -BALL_vX
            SPEED += 1
    elif BALL[0] >= WIN_WIDTH-PAD_WIDTH*2-10: #Right bounce
        if BALL[1] >= PAD_RIGHT[1] and BALL[1] <= PAD_RIGHT[1]+PAD_HEIGHT: #Left & Right bounce (with pad)
            BALL_vX = -BALL_vX
            SPEED += 1

def moveBall():
    for _ in range(SPEED+1):
        checkBall()
        aimBall()
        BALL[0] -= BALL_vX
        BALL[1] -= BALL_vY 

def aimBall():
    if BALL[1] >= 0+PAD_HEIGHT/2 and BALL[1] <= WIN_HEIGHT-PAD_HEIGHT/2:
        PAD_RIGHT[1] = BALL[1]-PAD_HEIGHT/2
        PAD_LEFT[1] = BALL[1]-PAD_HEIGHT/2 # Delete this line to play with the mouse

def drawPADS():
    pygame.draw.rect(screen, color=blue, rect=(PAD_LEFT[0], PAD_LEFT[1], PAD_WIDTH, PAD_HEIGHT), border_radius=5)
    pygame.draw.rect(screen, color=red, rect=(PAD_RIGHT[0], PAD_RIGHT[1], PAD_WIDTH, PAD_HEIGHT), border_radius=5)

def drawBALL():
    pygame.draw.circle(screen, green, BALL, BALL_RADIUS)

while Running:
    pygame.display.set_caption("PONG : {}pts | {} FPS | {} SPEED".format(points, int(clock.get_fps()), SPEED))

    keys()
    moveBall()

    # Graphical part
    screen.fill((0, 0, 0)) # Reset Frame
    drawPADS()
    drawBALL()

    # Update Rendering
    clock.tick(FPS)
    pygame.display.flip()
