import pygame


class Terrain:
    def __init__(self, screen_width, screen_height):
        ground_height = int(screen_height * 0.24)
        ground_y = screen_height - ground_height
        platform_height = int(screen_height * 0.021)
        platform_ys = [0.65, 0.56, 0.46, 0.36, 0.25, 0.46, 0.36, 0.25, 0.60, 0.65, 0.56]
        platform_y = [int(screen_height * h) for h in platform_ys]
        self.maps = {
            "medium": {
                "ground_rects": [
                    pygame.Rect(0, ground_y, 800, ground_height),
                    pygame.Rect(1000, ground_y, 600, ground_height),
                    pygame.Rect(1800, ground_y, 800, ground_height),
                ],
                "platform_rects": [
                    pygame.Rect(150, platform_y[0], 100, platform_height),
                    pygame.Rect(300, platform_y[1], 100, platform_height),
                    pygame.Rect(450, platform_y[2], 100, platform_height),
                    pygame.Rect(600, platform_y[3], 100, platform_height),
                    pygame.Rect(200, platform_y[4], 100, platform_height),
                    pygame.Rect(1450, platform_y[5], 100, platform_height),
                    pygame.Rect(1300, platform_y[6], 100, platform_height),
                    pygame.Rect(800, platform_y[7], 100, platform_height),
                    pygame.Rect(950, platform_y[8], 200, platform_height),
                    pygame.Rect(1450, platform_y[9], 100, platform_height),
                    pygame.Rect(1600, platform_y[10], 200, platform_height),
                ],

                "lift": [
                    pygame.Rect(2150, ground_y-125, 70, 80)
                ]
            },
        }

    def get_map(self, difficulty):
        difficulty = difficulty.lower()
        return self.maps.get(difficulty, self.maps["medium"])
