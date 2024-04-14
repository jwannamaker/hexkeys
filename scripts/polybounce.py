import random
import json

import pygame
from pygame import Surface, Color

from ball import Ball
from borderedbox import BorderedBox


class PolyBounce:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([pygame.display.get_desktop_sizes()[0][0],
                                               pygame.display.get_desktop_sizes()[0][1]])
        self.SCREEN_SIZE = self.screen.get_size()
        self.CENTER = self.SCREEN_SIZE[0] // 2, self.SCREEN_SIZE[1] // 2
        self.PALETTE = self.grab_palette('../data/palette.json')
        self.background = Surface([self.screen.get_size()[0], self.screen.get_size()[1]])
        self.background.fill(self.PALETTE['black'][0])

        self.clock = pygame.Clock()
        self.fps = 60
        self.running = False
        self.frame_start = 0.0
        self.dt = 0.0

        self.all_entities = pygame.sprite.Group()
        self.HUD = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.player = Ball(self)

        self.font = self.load_font()
        self.unit_column = self.screen.get_width() / 8
        self.unit_row = self.screen.get_height() / 9
        self.hud_matrix = {}
        self.label_list = self.load_HUD()

    def grab_palette(self, json_filename: str) -> dict[str, Color]:
        palette = {}
        with open(json_filename, 'r') as palette_file:
            palette = json.load(palette_file)
        for key in palette.keys():
            palette[key] = [Color(value) for value in palette[key]]
        return palette

    def get_shuffled_colors(self, N: int) -> list[Color]:
        colors = list(self.PALETTE.keys())
        colors.remove('white')
        colors.remove('black')
        random.shuffle(colors)

        return random.sample(colors, N)

    def get_gradients(self, N: int, color: str) -> list[Color]:
        return random.sample([Color(self.PALETTE[color][i]) for i in range(N)], N)

    def load_font(self):
        pygame.font.init()
        return pygame.font.SysFont('monogram', 40)

    def load_HUD(self) -> list[BorderedBox]:
        self.unit_column = self.screen.get_width() / 8
        self.unit_row = self.screen.get_height() / 18
        self.hud_matrix = {
            'Level': {
                'width': 2,     # multiplied by the unit column width
                'height': 1,    # multiplied by the unit row height
                'border-width': 5,    # in pixels
                'border-radius': 15,    # in pixels
                'position': [1, 0.5],      # center, multiplied by unit column/row
                'font-size': 60,
                'bg-color': self.PALETTE['black'][1],
                'font-color': self.PALETTE['white'][0],
                'update-func': self.get_level
            },
            'Level Clock': {
                'width': 2,     # multiplied by the unit column width
                'height': 1,    # multiplied by the unit row height
                'border-width': 5,   # in pixels
                'border-radius': 15,    # in pixels
                'position': [7, 0.5],      # center, multiplied by unit column/row
                'font-size': 40,
                'bg-color': self.PALETTE['black'][1],
                'font-color': self.PALETTE['white'][0],
                'update-func': self.get_level_clock
            },
            'Inner Clock': {
                'width': 2,     # multiplied by the unit column width
                'height': 1,    # multiplied by the unit row height
                'border-width': 5,   # in pixels
                'border-radius': 15,    # in pixels
                'position': [7, 1.5],      # center, multiplied by unit column/row
                'font-size': 40,
                'bg-color': self.PALETTE['black'][1],
                'font-color': self.PALETTE['white'][0],
                'update-func': None
            },
            'Middle Clock': {
                'width': 2,     # multiplied by the unit column width
                'height': 1,    # multiplied by the unit row height
                'border-width': 5,   # in pixels
                'border-radius': 15,    # in pixels
                'position': [7, 2.5],      # center, multiplied by unit column/row
                'font-size': 40,
                'bg-color': self.PALETTE['black'][1],
                'font-color': self.PALETTE['white'][0],
                'update-func': None
            },
            'Outer Clock': {
                'width': 2,     # multiplied by the unit column width
                'height': 1,    # multiplied by the unit row height
                'border-width': 5,   # in pixels
                'border-radius': 15,    # in pixels
                'position': [7, 3.5],      # center, multiplied by unit column/row
                'font-size': 40,
                'bg-color': self.PALETTE['black'][1],
                'font-color': self.PALETTE['white'][0],
                'update-func': None
            },
            'Score': {
                'width': 4,     # multiplied by the unit column width
                'height': 1,    # multiplied by the unit row height
                'border-width': 5,   # in pixels
                'border-radius': 8,    # in pixels
                'position': [4, 0.5],      # center, multiplied by unit column/row
                'font-size': 40,
                'bg-color': self.PALETTE['black'][1],
                'font-color': self.PALETTE['white'][0],
                'update-func': self.player.get_score
            }
        }
        label_list = []
        for key in list(self.hud_matrix.keys()):
            label = BorderedBox(game=self,
                                fixed_text=key,
                                bg_color=self.hud_matrix[key]['bg-color'],
                                font_color=self.hud_matrix[key]['font-color'],
                                font_size=self.hud_matrix[key]['font-size'],
                                width=(self.hud_matrix[key]['width'] * self.unit_column)-5,
                                height=(self.hud_matrix[key]['height'] * self.unit_row)-5,
                                border=self.hud_matrix[key]['border-width'],
                                position=(self.hud_matrix[key]['position'][0] * self.unit_column,
                                          self.hud_matrix[key]['position'][1] * self.unit_row))
            label.draw(self.screen)
            self.hud_matrix[key]['label'] = label

    def get_level(self) -> str:
        return self.player.get_score() // 3

    def get_level_clock(self) -> str:
        return str(round(pygame.time.get_ticks() / 1000, 1)) + 's'

    def start(self) -> None:
        self.running = True
        self.main_loop()

    def main_loop(self) -> None:
        while self.running:
            self.frame_start = pygame.time.get_ticks()
            self.handle_user_input()
            self.process_game_logic()
            self.render()
        pygame.quit()

    def handle_user_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

            if event.type == pygame.KEYUP:
                # TODO: Implement the player input
                if event.key == pygame.K_RETURN:
                    print('freeze selected ring + start timer till unfreeze')

    def process_game_logic(self) -> None:
        """ Retrieve the position data from the PhysicsEngine. """
        self.dt = pygame.time.get_ticks() - self.frame_start
        self.all_entities.update(self.dt)
        for key in list(self.hud_matrix.keys()):
            if self.hud_matrix[key]['update-func'] != None:
                self.hud_matrix[key]['label'].set_text(str(self.hud_matrix[key]['update-func']()))

    def render(self):
        self.screen.blit(self.background, [0, 0])
        self.all_entities.draw(self.screen)

        self.clock.tick_busy_loop(self.fps)
        # PhysicsEngine.step_by(self.dt)
        pygame.display.flip()


if __name__ == "__main__":
    PolyBounce().start()

