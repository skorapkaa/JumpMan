import pygame

class Items:
    def __init__(self):
        self.item_data = {
            "medium": {
                "coins": [
                    pygame.Rect(182, 430, 16, 16),
                    pygame.Rect(332, 360, 16, 16),
                    pygame.Rect(482, 290, 16, 16),
                    pygame.Rect(632, 220, 16, 16),
                    pygame.Rect(232, 140, 16, 16),
                    pygame.Rect(832, 140, 16, 16),
                    pygame.Rect(1482, 290, 16, 16),
                    pygame.Rect(600, 500, 16, 16),
                    pygame.Rect(700, 500, 16, 16),
                    pygame.Rect(1200, 500, 16, 16),
                    pygame.Rect(1300, 500, 16, 16),
                    pygame.Rect(1400, 500, 16, 16),
                    pygame.Rect(1900, 500, 16, 16),
                    pygame.Rect(2000, 500, 16, 16),
                    pygame.Rect(2100, 500, 16, 16),
                ],
                "boosts": [
                    pygame.Rect(1332, 220, 16, 16),
                ]
            }
        }

    def get_items_and_boosts(self, difficulty):
        difficulty = difficulty.lower()
        data = self.item_data.get(difficulty, self.item_data["medium"])
        return data["coins"].copy(), data["boosts"].copy()
