import pygame

from character import Character


class Player(Character):
    def __init__(self):
        super().__init__()

    def check_collisions(self, items, terrain):
        self.check_collision(terrain)
        for item in items:
            if self.get_rect().colliderect(item.itemBounds):
                item.collectItem()


    def handle_input(self, offset_x=0, screen_width=800):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move("left", screen_width, offset_x)
        if keys[pygame.K_RIGHT]:
            self.move("right", screen_width, offset_x)
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.jump()
