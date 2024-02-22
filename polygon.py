'''
    Summary of this file
'''

from utils import *

class Polygon(pygame.sprite.Sprite):
    '''Polygon ring rotates using  Q/A (counterclockwise) and E/D (clockwise).

    Args:
        pygame (pygame.sprite.Sprite): base class
    '''
    
    def __init__(self, space, radius, N, wall_thickness=50, color=random.choice(list(PALLETE.values()))):
        super().__init__()
        self.radius = radius
        self.N = N                  
        self.color = color
        self.wall_thickness = wall_thickness
        self.inner_radius = self.radius - self.wall_thickness

        # self.active = False     # active ==> ball currently inside
        # self.keys_pressed = []
        
        # Calculated properties
        self.position = Vector2(CENTER)
        self.theta = self.get_theta()
        self.vertices = self.get_vertices(self.radius, self.radius)
        self.inner_vertices = self.get_vertices(self.inner_radius, self.radius)
        self.image = pygame.Surface((self.radius*2, self.radius*2))
        self.image.fill((0, 0, 0))
        self.draw_ring()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.mask = pygame.mask.from_surface(self.image)
        
        # pymunk setup as a kinematic body because it needs to be able to rotate
        self.body = pymunk.Body(0, 0, pymunk.Body.STATIC)
        self.body.position = float(CENTER.x), float(CENTER.y)
        sides = self.get_vertices(self.inner_radius)
        Polygon.attach_segments(sides, self.body, space)
    
    def get_theta(self):
        '''
            Returns the calculation for the internal angle in radians. Used for 
            drawing the vertices of the polygon.
        '''
        return (2 * np.pi) / self.N
    
    def get_vertices(self, radius, offset=0, tilt=1.5*np.pi):
        vertices = []
        for i in range(1, self.N + 1):
            x = (radius * np.cos(tilt + self.theta * i)) + offset
            y = (radius * np.sin(tilt + self.theta * i)) + offset
            vertices.append(Vector2(x, y))
        return vertices
    
    @staticmethod
    def attach_segments(vertices, body, space):
        '''
            Returns the line segments connecting all the passed vertices together,
            adding to the specified body and making all segments neighbors.
            
            Effectively creates a polygon for pymunk purposes.
        '''
        space.add(body)
        for i in range(len(vertices)):
            j = i + 1 if i < len(vertices)-1 else 0
            point_a = vertices[i][0], vertices[i][1]
            point_b = vertices[j][0], vertices[j][1]
            segment = pymunk.Segment(body, point_a, point_b, 2)
            segment.set_neighbors(point_a, point_b) # there is a neighbor present at both endpoints of this segment
            segment.density = 100
            segment.elasticity = 0.98
            segment.friction = 0.65
            space.add(segment)
        # return segment_list
        
    def draw_ring(self):
        '''
            Draw the ring according to the body's position of the polygon.
        '''
        pygame.draw.polygon(self.image, random.choice(list(RING_PALLETE.values())), self.vertices)
        pygame.draw.polygon(self.image, (0, 0, 0), self.inner_vertices)
    
    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.image, blit_position)
    
    def get_closest_side(self, point):
        '''
            Returns the two points from the inner vertices that are closest to 
            the passed point.
        '''
        distances = list(map(point.distance_to, self.inner_vertices))
        distances_dict = dict(zip(distances, self.inner_vertices))
        
        # Get the shortest distance from the point to a vertex and remove from distances
        closest_distance = min(distances_dict.keys())
        closest_vertex = distances_dict.pop(closest_distance)
        
        # Get the next shortest distance from the point to the remaining vertices and remove from distances
        next_distance = min(distances_dict.keys())
        next_vertex = distances_dict.pop(next_distance)
        
        # Return the vector representing the slope of the closest side
        return get_slope(Vector2(closest_vertex), Vector2(next_vertex))
    
    def update(self, dt):
        pass
        
    def cw_rotate(self, dt):
        pass
        
    def ccw_rotate(self, dt):   
        pass