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

    def play(self):
        screen_run = True
        player = Player()
        ground = [pygame.Rect(0, 500, 800, 100)]  # základní zem

        while screen_run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    screen_run = False

            player.handle_input()
            player.update()
            player.checkColisions([], ground)

            self.SCREEN.fill((255, 255, 255))  # bílé pozadí

            # Vykresli zem
            for rect in ground:
                pygame.draw.rect(self.SCREEN, (0, 200, 0), rect)

            # Vykresli hráče
            player.draw(self.SCREEN)

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()

    def options(self):
        menu_pop_btn_sfx = pygame.mixer.Sound("assets/sounds/pop.wav")
        menu_pop_btn_sfx.set_volume(0.2)
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
                        menu_pop_btn_sfx.play()
                        return  # jen návrat, menu zavolá znovu hlavní smyčka

            self.SCREEN.fill((0, 0, 255))
            BACK_BUTTON.changeColor(MOUSE_POS)
            BACK_BUTTON.update(self.SCREEN)

            pygame.display.update()
            self.clock.tick(60)       

    def menu(self):
        menu_birds_sfx = pygame.mixer.Sound("assets/sounds/birds.wav")
        menu_pop_btn_sfx = pygame.mixer.Sound("assets/sounds/pop.wav")
        menu_pop_btn_sfx.set_volume(0.2)
        menu_background = pygame.image.load("assets/sprites/menu_sprites/background_menu.png").convert()
        pygame.display.set_caption("Menu")

        menu_background = pygame.transform.scale(menu_background, (800, 600))
        background_x = (self.WIDTH - menu_background.get_width()) // 2
        background_y = (self.HEIGHT - menu_background.get_height()) // 2
        menu_birds_sfx.play(loops=-1, maxtime=0)

        while True:
            self.SCREEN.blit(menu_background,(background_x, background_y))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = get_font(100).render("MAIN MENU", True, "#04049B")
            MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))
            self.SCREEN.blit(MENU_TEXT, MENU_RECT)

            PLAY_BUTTON = Button(image=pygame.image.load("assets/sprites/menu_sprites/Play Rect.png"), pos=(400, 250), 
                            text_input="PLAY", font=get_font(60), base_color="#1C86E5", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("assets/sprites/menu_sprites/Options Rect.png"), pos=(400, 400), 
                            text_input="OPTIONS", font=get_font(50), base_color="#1C86E5", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/sprites/menu_sprites/Quit Rect.png"), pos=(400, 550), 
                            text_input="QUIT", font=get_font(50), base_color="#1C86E5", hovering_color="White")

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        menu_pop_btn_sfx.play()
                        menu_birds_sfx.stop()
                        self.play()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        menu_pop_btn_sfx.play()
                        self.options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()                    
            pygame.display.update()
