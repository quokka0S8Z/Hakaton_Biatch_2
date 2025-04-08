import pygame
import cv2
from smile_detector import detect_smile, release_camera

pygame.init()

# הגדרות חלון
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smile to Jump!")

# צבעים
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# משתנים לדמות
player = pygame.Rect(100, HEIGHT - 60, 50, 50)
player_y_velocity = 0
gravity = 1
jump_strength = -15
is_jumping = False

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(30)
    screen.fill(WHITE)

    # אירועים
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # תנועה אוטומטית הצידה
    player.x += 5
    if player.right > WIDTH:
        player.left = 0  # חוזר מההתחלה

    # קפיצה אם יש חיוך
    if not is_jumping and detect_smile():
        player_y_velocity = jump_strength
        is_jumping = True

    # עדכון קפיצה וגרוויטציה
    player.y += player_y_velocity
    player_y_velocity += gravity

    # בדיקה אם חזר לקרקע
    if player.y >= HEIGHT - 60:
        player.y = HEIGHT - 60
        player_y_velocity = 0
        is_jumping = False

    # ציור הדמות
    pygame.draw.rect(screen, BLUE, player)
    pygame.display.flip()

# שחרור משאבים
release_camera()
pygame.quit()
