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

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), self.get_rect())

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 40, 60)

    def update(self):
        self.velocity_y += self.gravity
        self.y += self.velocity_y

        # Zabraň opuštění obrazovky (x)
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
