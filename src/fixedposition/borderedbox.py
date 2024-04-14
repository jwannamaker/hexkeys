import pygame
from pygame import Color, Font

from fixedposition import FixedPosition
from asset.asset import Asset
from asset.shape import BOX


class BorderedBox(FixedPosition):
    def __init__(self, game, fixed_text: str, bg_color: Color, font_color: Color,
                 font_size: int, width: float, height: float, border: int,
                 position: tuple[float, float]):
        self.game = game
        self.font: Font = self.game.font
        self.asset = Asset([self.game.all_entities, self.game.HUD],
                           BOX(width, height, border),
                           bg_color,
                           position)
        self.border = border
        self.font_color = font_color

        self.fixed_text = fixed_text
        self.fixed_text_image = self.font.render(self.fixed_text, False, self.font_color)
        self.fixed_text_rect = self.fixed_text_image.get_bounding_rect()

        self.text = 'look away...'
        self.text_image = self.font.render(self.text, False, self.font_color)

        self.asset.image.blit(self.fixed_text_image,
                              [self.get_left_align_x(), self.get_center_align_y(self.fixed_text)]),
        self.asset.image.blit(self.text_image,
                              [self.get_right_align_x(self.text), self.get_center_align_y(self.text)])

        self.update_func = None

    def get_center_align_y(self, text: str) -> float:
        text_height = self.font.size(text)[1]
        return self.asset.rect.centery-(text_height/2)

    def get_left_align_x(self) -> float:
        return self.asset.rect.left+(self.border*3)

    def get_right_align_x(self, text: str) -> float:
        text_width = self.font.size(text)[0]
        return self.asset.rect.right-(self.border*3)-text_width

    def draw(self, surface) -> None:
        self.fixed_text_image = self.font.render(self.fixed_text, False, self.font_color)
        self.text_image = self.font.render(self.text, False, self.font_color)
        self.asset.image.blit(self.fixed_text_image,
            [self.get_left_align_x(), self.get_center_align_y(self.fixed_text)]),
        self.asset.image.blit(self.text_image,
            [self.get_right_align_x(self.text), self.get_center_align_y(self.text)])

        self.asset.draw(surface)

    def update(self, dt: float) -> None:
        if self.update_func is not None:
            self.text = str(self.update_func())
        self.draw(self.game.screen)

    def set_update_func(self, update_func: callable) -> None:
        self.update_func = update_func
