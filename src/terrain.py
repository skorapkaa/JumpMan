import pygame

class Terrain:
    def __init__(self):
        self.maps = {
            "easy": [
                pygame.Rect(0, 550, 300, 50),
                pygame.Rect(500, 550, 300, 50),

                pygame.Rect(100, 450, 200, 20),
                pygame.Rect(400, 350, 150, 20),
                pygame.Rect(200, 250, 180, 20),
                pygame.Rect(600, 200, 100, 20),
            ],
            "medium": [
                pygame.Rect(0, 550, 800, 50),
                pygame.Rect(150, 470, 100, 20),
                pygame.Rect(300, 400, 100, 20),
                pygame.Rect(450, 330, 100, 20),
                pygame.Rect(600, 260, 100, 20),
                pygame.Rect(200, 180, 150, 20),
            ],
            "hard": [
                pygame.Rect(0, 550, 800, 50),
                pygame.Rect(100, 500, 80, 20),
                pygame.Rect(250, 420, 70, 20),
                pygame.Rect(400, 340, 60, 20),
                pygame.Rect(550, 260, 50, 20),
                pygame.Rect(700, 180, 40, 20),
            ]
        }

    def get_map(self, difficulty):
        return self.maps.get(difficulty, self.maps["easy"])
