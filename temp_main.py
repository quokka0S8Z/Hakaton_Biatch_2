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
        self.background = pygame.image.load("pygame_art\\background.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (800, 600))
        self.game_background = pygame.image.load("pygame_art\\simple_background.png").convert_alpha()
        self.game_background = pygame.transform.scale(self.game_background, (800, 600))

        # Load sprite sheets with transparency
        self.run_sprite_sheet = pygame.image.load("pygame_art\\mefune-Sheet.jpg").convert_alpha()
        self.jump_sprite_sheet = pygame.image.load("pygame_art\\jump_prob.png").convert_alpha()
        
        # Extract frames from sprite sheets
        self.run_frames = self.extract_frames(self.run_sprite_sheet, 4, (80, 64))  # 4 frames for running
        self.jump_frames = self.extract_frames(self.jump_sprite_sheet, 2, (80, 64))  # Adjust if needed
        
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 200  # Milliseconds per frame (slower animation)

        self.button_color = (255, 0, 0) 
        self.button_rect = pygame.Rect(225, 290, 370, 80)  

        self.state = "menu"
        self.health = 100
        self.speed = 5
        self.player_rect = self.run_frames[0].get_rect()
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

    def extract_frames(self, sprite_sheet, num_frames, frame_size):
        """Extract frames from a sprite sheet."""
        frames = []
        sheet_width, sheet_height = sprite_sheet.get_width(), sprite_sheet.get_height()

        # Debugging dimensions
        print(f"Sprite sheet size: {sheet_width}x{sheet_height}")
        print(f"Frame size: {frame_size}, Number of frames: {num_frames}")

        for i in range(num_frames):
            # Ensure the rectangle is within the sprite sheet bounds
            if i * frame_size[0] + frame_size[0] > sheet_width or frame_size[1] > sheet_height:
                raise ValueError(f"Frame {i} is outside the sprite sheet bounds. Check frame size or sprite sheet dimensions.")
        
            frame = sprite_sheet.subsurface(pygame.Rect(i * frame_size[0], 0, frame_size[0], frame_size[1]))
            frames.append(frame)
        return frames

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

    def update_animation(self):
        """Update the current animation frame based on time."""
        self.animation_timer += pygame.time.get_ticks()
        if self.animation_timer > self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(
                self.jump_frames if self.is_jumping else self.run_frames
            )

    def update(self):
        if self.state == "menu":
            self.screen.blit(self.background, (0, 0))
        elif self.state == "game":
            self.screen.blit(self.game_background, (0, 0))# change backgound to game background
            self.draw_health(self.screen)
            
            # Update player position
            self.player_rect.x += self.speed
            if self.player_rect.x > WIDTH:
                self.create_obstacles()
                self.player_rect.x = 20
            
            # Handle jumping
            if not self.is_jumping and detect_smile():
                self.player_y_velocity = JUMP_STRENGTH
                self.is_jumping = True
            
            self.player_rect.y += self.player_y_velocity
            self.player_y_velocity += GRAVITY
            
            if self.player_rect.y >= HEIGHT - 201:
                self.player_rect.y = HEIGHT - 201
                self.player_y_velocity = 0
                self.is_jumping = False
            
            # Update animation
            self.update_animation()
            
            # Draw player
            current_animation = self.jump_frames if self.is_jumping else self.run_frames
            self.screen.blit(current_animation[self.current_frame], self.player_rect)
            
            # Draw obstacles
            for obstacle in self.obstacles:
                self.screen.blit(self.obstacle_image, obstacle)
        #TODO:
            # make main game background platforms exit(or something like that) and obsticoles(use the smile detector in each one of them)
            # combie the health bar and character into one file and make it work with the game
            #make player animation(items maybe?)
            # make unique lvls(maybe 3-5) wit \h different obsticoles
            #make the smile alert pop up then needed(slow the game while that happens to give the player time to smile)
            #add error logic to the smile detector in case theres is no cemra detected #done
    def draw_health(self, screen):
                pygame.draw.rect(screen, (255, 0, 0), (20, 20, 200, 20))
                pygame.draw.rect(screen, (0, 255, 0), (20, 20, 2 * self.health, 20))
                #ammmm... well the health bar does something i guess
                #yea im not fixing this shit
            
    def next_area(self):
        self.speed +=0.3
        self.count = 0
        if self.count  == 1 or self.count == 0:
            self.animated_background = pygame.image.load("pygame_art\\simple_background1.png")
            self.animated_background = pygame.transform.scale(self.animated_background (800, 600))
        elif self.count == 2:
            self.animated_background = pygame.image.load("pygame_art\\simple_background2.png")
            self.animated_background = pygame.transform.scale(self.animated_background (800, 600))
        elif self.count == 3:
            self.animated_background = pygame.image.load("pygame_art\\simple_background3.png")
            self.animated_background = pygame.transform.scale(self.animated_background (800, 600))

    def find_dis(self):
        closest_distance = float('inf')  # Start with a very large number
        player_center = self.player_rect.center  # Get the center of the player

        for obstacle in self.obstacles:
            obstacle_center = obstacle.center  # Use the center property of pygame.Rect
            distance = ((player_center[0] - obstacle_center[0]) ** 2 + (player_center[1] - obstacle_center[1]) ** 2) ** 0.5  # Calculate Euclidean distance
            if distance < closest_distance:
                closest_distance = distance

        # Check if the closest distance is less than 10
        if closest_distance < 50:
            self.health -= 10
            print("Took damage! Health reduced by 10.")
            print(f"Closest distance: {closest_distance}")

        return closest_distance

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            pygame.display.flip()

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()
