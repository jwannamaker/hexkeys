'''
    Summary of this file here
'''

from utils import *
from polygon import Polygon
from ball import Ball

class ScreenBox:
    '''
        The pymunk simulation that the game references and interacts with, but 
        not necessarily what gets displayed to the screen 1:1
    '''
    def __init__(self, screen):
        
        # pymunk setup
        self.space = pymunk.Space()
        self.space.gravity = (0, 50)
        self.draw_options = pymunk.pygame_util.DrawOptions(screen)
        self.wall_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.wall_shape = self.get_walls(screen)
        self.space.add(self.wall_body)
        
    def get_walls(self, surface):
        margin = 0     # distance from the wall to the box
        x, y = surface.get_size()
        
        screen_corners = [(0, 0), (0, y), (x, y), (x, 0)]
        Polygon.attach_segments(screen_corners, self.wall_body)
        
    def step(self, dt):
        self.space.step(dt)

class PolyBounce:
    '''
    End Product:
        The Rings will: 
            Continually generate with random N = [3 - 7]
            All smoothly shrink towards the center once the ball 'clears' a ring
            Smoothly rotate CCW or CW when the player presses A or D respectively
            
        The Ball will:
            Change color according to the last Ring wall it touched
            Stay 'trapped' within the innermost ring until it clears
        
    '''
    def __init__(self):
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Johnny Tries Physics and Stuff!')
        self.clock = pygame.time.Clock()
        self.fps = 1
        self.dt = 1 / self.fps        # To create a semi-fixed framerate rendering
        self.running = False
        
        self.physics_box = ScreenBox(self.screen)
        
        # font setup
        pygame.font.init()
        self.font = load_font()
        
        # background setup
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill(BACKGROUND_PALLETE['black'])
        self.screen.blit(self.background, (0, 0))
        
        # game objects setup
        self.inner_ring = Polygon(self.physics_box.space, 350, 4)
        # self.outer_ring = Polygon(250, 6)
        # self.outer_outer_ring = Polygon(300, 6)
        self.ring_group = pygame.sprite.Group(self.inner_ring)
        
        self.player_ball = Ball(self.physics_box.space, 20)
        self.player_group = pygame.sprite.RenderClear(self.player_ball)
        
    def start(self):
        self.running = True
        self.main_loop()
    
    def set_fps(self, fps):
        self.fps = fps
        
    def display_stats(self):
        player_info = []
        player_info.append('{:15s} {:8.2f} {:8.2f}'.format('Position', self.player_ball.position[0], self.player_ball.position[1]))
        player_info.append('{:15s} {:8.2f} {:8.2f}'.format('Velocity', self.player_ball.velocity[0], self.player_ball.velocity[1]))
        
        # TODO Make some fancy display rect for the text to go onto and then blit that onto the screen
        
        for i, line in enumerate(player_info):
            self.screen.blit(self.font.render(line, True, PALLETE['white']), (0, SCREEN_SIZE.y - 40 + 20 * i))
    
    def handle_user_input(self):
        '''
            Poll for user events, updating lists containing with movements 
            that need to be applied to game objects.
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_LSHIFT:
                    self.player_ball.add_key_held('boost')
                
                if event.key == pygame.K_w:
                    self.player_ball.add_key_held('up')
                if event.key == pygame.K_s:
                    self.player_ball.add_key_held('down')
                if event.key == pygame.K_a:
                    self.player_ball.add_key_held('left')
                if event.key == pygame.K_d:
                    self.player_ball.add_key_held('right')
                
                if event.key == pygame.K_SPACE:
                    self.player_ball.add_key_held('jump')
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    self.player_ball.remove_key_held('boost')
                    
                if event.key == pygame.K_w:
                    self.player_ball.remove_key_held('up')
                if event.key == pygame.K_s:
                    self.player_ball.remove_key_held('down')
                if event.key == pygame.K_d:
                    self.player_ball.remove_key_held('right')
                if event.key == pygame.K_a:
                    self.player_ball.remove_key_held('left')
                
                if event.key == pygame.K_SPACE:
                    self.player_ball.remove_key_held('jump')
                    
                if event.key == pygame.K_q:
                    self.inner_ring.ccw_rotate()
                if event.key == pygame.K_e:
                    self.inner_ring.cw_rotate()
    
    def process_game_logic(self):
        '''
            Updates the player_group and the ring_group according to the current
            game state.
        '''
        self.player_group.update(self.dt)
        self.ring_group.update(self.dt)
    
    def draw(self):
        '''
            Draw the new state of each object in the game onto the screen.
        '''
        self.screen.blit(self.background, (0, 0))
        # drawing some lines for the purpose of debugging/analyzing output values
        pygame.draw.line(self.screen, (255, 0, 0), (self.player_ball.position.x, 0), (self.player_ball.position.x, SCREEN_SIZE.y))
        pygame.draw.line(self.screen, (255, 0, 0), (0, self.player_ball.position.y), (SCREEN_SIZE.x, self.player_ball.position.y))
        self.display_stats()
        self.player_ball.draw(self.screen)
        self.ring_group.draw(self.screen)
        
        # TODO: Add some logic to address the need for semi-fixed framerate
        self.dt = self.clock.tick(self.fps) / 1000
        self.physics_box.step(self.dt)
        pygame.display.flip()
        
    def main_loop(self):
        while self.running:
            self.handle_user_input()
            self.process_game_logic()
            self.draw()
        pygame.quit()