import pygame

class Terrain:
    def __init__(self):
        self.maps = {
            "medium": {
                "ground_rects": [
                    pygame.Rect(0, 550, 800, 50),         # země do x = 800
                    # díra mezi 800 a 1000
                    pygame.Rect(1000, 550, 600, 50),      # země od x = 1000 do 1600
                    # díra mezi 1600 a 1800
                    pygame.Rect(1800, 550, 800, 50),  

                ],
                "platform_rects": [
                    pygame.Rect(150, 470, 100, 15),
                    pygame.Rect(300, 400, 100, 15),
                    pygame.Rect(450, 330, 100, 15),
                    pygame.Rect(600, 260, 100, 15),
                    pygame.Rect(200, 180, 100, 15),
                ],
            },
        }

    def get_map(self, difficulty):
        difficulty = difficulty.lower()  # zajistí, že případně velká písmena nevadí
        return self.maps.get(difficulty, self.maps["medium"])
