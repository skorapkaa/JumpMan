import pygame

class Terrain:
    def __init__(self):
        self.maps = {
            "medium": {
                "ground_rects": [
                    pygame.Rect(0, 550, 750, 50),
                    pygame.Rect(1000, 550, 550, 50),
                    pygame.Rect(1800, 550, 800, 50),
                ],
                "platform_rects": [
                    pygame.Rect(150, 470, 100, 15),
                    pygame.Rect(300, 400, 100, 15),
                    pygame.Rect(450, 330, 100, 15),
                    pygame.Rect(600, 260, 100, 15),
                    pygame.Rect(200, 180, 100, 15),
                    pygame.Rect(1450, 330, 100, 15),
                    pygame.Rect(1300, 260, 100, 15),
                    pygame.Rect(800, 180, 100, 15),
                    pygame.Rect(950, 430, 200, 15),
                    pygame.Rect(1450, 470, 100, 15),
                    pygame.Rect(1600, 400, 200, 15),
                ],
            },
        }

    def get_map(self, difficulty):
        difficulty = difficulty.lower()
        return self.maps.get(difficulty, self.maps["medium"])
