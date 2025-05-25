import pygame

from character import Character


class Player(Character):
    def __init__(self):
        super().__init__()
        self.jump_boost_end_time = 0
        self.velocity_y = 0.0
        self.on_ground = True

    def handle_input(self, background_width=2400) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move("left", background_width)
        elif keys[pygame.K_RIGHT]:
            self.move("right", background_width)
        else:
            self.move("stop")

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.jump()

    def jump(self) -> None:
        current_time = pygame.time.get_ticks()
        if self.on_ground:
            if current_time < self.jump_boost_end_time:
                self.velocity_y = -18
            else:
                self.velocity_y = -10
            self.on_ground = False

    def check_collisions(self, items) -> None:
        # remove check collisions with terrain that is not implemented in this class thus fixing a bug
        # where player would fall of the edge of the terrain
        for item in items:
            if self.get_rect().colliderect(item.itemBounds):
                item.collectItem()
