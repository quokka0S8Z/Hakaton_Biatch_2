import pygame

class Character:
    def __init__(self, image_path):
        self.health = 0
        self.x = 100
        self.y = 550
        self.width = 50
        self.height = 50
        self.speed = 5
        self.jumping = False
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def move(self):
        if not self.jumping:
            self.x += self.speed

    def jump(self):
        self.jumping = True
        self.y -= 50

    def land(self):
        self.jumping = False
        self.y = 550

    def hit_obstacle(self):
        self.health -= 10
        if self.health < 0:
            self.health = 0

    def pass_obstacle(self):
        self.health += 5

    def check_health(self):
        return self.health

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    #most of this is not really needed or useable with pygame