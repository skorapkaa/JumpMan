from typing import Tuple, List, Any

class Button:
	def __init__(self, image: Any, pos: Tuple[int, int], text_input: str, font: Any, base_color: Tuple[int, int, int], hovering_color: Tuple[int, int, int]):
		self.image: Any = image
		self.x_pos: int = pos[0]
		self.y_pos: int = pos[1]
		self.font: Any = font
		self.base_color: Tuple[int, int, int] = base_color
		self.hovering_color: Tuple[int, int, int] = hovering_color
		self.text_input: str = text_input
		self.text: Any = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect: Any = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect: Any = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen: Any) -> None:
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def check_for_input(self, position: List[int]) -> bool:
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def change_color(self, position: List[int]) -> None:
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

