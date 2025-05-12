import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
mixer.music.load('background.wav')  # Load your background music
mixer.music.play(-1)  # Play the music indefinitely

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
    enemyImg.append(pygame.image.load('enemy.png'))  # Load your enemy image
except pygame.error as e:
    print(f"Error loading player image: {e}")
    playerImg = None


    

playerX = 370
playerY = 480

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))  # Load enemy image
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)  # Initialize enemyX_change
    enemyY_change.append(40)  # Initialize enemyY_change
playerX_change = 0  # Initialize playerX_change
bullet_state = "ready"  # Ready state means you can't see the bullet on the screen
bulletX = 0
bulletY = playerY  # Initialize bulletY with the player's Y position

bullet_change = 10  # Speed of bullet
score_value = 0
font = pygame.font.Font('DejaVuMathTeXGyre.ttf', 32)
textX = 10
textY = 10

# Game Over text
def game_over_text():
    over_font = pygame.font.Font('DejaVuMathTeXGyre.ttf', 64)
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x,y):
    if playerImg:
        screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    if enemyImg[i]:
        screen.blit(enemyImg[i], (x, y))

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
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')  # Load your bullet sound
                    bullet_sound.play()  # Play the sound
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

    # Remove this line as it is redundant and incorrect

    # movement of enemy
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

            # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()  # Play the explosion sound
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            print("Collision detected!")


    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bullet_change


    
    # Call the player function to draw the player
    player(playerX, playerY)
    # Call the show_score function to display the score
    show_score(textX, textY)
    # Call the enemy function to draw the enemy
    for i in range(num_of_enemies):
        enemy(enemyX[i], enemyY[i], i)

    # Update the display
    pygame.display.update()