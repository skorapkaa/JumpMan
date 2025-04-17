import pygame


class Character:
    def __init__(self):
        self.alive = True
        self.x, self.y = 100, 400
        self.speed = 5
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 0.5
        self.on_ground = False
        self.facing_direction = "right"

        self.character_stand_right = pygame.image.load("../assets/sprites/character_sprites/stand_sprite_right.png")
        self.character_stand_right = pygame.transform.scale(self.character_stand_right, (40, 60))

        self.character_stand_left = pygame.image.load("../assets/sprites/character_sprites/stand_sprite_left.png")
        self.character_stand_left = pygame.transform.scale(self.character_stand_left, (40, 60))

    def draw(self, screen):
        if self.facing_direction == "right":
            screen.blit(self.character_stand_right, (self.x, self.y))
        else:
            screen.blit(self.character_stand_left, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 40, 60)

    def update(self):
        self.velocity_y += self.gravity
        self.y += self.velocity_y

        # postava neopustí obrazovku
        self.x = max(0, min(self.x, 800 - 40))

    def move(self, direction):
        if direction == "left":
            self.x -= self.speed
            self.facing_direction = "left"
        elif direction == "right":
            self.x += self.speed
            self.facing_direction = "right"

    def jump(self):
        if self.on_ground:
            self.velocity_y = -10
            self.on_ground = False

    def check_collision(self, terrain):
        self.on_ground = False
        for rect in terrain:
            if pygame.Rect(self.x, self.y + 60, 40, 1).colliderect(rect):
                self.on_ground = True
                self.velocity_y = 0
                self.y = rect.top - 60
