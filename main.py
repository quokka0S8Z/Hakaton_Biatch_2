import pygame
import random
from smile_detector import detect_smile
WIDTH, HEIGHT = 800, 600
OBSTACLE_SPACING = 400
SPEED = 5
OBSTACLE_WIDTH = 100
OBSTACLE_HEIGHT = 100
OBSTACLE_PASSED = 0
GRAVITY = 0.48
JUMP_STRENGTH = -9
class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.running = True
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("The Way Home Game")
        self.background = pygame.image.load("pygame_art\\background.png") #menu background i made in 5m why space?: idk
        self.background = pygame.transform.scale(self.background, (800, 600))
        self.player = pygame.image.load("pygame_art/wounded_soldier.png").convert_alpha()
        self.game_background = pygame.image.load("pygame_art\\simple_background.png")
        self.game_background = pygame.transform.scale(self.game_background, (800, 600))

        self.button_color = (255, 0, 0) 
        self.button_rect = pygame.Rect(225, 290, 370, 80)  

        self.state = "menu"
        self.health = 0
        self.speed = 5
        self.player = pygame.image.load("pygame_art/wounded_soldier.png").convert_alpha()
        self.player = pygame.transform.scale(self.player, (70, 90))
        self.player_rect = self.player.get_rect()
        self.player_rect.x = 20
        self.player_rect.y = HEIGHT - 201
        self.player_y_velocity = 0
        self.is_jumping = False
        self.obstacle_image = pygame.image.load("pygame_art\\Obstacle.png").convert_alpha()
        self.obstacle_image = pygame.transform.scale(self.obstacle_image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

        self.obstacles = []
        self.obstacle_counter = 2

        if self.player_rect.x < WIDTH:
            for i in range(self.obstacle_counter):
                x = 250 + i * OBSTACLE_SPACING
                y = 505 - OBSTACLE_HEIGHT
                self.obstacles.append(pygame.Rect(x, y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

        self.create_obstacles()

    def create_obstacles(self):
        self.obstacles = []
        for i in range(self.obstacle_counter):
            x = random.randint(200, 300) + i * OBSTACLE_SPACING
            y = 505 - OBSTACLE_HEIGHT
            self.obstacles.append(pygame.Rect(x, y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F5:
                    self.running = False
                elif event.key == pygame.K_p:
                    pygame.display.toggle_fullscreen()#toggle fullscreen mode by pressing p

            elif event.type == pygame.MOUSEBUTTONDOWN and self.state == "menu":
                if self.button_rect.collidepoint(pygame.mouse.get_pos()):
                    print("Start button clicked!")#log
                    self.state = "game"

    def update(self):
        if self.state == "menu":
            self.screen.blit(self.background, (0, 0))
            #pygame.draw.rect(self.screen, self.button_color, self.button_rect)
        elif self.state == "game":
            self.screen.blit(self.game_background, (0, 0))# change backgound to game background
            self.display_health(self.screen)
            for obstacle in self.obstacles:
                self.screen.blit(self.obstacle_image, obstacle)

            self.player_rect.x += self.speed

            if self.player_rect.x > WIDTH:
                self.create_obstacles()
                self.player_rect.x = 20

            if not self.is_jumping and detect_smile():
                self.player_y_velocity = JUMP_STRENGTH
            self.is_jumping = True

            self.player_rect.y += self.player_y_velocity
            self.player_y_velocity += GRAVITY

            if self.player_rect.y >= HEIGHT - 201:
                self.player_rect.y = HEIGHT - 201
                self.player_y_velocity = 0
                self.is_jumping = False

            self.screen.blit(self.player, self.player_rect)
        #TODO:
            # make main game background platforms exit(or something like that) and obsticoles(use the smile detector in each one of them)
            # combie the health bar and character into one file and make it work with the game
            #make player animation(items maybe?)
            # make unique lvls(maybe 3-5) wit \h different obsticoles
            #make the smile alert pop up then needed(slow the game while that happens to give the player time to smile)
            #add error logic to the smile detector in case theres is no cemra detected #done

    def display_health(self, screen):
        font = pygame.font.SysFont("Arial", 30)  # גופן בגודל 30
        text = font.render(f"Health: {self.health}", True, (255, 255, 255))
        screen.blit(text, (20, 20))
                
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            pygame.display.flip()

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()
