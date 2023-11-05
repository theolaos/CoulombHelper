import math
import pygame
from pygame import gfxdraw

def draw_arrow(
        surface: pygame.Surface,
        start: pygame.Vector2,
        end: pygame.Vector2,
        color: pygame.Color,
        body_width: int = 2,
        head_width: int = 4,
        head_height: int = 2,
    ):
    """Draw an arrow between start and end with the arrow head at the end. (No Antialiasing)
    
    Args:
        surface (pygame.Surface): The surface to draw on
        start (pygame.Vector2): Start position
        end (pygame.Vector2): End position
        color (pygame.Color): Color of the arrow
        body_width (int, optional): Defaults to 2.
        head_width (int, optional): Defaults to 4.
        head_height (float, optional): Defaults to 2.
    """
    arrow = start-end
    angle = arrow.angle_to(pygame.Vector2(0, -1))# angle diference from the arrow's vector to the up vector
    pygame.draw.line(surface, (255,0,0),start,start+pygame.Vector2(0, -100),3) 
    pygame.draw.line(surface, (0,255,0),start,start+pygame.Vector2(0, 100),3) 
    print(angle)
    body_length = arrow.length() - head_height

    # Create the triangle head around the origin
    head_verts = [
        pygame.Vector2(0, head_height / 2),  # Center
        pygame.Vector2(head_width / 2, -head_height / 2),  # Bottomright
        pygame.Vector2(-head_width / 2, -head_height / 2),  # Bottomleft
    ]

    # Rotate and translate the head into place
    translation = pygame.Vector2(0, arrow.length() - (head_height / 2)).rotate(-angle)
    # print(translation)
    for i in range(len(head_verts)):
        head_verts[i].rotate_ip(-angle)
        head_verts[i] += translation
        head_verts[i] += start

    pygame.gfxdraw.aapolygon(surface, head_verts, color)
    pygame.draw.polygon(surface, color, head_verts)

    #pygame.gfxdraw.aapolygon(surface,  aa_head_verts, color)

    # Stop weird shapes when the arrow is shorter than arrow head
    if arrow.length() >= head_height:
        # Calculate the body rect, rotate and translate into place
        body_verts = [
            pygame.Vector2(-body_width / 2, body_length / 2),  # Topleft
            pygame.Vector2(body_width / 2, body_length / 2),  # Topright
            pygame.Vector2(body_width / 2, -body_length / 2),  # Bottomright
            pygame.Vector2(-body_width / 2, -body_length / 2),  # Bottomleft
        ]
        translation = pygame.Vector2(0, body_length / 2).rotate(-angle)
        for i in range(len(body_verts)):
            body_verts[i].rotate_ip(-angle)
            body_verts[i] += translation
            body_verts[i] += start

        pygame.gfxdraw.aapolygon(surface,  body_verts, color)
        pygame.draw.polygon(surface, color, body_verts)
    
    dot = start.x*end.x + start.y*end.y      # Dot product between [x1, y1] and [x2, y2]
    det = start.x*end.y - start.y*end.x      # Determinant
    angle = math.atan2(det, dot) # radians
    print(angle)

pygame.init()

CLOCK = pygame.time.Clock()
FPS = 100

WIDTH = 1280
HEIGHT = 720
RESOLUTION = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(RESOLUTION)

while True:
    CLOCK.tick(FPS)

    for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()

    SCREEN.fill(pygame.Color("black"))

    center = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
    end = pygame.Vector2(pygame.mouse.get_pos())
    print(end,end=' ')
    draw_arrow(SCREEN, center, end, (pygame.Color("dodgerblue")), 3, 30, 30)

    pygame.display.flip()