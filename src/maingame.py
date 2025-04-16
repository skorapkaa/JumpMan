import pygame, sys
from button import Button
from player import Player

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

        # Načti zvuky a pozadí pouze jednou
        self.menu_birds_sfx = pygame.mixer.Sound("assets/sounds/birds.wav")
        self.menu_pop_btn_sfx = pygame.mixer.Sound("assets/sounds/pop.wav")
        self.menu_pop_btn_sfx.set_volume(0.2)
        self.menu_background = pygame.transform.scale(
            pygame.image.load("assets/sprites/menu_sprites/background_menu.png").convert(), (800, 600)
        )

    def play(self):
        screen_run = True
        paused = False
        player = Player()
        ground = [pygame.Rect(0, 500, 800, 100)]  # základní zem
        background = pygame.transform.scale(pygame.image.load("assets/sprites/game_sprites/background_game.png"), (800,600))

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

        while screen_run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused
                if paused and event.type == pygame.MOUSEBUTTONDOWN:
                    if RETURN_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        self.menu_pop_btn_sfx.play()
                        return  # návrat do menu

            if not paused:
                player.handle_input()
                player.update()
                player.checkColisions([], ground)

            self.SCREEN.blit(background, (0,0))

            # Vykresli zem
            for rect in ground:
                pygame.draw.rect(self.SCREEN, (139, 69, 19), rect)

            # Vykresli hráče
            player.draw(self.SCREEN)

            # Pokud je pauza, vykresli tlačítko
            if paused:
                pause_text = get_font(80).render("PAUSED", True, "#FF0000")
                pause_rect = pause_text.get_rect(center=(self.WIDTH // 2, 150))
                self.SCREEN.blit(pause_text, pause_rect)

                # Vykresli tlačítko návratu do menu
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
                        return  # návrat zpět do menu

            self.SCREEN.fill((0, 0, 255))
            BACK_BUTTON.changeColor(MOUSE_POS)
            BACK_BUTTON.update(self.SCREEN)

            pygame.display.update()
            self.clock.tick(60)

    def menu(self):
        # Spusť hudbu pokud ještě nehraje
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
                        self.menu_birds_sfx.play(loops=-1)  # znovu zapni po návratu
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.menu_pop_btn_sfx.play()
                        self.options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
            self.clock.tick(60)