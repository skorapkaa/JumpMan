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

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.move("left")
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.move("right")
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.jump()
