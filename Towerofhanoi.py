# ===============================================
# Tower of Hanoi Game 
# Using Python & Firebase
# ===============================================

# -----------------------------
# Import Statements
# -----------------------------
import pygame
import sys
import time
import pyttsx3      # Added for that sound
import webbrowser   # Added for Play Again button

# -----------------------------
# Initialization
# -----------------------------

pygame.init()
pygame.display.set_caption("Towers of Hanoi")
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
framerate = 60

# -----------------------------
# Game Variables
# -----------------------------
game_done = False
steps = 0
disks = []
towers_midx = [120, 320, 520]
pointing_at = 0
floating = False
floater = 0

# -----------------------------
# Colors
# -----------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GOLD = (239, 229, 51)
BLUE = (78,162,196) 
GREY = (170, 170, 170)
GREEN = (77, 206, 145)

# -----------------------------
# User Input Arguments
# -----------------------------

# Check if Flask passed arguments
if len(sys.argv) >= 3:
    username = sys.argv[1]           # player name from form
    n_disks = int(sys.argv[2])       # number of disks from form
else:
    # fallback if running manually
    username = input("Enter your name: ") or "Guest"
    
    while True:
        try:
            n_disks = int(input("Enter number of disks (3-6): "))
            if 3 <= n_disks <= 6:
                break
            print("Please enter a number between 3 and 6.")
        except:
            print("Invalid input, enter a number.")

print(f"Starting Tower of Hanoi for {username} with {n_disks} disks")

# -----------------------------
# Audio Setup
# -----------------------------
engine = pyttsx3.init()
engine.say("Enjoy Tower of Hanoi Game!!!")
engine.runAndWait()

# =============================
# Helper Functions
# =============================

# -----------------------------
# Function: blit_text
# Purpose: Draw text on screen at midtop position
# -----------------------------
def blit_text(screen, text, midtop, aa=True, font=None, font_name = None, size = None, color=(255,0,0)):
    """
    Draws text on the pygame screen.
    
    Parameters:
    screen : pygame.Surface
        Surface to draw text
    text : str
        Text string to display
    midtop : tuple
        (x, y) coordinate for midtop
    aa : bool
        Anti-aliasing
    font : pygame.font.Font
        Preloaded font
    font_name : str
        Font family name
    size : int
        Font size
    color : tuple
        RGB color
    """
    if font is None:
        font = pygame.font.SysFont(font_name, size)
    font_surface = font.render(text, aa, color)
    font_rect = font_surface.get_rect()
    font_rect.midtop = midtop
    screen.blit(font_surface, font_rect)

# -----------------------------
# Function: menu_screen
# Purpose: Display initial menu and select number of disks
# -----------------------------
def menu_screen():
    """
    Menu screen loop to select difficulty and display title.
    Arrow keys adjust difficulty (number of disks).
    Press ENTER to start.
    Press Q to quit.
    """
    global screen, n_disks, game_done
    menu_done = False
    while not menu_done:
        screen.fill(WHITE)
        
        # Draw Title Shadow
        blit_text(screen, 'Towers of Hanoi', (323,122), font_name='sans serif', size=90, color=GREY)
        blit_text(screen, 'Towers of Hanoi', (320,120), font_name='sans serif', size=90, color=GOLD)
        
        # Instruction
        blit_text(screen, 'Use arrow keys to select difficulty:', (320, 220), font_name='sans serif', size=30, color=BLACK)
        blit_text(screen, str(n_disks), (320, 260), font_name='sans serif', size=40, color=BLUE)
        blit_text(screen, 'Press ENTER to continue', (320, 320), font_name='sans serif', size=30, color=BLACK)
        
        # Event handling for menu
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    menu_done = True
                    game_done = True
                    print("Menu: Quit pressed")
                if event.key == pygame.K_RETURN:
                    menu_done = True
                    print("Menu: Enter pressed")
                if event.key in [pygame.K_RIGHT, pygame.K_UP]:
                    n_disks += 1
                    if n_disks > 6:
                        n_disks = 6
                    print(f"Menu: Increased disks to {n_disks}")
                if event.key in [pygame.K_LEFT, pygame.K_DOWN]:
                    n_disks -= 1
                    if n_disks < 1:
                        n_disks = 1
                    print(f"Menu: Decreased disks to {n_disks}")
            if event.type == pygame.QUIT:
                menu_done = True
                game_done = True
                print("Menu: Quit via window close")
        pygame.display.flip()
        clock.tick(60)

# -----------------------------
# Function: make_disks
# Purpose: Initialize disk objects with size, value, position
# -----------------------------
def make_disks():
    global n_disks, disks
    disks = []
    height = 20
    ypos = 397 - height
    width = n_disks * 23
    for i in range(n_disks):
        disk = {}
        disk['rect'] = pygame.Rect(0, 0, width, height)
        disk['rect'].midtop = (120, ypos)
        disk['val'] = n_disks-i
        disk['tower'] = 0
        disks.append(disk)
        ypos -= height+3
        width -= 23
        # Debug log
        print(f"Disk {i} created with width {disk['rect'].width} at position {disk['rect'].midtop}")

# -----------------------------
# Function: draw_disks
# Purpose: Draw all disks on screen
# -----------------------------
def draw_disks():
    for disk in disks:
        pygame.draw.rect(screen, BLUE, disk['rect'])

