import os
import sys

import pygame

from button import Button
from items import Items
from player import Player
from terrain import Terrain

os.environ["SDL_VIDEO_CENTERED"] = (
    "1"  # toto nam umozni menit rozliseni bez pohybu okna
)

pygame.init()


def get_font(size):
    return pygame.font.Font("assets/fonts/Lana Turner.ttf", size)


class MainGame:
    def __init__(self):
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Jumper")
        self.clock = pygame.time.Clock()

        self.coin_grab = pygame.mixer.Sound("assets/sounds/coin.wav")
        self.coin_grab.set_volume(0.2)

        self.menu_birds_sfx = pygame.mixer.Sound("assets/sounds/birds.wav")
        self.menu_pop_btn_sfx = pygame.mixer.Sound("assets/sounds/pop.wav")
        self.menu_pop_btn_sfx.set_volume(0.2)

        self.menu_song = pygame.mixer.Sound("assets/music/Oceania.mp3")
        self.menu_song.set_volume(0.05)

        self.game_song = pygame.mixer.Sound("assets/music/time_for_adventure.mp3")
        self.game_song.set_volume(0.05)

        self.power_up = pygame.mixer.Sound("assets/sounds/power_up.wav")
        self.power_up.set_volume(0.2)

        self.lift_sound = pygame.mixer.Sound("assets/sounds/lift_sound.mp3")
        self.lift_sound.set_volume(0.05)

        self.menu_backgrounds = {
            (800, 600): pygame.transform.scale(
                pygame.image.load(
                    "assets/sprites/menu_sprites/background_menu_800_600.png"
                ).convert(),
                (800, 600),
            ),
            (1024, 768): pygame.transform.scale(
                pygame.image.load(
                    "assets/sprites/menu_sprites/background_menu_1024_768.png"
                ).convert(),
                (1024, 768),
            ),
            (1280, 720): pygame.transform.scale(
                pygame.image.load(
                    "assets/sprites/menu_sprites/background_menu_1280_720.png"
                ).convert(),
                (1280, 720),
            ),
        }

        self.scaled_background = self.menu_backgrounds[(self.WIDTH, self.HEIGHT)]

    def play(self, difficulty="medium"):
        screen_run = True
        paused = False
        player = Player()
        terrain = Terrain(self.WIDTH, self.HEIGHT)
        items = Items()
        terrain_data = terrain.get_map(difficulty)
        score = 0

        ground_rects = terrain_data["ground_rects"]
        platform_rects = terrain_data["platform_rects"]
        item_rects, boost_rects = items.get_items_and_boosts(
            difficulty, self.WIDTH, self.HEIGHT
        )
        lift_rects = terrain_data.get("lift", [])

        background = pygame.image.load(
            "assets/sprites/game_sprites/background.png"
        ).convert()
        background_width = background.get_width()

        ground_texture = pygame.image.load(
            "assets/sprites/game_sprites/ground.png"
        ).convert_alpha()
        ground_texture = pygame.transform.scale(ground_texture, (64, 64))

        platform_texture_original = pygame.image.load(
            "assets/sprites/game_sprites/platform.png"
        ).convert_alpha()

        item_texture = pygame.image.load(
            "assets/sprites/game_sprites/item.png"
        ).convert_alpha()
        item_texture = pygame.transform.scale(item_texture, (32, 32))

        boost_texture = pygame.image.load(
            "assets/sprites/game_sprites/boost.png"
        ).convert_alpha()
        boost_texture = pygame.transform.scale(boost_texture, (32, 32))

        lift_texture_open = pygame.image.load(
            "assets/sprites/game_sprites/lift_open.png"
        ).convert_alpha()
        lift_texture_open = pygame.transform.scale(lift_texture_open, (128, 128))
        lift_texture_closed = pygame.image.load(
            "assets/sprites/game_sprites/lift_closed.png"
        ).convert_alpha()
        lift_texture_closed = pygame.transform.scale(lift_texture_closed, (128, 128))

        self.menu_birds_sfx.stop()
        self.menu_birds_sfx.play(loops=-1)
        self.game_song.play(loops=-1)

        RETURN_BUTTON = Button(
            image=pygame.image.load("assets/sprites/menu_sprites/Options Rect.png"),
            pos=(self.WIDTH // 2, 300),
            text_input="RETURN TO MENU",
            font=get_font(40),
            base_color="#CDE3F7",
            hovering_color="White",
        )

        scroll_x = 0

        while screen_run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if (
                        event.type == pygame.KEYDOWN
                        and hasattr(event, "key") == pygame.K_ESCAPE
                ):
                    paused = not paused
                if paused and event.type == pygame.MOUSEBUTTONDOWN:
                    if RETURN_BUTTON.check_for_input(pygame.mouse.get_pos()):
                        self.menu_pop_btn_sfx.play()
                        self.menu_birds_sfx.stop()
                        self.game_song.stop()
                        return  # návrat do menu

            if not paused:
                player.handle_input()
                player.update(ground_rects + platform_rects)

            if not player.alive:
                pygame.time.wait(500)
                player = Player()
                terrain = Terrain(self.WIDTH, self.HEIGHT)
                items = Items()
                terrain_data = terrain.get_map(difficulty)
                ground_rects = terrain_data["ground_rects"]
                platform_rects = terrain_data["platform_rects"]
                item_rects, boost_rects = items.get_items_and_boosts(
                    difficulty, self.WIDTH, self.HEIGHT
                )
                score = 0

            scroll_x = max(
                0, min(player.x - self.WIDTH // 2, background_width - self.WIDTH)
            )
            self.SCREEN.blit(background, (-scroll_x, 0))

            # Vykreslení země
            for rect in ground_rects:
                tile_width = ground_texture.get_width()
                tiles_x = rect.width // tile_width + 1
                for x in range(tiles_x):
                    stretched_ground = pygame.transform.scale(
                        ground_texture, (tile_width, rect.height)
                    )
                    pos_x = rect.x + x * tile_width - scroll_x
                    self.SCREEN.blit(stretched_ground, (pos_x, rect.y))

            # Vykreslení platforem
            for rect in platform_rects:
                platform_texture = pygame.transform.scale(
                    platform_texture_original, (rect.width, rect.height)
                )
                self.SCREEN.blit(platform_texture, (rect.x - scroll_x, rect.y))

            # Vykreslení mincí
            for coin in item_rects[:]:
                if player.get_rect().colliderect(coin):
                    self.coin_grab.play()
                    item_rects.remove(coin)
                    score += 1

                    if score == 15:
                        self.lift_sound.play()
                else:
                    self.SCREEN.blit(item_texture, (coin.x - scroll_x, coin.y))

            # Vykresleni boostu
            for boost in boost_rects:
                if player.get_rect().colliderect(boost):
                    boost_rects.remove(boost)
                    self.power_up.play()
                    player.jump_boost_end_time = (
                            pygame.time.get_ticks() + 5000
                    )  # boost na 5 sekund
                else:
                    self.SCREEN.blit(boost_texture, (boost.x - scroll_x, boost.y))

            for lift_rect in lift_rects:
                if score == 15:
                    self.SCREEN.blit(
                        lift_texture_open, (lift_rect.x - scroll_x, lift_rect.y)
                    )
                    if player.get_rect().colliderect(lift_rect):
                        print("konec")
                        final_text = get_font(150).render("YOU WON!", True, "#FFA600")
                        final_rect = final_text.get_rect(
                            center=(self.WIDTH // 2, self.HEIGHT // 2)
                        )
                        self.SCREEN.blit(final_text, final_rect)
                        pygame.display.update()
                        pygame.time.wait(2000)
                        self.menu_birds_sfx.stop()
                        self.game_song.stop()
                        return
                else:
                    self.SCREEN.blit(
                        lift_texture_closed, (lift_rect.x - scroll_x, lift_rect.y)
                    )

                    # Vykreslení hráče
            player.draw(self.SCREEN, scroll_x)

            # Vykresleni skore
            score_text = get_font(30).render(f"Score: {score}", True, "#FFFFFF")
            self.SCREEN.blit(score_text, (30, 30))

            # Vykresleni casu pro boost
            current_time = pygame.time.get_ticks()
            if player.jump_boost_end_time > current_time:
                remaining_ms = player.jump_boost_end_time - current_time
                remaining_seconds = round(remaining_ms / 1000, 1)
                boost_text = get_font(30).render(
                    f"Boost: {remaining_seconds}s", True, "#FFD700"
                )
                self.SCREEN.blit(boost_text, (30, 70))

            # Pauza
            if paused:
                pause_text = get_font(80).render("PAUSED", True, "#04049B")
                pause_rect = pause_text.get_rect(center=(self.WIDTH // 2, 150))
                self.SCREEN.blit(pause_text, pause_rect)

                RETURN_BUTTON.change_color(pygame.mouse.get_pos())
                RETURN_BUTTON.update(self.SCREEN)

            pygame.display.update()
            self.clock.tick(60)

    def options(self) -> None:
        screen_run = True

        BACK_BUTTON = self.create_button(
            "BACK",
            (self.WIDTH // 2, 500),
            font_size=60,
            img_path="assets/sprites/menu_sprites/Play Rect.png",
            base_color="#1C86E5",
        )

        RES_BUTTONS = [
            self.create_button("800x600", (self.WIDTH // 2, 150)),
            self.create_button("1024x768", (self.WIDTH // 2, 250)),
            self.create_button("1280x720", (self.WIDTH // 2, 350)),
        ]

        while screen_run:
            self.SCREEN.blit(self.scaled_background, (0, 0))
            MOUSE_POS = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON.check_for_input(MOUSE_POS):
                        self.menu_pop_btn_sfx.play()
                        return
                    for btn in RES_BUTTONS:
                        if btn.check_for_input(MOUSE_POS):
                            width, height = map(int, btn.text_input.split("x"))
                            self.change_resolution(width, height)
                            self.menu_pop_btn_sfx.play()
                            return

            for btn in RES_BUTTONS + [BACK_BUTTON]:
                btn.change_color(MOUSE_POS)
                btn.update(self.SCREEN)

            pygame.display.update()
            self.clock.tick(60)

    def menu(self) -> None:

        if not pygame.mixer.get_busy():
            self.menu_song.play(loops=-1)

        while True:

            self.SCREEN.blit(self.scaled_background, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = get_font(150).render("JUMPMAN", True, "#04049B")
            MENU_RECT = MENU_TEXT.get_rect(center=(self.WIDTH // 2, 100))
            self.SCREEN.blit(MENU_TEXT, MENU_RECT)

            PLAY_BUTTON = Button(
                image=pygame.image.load("assets/sprites/menu_sprites/Play Rect.png"),
                pos=(self.WIDTH // 2, 250),
                text_input="PLAY",
                font=get_font(60),
                base_color="#CDE3F7",
                hovering_color="White",
            )
            OPTIONS_BUTTON = Button(
                image=pygame.image.load("assets/sprites/menu_sprites/Options Rect.png"),
                pos=(self.WIDTH // 2, 400),
                text_input="OPTIONS",
                font=get_font(50),
                base_color="#CDE3F7",
                hovering_color="White",
            )
            QUIT_BUTTON = Button(
                image=pygame.image.load("assets/sprites/menu_sprites/Quit Rect.png"),
                pos=(self.WIDTH // 2, 550),
                text_input="QUIT",
                font=get_font(50),
                base_color="#CDE3F7",
                hovering_color="White",
            )

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.change_color(MENU_MOUSE_POS)
                button.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.check_for_input(MENU_MOUSE_POS):
                        self.menu_pop_btn_sfx.play()
                        self.menu_song.stop()
                        self.play()
                        self.menu_song.play(loops=-1)
                    if OPTIONS_BUTTON.check_for_input(MENU_MOUSE_POS):
                        self.menu_pop_btn_sfx.play()
                        self.options()
                    if QUIT_BUTTON.check_for_input(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
            self.clock.tick(60)

    def change_resolution(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        if (width, height) in self.menu_backgrounds:
            self.scaled_background = self.menu_backgrounds[(width, height)]
        else:
            self.scaled_background = pygame.transform.smoothscale(
                list(self.menu_backgrounds.values())[0], (width, height)
            )

    def create_button(
            self,
            text,
            pos,
            font_size=40,
            img_path="assets/sprites/menu_sprites/Options Rect.png",
            base_color="#FFD700",
            hover_color="White",
    ):
        return Button(
            image=pygame.image.load(img_path),
            pos=pos,
            text_input=text,
            font=get_font(font_size),
            base_color=base_color,
            hovering_color=hover_color,
        )
