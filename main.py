import pygame
from smile_detector import detect_smile

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.running = True
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("The Way Home Game")
        self.background = pygame.image.load("pygame_art\\background.png") #menu background i made in 5m why space?: idk
        self.background = pygame.transform.scale(self.background, (800, 600))

        self.game_backgeound = pygame.image.load("pygame_art\\simple_background.png")
        self.game_background = pygame.transform.scale(self.game_backgeound, (800, 600))

        self.button_color = (255, 0, 0) 
        self.button_rect = pygame.Rect(225, 290, 370, 80)  

        self.state = "menu"

        self.health = 0
        self.speed = 5

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
            self.draw_health(self.screen)
        #TODO:
            # make main game background platforms exit(or something like that) and obsticoles(use the smile detector in each one of them)
            # combie the health bar and character into one file and make it work with the game
            #make player animation(items maybe?)
            # make unique lvls(maybe 3-5) with different obsticoles
            #make the smile alert pop up then needed(slow the game while that happens to give the player time to smile)
            #add error logic to the smile detector in case theres is no cemra detected #done
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
