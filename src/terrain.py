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
                    pygame.Rect(1450, 330, 100, 15),
                    pygame.Rect(1300, 260, 100, 15),
                    pygame.Rect(800, 180, 100, 15),
                    pygame.Rect(950, 430, 200, 15),
                    pygame.Rect(1450, 470, 100, 15),
                    pygame.Rect(1600, 400, 200, 15),

                ],
                "items": [
                    #Coiny ve vzduchu
                    pygame.Rect(182, 430, 16, 16),
                    pygame.Rect(332, 360, 16, 16),
                    pygame.Rect(482, 290, 16, 16),
                    pygame.Rect(632, 220, 16, 16),
                    pygame.Rect(232, 140, 16, 16),
                    pygame.Rect(832, 140, 16, 16),
                    pygame.Rect(1482, 290, 16, 16),          



                    #Coiny na zemi
                    pygame.Rect(600, 500, 16, 16),
                    pygame.Rect(700, 500, 16, 16),
                    pygame.Rect(800, 500, 16, 16),
                    pygame.Rect(1200, 500, 16, 16),
                    pygame.Rect(1300, 500, 16, 16),
                    pygame.Rect(1400, 500, 16, 16), 
                    pygame.Rect(1900, 500, 16, 16),
                    pygame.Rect(2000, 500, 16, 16),
                    pygame.Rect(2100, 500, 16, 16),                                       

                ],
                "boosts": [
                    pygame.Rect(1332, 220, 16, 16),

                ],
            },
        }

    def get_map(self, difficulty):
        difficulty = difficulty.lower()
        return self.maps.get(difficulty, self.maps["medium"])
