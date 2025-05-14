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

        self.character_stand_right = pygame.image.load("assets/sprites/character_sprites/stand_sprite_right.png")
        self.character_stand_right = pygame.transform.scale(self.character_stand_right, (40, 60))

        self.character_stand_left = pygame.image.load("assets/sprites/character_sprites/stand_sprite_left.png")
        self.character_stand_left = pygame.transform.scale(self.character_stand_left, (40, 60))

    def draw(self, screen):
        if self.facing_direction == "right":
            screen.blit(self.character_stand_right, (self.x, self.y))
        else:
            screen.blit(self.character_stand_left, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 40, 60)

    def update(self, terrain):
        self.on_ground = False
        self.x += self.velocity_x
        player_rect = self.get_rect()
        
        for rect in terrain:
            if player_rect.colliderect(rect):
                if self.velocity_x > 0:
                    self.x = rect.left - player_rect.width
                elif self.velocity_x < 0:
                    self.x = rect.right
                self.velocity_x = 0
                player_rect = self.get_rect()

        self.velocity_y += self.gravity
        self.y += self.velocity_y
        player_rect = self.get_rect()

        for rect in terrain:
            if player_rect.colliderect(rect):
                if self.velocity_y > 0:
                    self.y = rect.top - player_rect.height
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.y = rect.bottom
                    self.velocity_y = 0
                    
        if self.y > 700:
            self.alive = False
        
              


    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
            self.facing_direction = "left"
        elif direction == "right" and self.x < 760:
            self.x += self.speed
            self.facing_direction = "right"

    def jump(self):
        if self.on_ground:
            self.velocity_y = -10
            self.on_ground = False


