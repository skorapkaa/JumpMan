import sys
import pygame

from button import Button
from player import Player
from terrain import Terrain

pygame.init()

def get_font(size):
    return pygame.font.Font("assets/fonts/chrustyrock.ttf", size)

class MainGame:
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Jumper")
        self.clock = pygame.time.Clock()

        self.menu_birds_sfx = pygame.mixer.Sound("assets/sounds/birds.wav")
        self.menu_pop_btn_sfx = pygame.mixer.Sound("assets/sounds/pop.wav")
        self.menu_pop_btn_sfx.set_volume(0.2)

        self.menu_background = pygame.transform.scale(
            pygame.image.load("assets/sprites/menu_sprites/background_menu.png").convert(),
            (800, 600)
        )

    def play(self, difficulty="medium"):
        screen_run = True
        paused = False
        player = Player()
        terrain = Terrain()
        terrain_data = terrain.get_map(difficulty)
        score = 0

        ground_rects = terrain_data["ground_rects"]
        platform_rects = terrain_data["platform_rects"]
        item_rects = terrain_data["items"]
        boost_rects = terrain_data["boosts"]

        background = pygame.image.load("assets/sprites/game_sprites/background.png").convert()
        background_width = background.get_width()

        ground_texture = pygame.image.load("assets/sprites/game_sprites/ground.png").convert_alpha()
        ground_texture = pygame.transform.scale(ground_texture, (64, 64))

        platform_texture_original = pygame.image.load("assets/sprites/game_sprites/platform.png").convert_alpha()

        item_texture = pygame.image.load("assets/sprites/game_sprites/item.png").convert_alpha()
        item_texture = pygame.transform.scale(item_texture, (32,32))

        boost_texture = pygame.image.load("assets/sprites/game_sprites/boost.png").convert_alpha()
        boost_texture = pygame.transform.scale(boost_texture, (32,32))

        self.menu_birds_sfx.stop()
        self.menu_birds_sfx.play(loops=-1)

        RETURN_BUTTON = Button(
            image=pygame.image.load("assets/sprites/menu_sprites/Options Rect.png"),
            pos=(400, 300),
            text_input="RETURN TO MENU",
            font=get_font(40),
            base_color="#1C86E5",
            hovering_color="White"
        )

        scroll_x = 0

        while screen_run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    paused = not paused
                if paused and event.type == pygame.MOUSEBUTTONDOWN:
                    if RETURN_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        self.menu_pop_btn_sfx.play()
                        return  # návrat do menu

            if not paused:
                player.handle_input(offset_x=scroll_x, screen_width=self.WIDTH)
                player.update(ground_rects + platform_rects)

            if not player.alive:
                print("propast")
                pygame.time.wait(500)
                player = Player()
                terrain = Terrain()
                terrain_data = terrain.get_map(difficulty)
                ground_rects = terrain_data["ground_rects"]
                platform_rects = terrain_data["platform_rects"]
                item_rects = terrain_data["items"]
                boost_rects = terrain_data["boosts"]
                score = 0

            scroll_x = max(0, min(player.x - self.WIDTH // 2, background_width - self.WIDTH))
            self.SCREEN.blit(background, (-scroll_x, 0))

            # Vykreslení země
            for rect in ground_rects:
                tiles_x = rect.width // ground_texture.get_width() + 1
                tiles_y = rect.height // ground_texture.get_height() + 1
                for x in range(tiles_x):
                    for y in range(tiles_y):
                        pos_x = rect.x + x * ground_texture.get_width() - scroll_x
                        pos_y = rect.y + y * ground_texture.get_height()
                        self.SCREEN.blit(ground_texture, (pos_x, pos_y))

            # Vykreslení platforem
            for rect in platform_rects:
                platform_texture = pygame.transform.scale(platform_texture_original, (rect.width, rect.height))
                self.SCREEN.blit(platform_texture, (rect.x - scroll_x, rect.y))

            # Vykreslení mincí a podminka pro jejich sebrani
            for coin in item_rects[:]:
                if player.get_rect().colliderect(coin):
                    item_rects.remove(coin)
                    score += 1
                else:
                    self.SCREEN.blit(item_texture, (coin.x - scroll_x, coin.y))

            # Vykresleni boostu
            for boost in boost_rects:
                if player.get_rect().colliderect(boost):
                    boost_rects.remove(boost)    
                    player.jump_boost_end_time = pygame.time.get_ticks() + 5000  # boost na 5 sekund
                else:
                    self.SCREEN.blit(boost_texture, (boost.x - scroll_x, boost.y))    

            # Vykreslení hráče
            player.draw(self.SCREEN, scroll_x)

            #Vykresleni skore. MIZI OPRAVIT !
            score_text = get_font(30).render(f"Score: {score}", True, "#FFFFFF")
            self.SCREEN.blit(score_text, (30, 30))

            # Vykresleni casu pro boost
            current_time = pygame.time.get_ticks()
            if player.jump_boost_end_time > current_time:
                remaining_ms = player.jump_boost_end_time - current_time
                remaining_seconds = round(remaining_ms / 1000, 1)
                boost_text = get_font(30).render(f"Boost: {remaining_seconds}s", True, "#FFD700")
                self.SCREEN.blit(boost_text, (30, 70))


            # Pauza
            if paused:
                pause_text = get_font(80).render("PAUSED", True, "#FF0000")
                pause_rect = pause_text.get_rect(center=(self.WIDTH // 2, 150))
                self.SCREEN.blit(pause_text, pause_rect)

                RETURN_BUTTON.changeColor(pygame.mouse.get_pos())
                RETURN_BUTTON.update(self.SCREEN)

            pygame.display.update()
            self.clock.tick(60)

    def options(self):
        screen_run = True
        BACK_BUTTON = Button(
            image=pygame.image.load("assets/sprites/menu_sprites/Play Rect.png"),
            pos=(400, 250),
            text_input="BACK",
            font=get_font(60),
            base_color="#1C86E5",
            hovering_color="White"
        )

        while screen_run:
            MOUSE_POS = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON.checkForInput(MOUSE_POS):
                        self.menu_pop_btn_sfx.play()
                        return

            self.SCREEN.fill((0, 0, 255))
            BACK_BUTTON.changeColor(MOUSE_POS)
            BACK_BUTTON.update(self.SCREEN)

            pygame.display.update()
            self.clock.tick(60)

    def menu(self):
        if not pygame.mixer.get_busy():
            self.menu_birds_sfx.play(loops=-1)

        while True:
            self.SCREEN.blit(self.menu_background, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = get_font(100).render("MAIN MENU", True, "#04049B")
            MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))
            self.SCREEN.blit(MENU_TEXT, MENU_RECT)

            PLAY_BUTTON = Button(
                image=pygame.image.load("assets/sprites/menu_sprites/Play Rect.png"),
                pos=(400, 250),
                text_input="PLAY",
                font=get_font(60),
                base_color="#1C86E5",
                hovering_color="White"
            )
            OPTIONS_BUTTON = Button(
                image=pygame.image.load("assets/sprites/menu_sprites/Options Rect.png"),
                pos=(400, 400),
                text_input="OPTIONS",
                font=get_font(50),
                base_color="#1C86E5",
                hovering_color="White"
            )
            QUIT_BUTTON = Button(
                image=pygame.image.load("assets/sprites/menu_sprites/Quit Rect.png"),
                pos=(400, 550),
                text_input="QUIT",
                font=get_font(50),
                base_color="#1C86E5",
                hovering_color="White"
            )

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.menu_pop_btn_sfx.play()
                        self.menu_birds_sfx.stop()
                        self.play()
                        self.menu_birds_sfx.play(loops=-1)
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.menu_pop_btn_sfx.play()
                        self.options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
            self.clock.tick(60)
