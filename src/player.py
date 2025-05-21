from character import Character
import pygame

class Player(Character):
    def __init__(self):
        super().__init__()
        self.jump_boost_end_time = 0

    def handle_input(self, offset_x=0, screen_width=800, background_width=2400):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move("left", screen_width, offset_x, background_width)
        elif keys[pygame.K_RIGHT]:
            self.move("right", screen_width, offset_x, background_width)
        else:
            self.velocity_x = 0

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.jump()

    def jump(self):
        current_time = pygame.time.get_ticks()
        if self.on_ground:
            if current_time < self.jump_boost_end_time:
                self.velocity_y = -18
            else:
                self.velocity_y = -10
            self.on_ground = False

    def check_collisions(self, items, terrain):
        self.check_collision(terrain)
        for item in items:
            if self.get_rect().colliderect(item.itemBounds):
                item.collectItem()
