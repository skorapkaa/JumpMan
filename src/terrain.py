import pygame


class Terrain:
    def __init__(self, screen_width, screen_height):
        ground_height = int(screen_height * 0.24)
        ground_y = screen_height - ground_height
        platform_height = int(screen_height * 0.021)  # 15/720 ~ 0.021
        # Platform y-positions as a proportion of screen height
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
                "items": [
                    pygame.Rect(182, int(screen_height * 0.60), 16, 16),
                    pygame.Rect(332, int(screen_height * 0.50), 16, 16),
                    pygame.Rect(482, int(screen_height * 0.40), 16, 16),
                    pygame.Rect(632, int(screen_height * 0.30), 16, 16),
                    pygame.Rect(232, int(screen_height * 0.19), 16, 16),
                    pygame.Rect(832, int(screen_height * 0.19), 16, 16),
                    pygame.Rect(1482, int(screen_height * 0.40), 16, 16),
                    pygame.Rect(600, int(screen_height * 0.70), 16, 16),
                    pygame.Rect(700, int(screen_height * 0.70), 16, 16),
                    pygame.Rect(800, int(screen_height * 0.70), 16, 16),
                    pygame.Rect(1200, int(screen_height * 0.70), 16, 16),
                    pygame.Rect(1300, int(screen_height * 0.70), 16, 16),
                    pygame.Rect(1400, int(screen_height * 0.70), 16, 16),
                    pygame.Rect(1900, int(screen_height * 0.70), 16, 16),
                    pygame.Rect(2000, int(screen_height * 0.70), 16, 16),
                    pygame.Rect(2100, int(screen_height * 0.70), 16, 16),
                ],
                "boosts": [
                    pygame.Rect(1332, int(screen_height * 0.30), 16, 16),
                ],
            },
        }

    def get_map(self, difficulty):
        difficulty = difficulty.lower()
        return self.maps.get(difficulty, self.maps["medium"])
