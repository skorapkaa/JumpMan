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
        self.facing_right = True

        self.frame_index = 0
        self.animation_speed = 0.03

        # Sprity - chodící animace pouze pro pravou stranu
        self.walk_right_frames = [
            pygame.transform.scale(pygame.image.load("assets/sprites/character_sprites/walk_right1.png"), (60, 60)),
            pygame.transform.scale(pygame.image.load("assets/sprites/character_sprites/walk_right2.png"), (60, 60)),
        ]

        # Idle animace - dva snímky pro pohupování, jen pro pravou stranu
        self.idle_right_frames = [
            pygame.transform.scale(pygame.image.load("assets/sprites/character_sprites/stand_right.png"), (40, 60)),
            pygame.transform.scale(pygame.image.load("assets/sprites/character_sprites/stand_right2.png"), (40, 60))
        ]

        self.image = self.idle_right_frames[0]

        self.idle_frame_index = 0
        self.idle_animation_speed = 0.02  # rychlost animace stání
        self.idle_animation_timer = 0

    def draw(self, screen, offset_x=0):
        # Pokud postava čelí doleva, otočíme obrázek horizontálně
        if self.facing_right:
            screen.blit(self.image, (self.x - offset_x, self.y))
        else:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, (self.x - offset_x, self.y))

    def get_rect(self):
        # Většina snímků má velikost 40x60
        return pygame.Rect(self.x, self.y, 40, 60)

    def update(self, terrain):
        self.on_ground = False
        self.x += self.velocity_x
        player_rect = self.get_rect()

        # Kolize na osu X
        for rect in terrain:
            if player_rect.colliderect(rect):
                if self.velocity_x > 0:
                    self.x = rect.left - player_rect.width
                elif self.velocity_x < 0:
                    self.x = rect.right
                self.velocity_x = 0
                player_rect = self.get_rect()

        # Gravitační efekt a pohyb na ose Y
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        player_rect = self.get_rect()
        prev_bottom = player_rect.bottom - self.velocity_y

        # Kolize na osu Y (vylepšená detekce "on_ground" na hraně)
        ground_check_rect = player_rect.inflate(8, 0)  # rozšíříme kolizní obdélník o 8px do stran
        for rect in terrain:
            if player_rect.colliderect(rect):
                if prev_bottom <= rect.top + 10:
                    self.y = rect.top - player_rect.height
                    self.velocity_y = 0
                    self.on_ground = True
                elif player_rect.top < rect.bottom and self.velocity_y < 0:
                    self.y = rect.bottom
                    self.velocity_y = 0

        # Pokud spadne pod obrazovku, zemře
        if self.y > 700:
            self.alive = False

        # Aktualizace animace
        self.update_animation()

    def move(self, direction, screen_width=800, offset_x=0):
        max_x_on_screen = offset_x + screen_width - 40
        if direction == "left" and self.x > 0:
            self.velocity_x = -self.speed
            self.facing_right = False
        elif direction == "right":
            if self.x + self.speed < max_x_on_screen:
                self.velocity_x = self.speed
                self.facing_right = True
        else:
            self.velocity_x = 0

    def update_animation(self):
        if self.velocity_x > 0:
            # Chůze doprava
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.walk_right_frames):
                self.frame_index = 0
            self.image = self.walk_right_frames[int(self.frame_index)]
            self.idle_frame_index = 0
            self.idle_animation_timer = 0

        elif self.velocity_x < 0:
            # Chůze doleva (stejné snímky jako doprava, jen se při vykreslení otočí)
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.walk_right_frames):
                self.frame_index = 0
            self.image = self.walk_right_frames[int(self.frame_index)]
            self.idle_frame_index = 0
            self.idle_animation_timer = 0

        else:
            # Stání - animace pohupování mezi dvěma snímky
            self.idle_animation_timer += self.idle_animation_speed
            if self.idle_animation_timer >= 1:
                self.idle_animation_timer = 0
                self.idle_frame_index = (self.idle_frame_index + 1) % len(self.idle_right_frames)
            self.image = self.idle_right_frames[self.idle_frame_index]
