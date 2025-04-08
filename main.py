import pygame
from smile_detector import detect_smile
WIDTH, HEIGHT = 800, 600
OBSTACLE_SPACING = 400
SPEED = 5
OBSTACLE_WIDTH = 100
OBSTACLE_HEIGHT = 100
OBSTACLE_PASSED = 0
GRAVITY = 1
JUMP_STRENGTH = -15
class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.running = True
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("The Way Home Game")
        self.background = pygame.image.load("pygame_art\\background.png") #menu background I made in 5m why space?
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
        self.player = pygame.transform.scale(self.player, (70, 70))
        self.player_rect = self.player.get_rect()
        self.player_rect.x = 20
        self.player_rect.y = HEIGHT - 183
        self.player_y_velocity = 0
        self.is_jumping = False
        self.obstacle_image = pygame.image.load("pygame_art\\Obstacle.png").convert_alpha()
        self.obstacle_image = pygame.transform.scale(self.obstacle_image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

        self.obstacles = []
        self.obstacle_counter = 10000

        if self.health == 90:
            self.obstacle_counter = 2

        for i in range(self.obstacle_counter):
            x = 300 + i * OBSTACLE_SPACING
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
            self.screen.blit(self.game_background, (0, 0))# change background to game background
            self.draw_health(self.screen)
            for obstacle in self.obstacles:
                self.screen.blit(self.obstacle_image, obstacle)

            self.player_rect.x += self.speed
            if self.player_rect.x > WIDTH:
                self.player_rect.x = 100

            if not self.is_jumping and detect_smile():
                self.player_y_velocity = JUMP_STRENGTH
                self.is_jumping = True

            self.player_rect.y += self.player_y_velocity
            self.player_y_velocity += GRAVITY

            if self.player_rect.y >= HEIGHT - 60:
                self.player_rect.y = HEIGHT - 60
                self.player_y_velocity = 0
                self.is_jumping = False

            self.screen.blit(self.player, self.player_rect)
        #TODO:
            # make main game background platforms exit(or something like that) and obstacles(use the smile detector in each one of them)
            # combine the health bar and character into one file and make it work with the game
            #make player animation(items maybe?)
            # make unique levels(maybe 3-5) with different obstacles
            #make the smile alert pop up then needed(slow the game while that happens to give the player time to smile)
            #add error logic to the smile detector in case theres is no camera detected #done
    def draw_health(self, screen):
                pygame.draw.rect(screen, (255, 0, 0), (20, 20, 200, 20))
                pygame.draw.rect(screen, (0, 255, 0), (20, 20, 2 * self.health, 20))
                #ammmm... well the health bar does something i guess
                #yea im not fixing this shit
                
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            pygame.display.flip()

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()
