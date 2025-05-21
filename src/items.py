import pygame

class Items:
    def __init__(self):
        # Store item positions as (x, y) proportions of width/height
        self.item_data = {
            "medium": {
                "coins": [
                    (182, 0.597),
                    (332, 0.5),
                    (482, 0.403),
                    (632, 0.306),
                    (232, 0.194),
                    (832, 0.194),
                    (1482, 0.403),
                    (600, 0.694),
                    (700, 0.694),
                    (1200, 0.694),
                    (1300, 0.694),
                    (1400, 0.694),
                    (1900, 0.694),
                    (2000, 0.694),
                    (2100, 0.694),
                ],
                "boosts": [
                    (1332, 0.306),
                ]
            }
        }

    def get_items_and_boosts(self, difficulty, screen_width=1280, screen_height=720):
        difficulty = difficulty.lower()
        data = self.item_data.get(difficulty, self.item_data["medium"])
        coins = [pygame.Rect(x, int(screen_height * y), 16, 16) for x, y in data["coins"]]
        boosts = [pygame.Rect(x, int(screen_height * y), 16, 16) for x, y in data["boosts"]]
        return coins, boosts
