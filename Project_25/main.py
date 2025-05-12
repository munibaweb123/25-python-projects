import pygame
import random
import math

# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background

# Title and Icon
pygame.display.set_caption("Space Invaders")
try:
    icon = pygame.image.load('spaceship.png')  # Load your icon image
    pygame.display.set_icon(icon)
except pygame.error as e:
    print(f"Error loading icon image: {e}")

# Player
try:
    playerImg = pygame.image.load('space-invaders.png')  # Load your player image
    enemyImg = pygame.image.load('enemy.png')  # Load your enemy image
except pygame.error as e:
    print(f"Error loading player image: {e}")
    playerImg = None


    

playerX = 370
playerY = 480
enemyX = random.randint(0, 735)
enemyY = random.randint(50, 150)
enemyX_change = 1  # Initialize enemyX_change
enemyY_change = 40  # Initialize enemyY_change
playerX_change = 0  # Initialize playerX_change
bullet_state = "ready"  # Ready state means you can't see the bullet on the screen
bulletX = 0
bulletY = playerY  # Initialize bulletY with the player's Y position

bullet_change = 10  # Speed of bullet

def player(x,y):
    if playerImg:
        screen.blit(playerImg, (x, y))

def enemy(x,y):
    if enemyImg:
        screen.blit(enemyImg, (x, y))

try:
    bulletImg = pygame.image.load('bullet.png')  # Load your bullet image once
except pygame.error as e:
    print(f"Error loading bullet image: {e}")
    bulletImg = None

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    if bulletImg:
        screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow( enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))  
    if distance < 27:
        return True
    else:
        return False

# infinite loop
running = True
while running:
    # Fill the screen with black
    screen.fill((0, 0, 0))
# Background image
    try:
        background = pygame.image.load('background.jpg')  # Load your background image
        screen.blit(background, (0, 0))
    except pygame.error as e:
        print(f"Error loading background image: {e}")
    # playerX -= 0.1
    # playerY -= 0.1

    # if keystroke is pressed check whether left or right
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # key down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # key up
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0



    playerX += playerX_change

    # Boundary checking for spaceship
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    enemyX += enemyX_change

    # movement of enemy
    if enemyX <= 0:
        enemyX_change = 1
        enemyY += enemyY_change

    elif enemyX >= 736:
        enemyX_change = -1
        enemyY += enemyY_change


    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bullet_change

    # Collision
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = 480
        bullet_state = "ready"
        enemyX = random.randint(0, 735)
        enemyY = random.randint(50, 150)
        print("Collision detected!")
    
    # Call the player function to draw the player
    player(playerX, playerY)
    # Call the enemy function to draw the enemy
    enemy(enemyX, enemyY)

    # Update the display
    pygame.display.update()