# -----------------------------
# Function: draw_towers
# Purpose: Draw towers and base
# -----------------------------
def draw_towers():
    for xpos in range(40, 460+1, 200):
        pygame.draw.rect(screen, GREEN, pygame.Rect(xpos, 400, 160 , 20))
        pygame.draw.rect(screen, GREY, pygame.Rect(xpos+75, 200, 10, 200))
    blit_text(screen, 'Start', (towers_midx[0], 403), font_name='mono', size=14, color=BLACK)
    blit_text(screen, 'Finish', (towers_midx[2], 403), font_name='mono', size=14, color=BLACK)

# -----------------------------
# Function: draw_ptr
# Purpose: Draw the pointer triangle on selected tower
# -----------------------------
def draw_ptr():
    ptr_points = [
        (towers_midx[pointing_at]-7 ,440), 
        (towers_midx[pointing_at]+7, 440), 
        (towers_midx[pointing_at], 433)
    ]
    pygame.draw.polygon(screen, RED, ptr_points)

# -----------------------------
# Function: check_won
# Purpose: Check if all disks are at last tower
# -----------------------------
def check_won():
    over = all(disk['tower']==2 for disk in disks)
    if over:
        print("All disks at finish tower! Game over.")
        time.sleep(0.2)
        game_over()

# -----------------------------
# Function: game_over
# Purpose: Display game over screen with steps and Play Again button
# -----------------------------
def game_over():
    global steps
    screen.fill(WHITE)
    min_steps = 2**n_disks-1
    # Title shadow
    blit_text(screen, 'You Won!', (322, 202), font_name='sans serif', size=72, color=GOLD)
    blit_text(screen, 'You Won!', (320, 200), font_name='sans serif', size=72, color=GOLD)
    # Steps info
    blit_text(screen, 'Your Steps: '+str(steps), (320, 360), font_name='mono', size=30, color=BLACK)
    blit_text(screen, 'Minimum Steps: '+str(min_steps), (320, 390), font_name='mono', size=30, color=RED)
    if min_steps==steps:
        blit_text(screen, 'You finished in minimum steps!', (320, 300), font_name='mono', size=26, color=GREEN)
    pygame.display.flip()
    print(f"Game Over! Steps taken: {steps}, Minimum: {min_steps}")
    time.sleep(2)
    
    # Open Flask game_over page
    try:
        webbrowser.open(f"http://127.0.0.1:5000/game_over?username={username}&disks={n_disks}&moves={steps}")
        print("Opened Play Again page in browser")
    except:
        print("Could not open browser page. Make sure Flask server is running.")
    
    pygame.quit()
    sys.exit()

# -----------------------------
# Function: reset
# Purpose: Reset game variables and go to menu
# -----------------------------
def reset():
    global steps, pointing_at, floating, floater
    steps = 0
    pointing_at = 0
    floating = False
    floater = 0
    menu_screen()
    make_disks()
    print("Game reset to menu")

# -----------------------------
# Function: handle_key_up
# Purpose: Pick up top disk from current tower
# -----------------------------
def handle_key_up():
    global floating, floater
    for disk in disks[::-1]:
        if disk['tower'] == pointing_at:
            floating = True
            floater = disks.index(disk)
            disk['rect'].midtop = (towers_midx[pointing_at], 100)
            print(f"Picked up disk {floater} from tower {pointing_at}")
            break

# -----------------------------
# Function: handle_key_down
# Purpose: Place the floating disk onto target tower
# -----------------------------
def handle_key_down():
    global floating, floater, steps
    for disk in disks[::-1]:
        if disk['tower'] == pointing_at and disks.index(disk) != floater:
            if disk['val'] > disks[floater]['val']:
                floating = False
                disk_top = disk['rect'].top
                disks[floater]['rect'].midtop = (towers_midx[pointing_at], disk_top-23)
                disks[floater]['tower'] = pointing_at
                steps += 1
                print(f"Placed disk {floater} on tower {pointing_at} on top of disk {disks.index(disk)}")
            break
    else:
        floating = False
        disks[floater]['rect'].midtop = (towers_midx[pointing_at], 400-23)
        disks[floater]['tower'] = pointing_at
        steps += 1
        print(f"Placed disk {floater} on empty tower {pointing_at}")

# =============================
# Start Game
# =============================

# Only show menu if NOT started via Flask
if len(sys.argv) < 3:
    menu_screen()

make_disks()

# =============================
# Main Game Loop
# =============================
while not game_done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_done = True
            print("Quit via window close")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                reset()
            if event.key == pygame.K_q:
                game_done = True
                print("Quit via Q key")
            if event.key == pygame.K_RIGHT:
                pointing_at = (pointing_at+1)%3
                if floating:
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at
                    print(f"Moved floating disk {floater} to tower {pointing_at}")
            if event.key == pygame.K_LEFT:
                pointing_at = (pointing_at-1)%3
                if floating:
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at
                    print(f"Moved floating disk {floater} to tower {pointing_at}")
            if event.key == pygame.K_UP and not floating:
                handle_key_up()
            if event.key == pygame.K_DOWN and floating:
                handle_key_down()
    
    # -----------------------------
    # Draw Everything
    # -----------------------------
    screen.fill(WHITE)
    draw_towers()
    draw_disks()
    draw_ptr()
    blit_text(screen, 'Steps: '+str(steps), (320, 20), font_name='mono', size=30, color=BLACK)
    
    # Check win condition if no disk floating
    if not floating:
        check_won()
    
    pygame.display.flip()
    clock.tick(framerate)

# ===============================================
# END OF GAME CODE
# ===============================================
