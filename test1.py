class States:
    s1 = 1
    s2 = 2
    s3 = 3

def print_s1():
    print(States.s1)

def print_s2():
    print(States.s2)

def change_s2(s2):
    States.s2 = s2

# pygame.math module, pygame.math.Vector2 object
# https://www.pygame.org/docs/ref/math.html
#
# How to know the angle between two vectors?
# https://stackoverflow.com/questions/42258637/how-to-know-the-angle-between-two-vectors/64563327#64563327
#
# GitHub - PyGameExamplesAndAnswers - Vector - Angle between vectors
# https://github.com/Rabbid76/PyGameExamplesAndAnswers/blob/master/documentation/pygame/pygame_math_vector_and_reflection.md

import pygame
import math

def angle_of_vector(x, y):
    #return math.degrees(math.atan2(-y, x))            # 1: with math.atan
    return pygame.math.Vector2(x, y).angle_to((0, -1))  # 2: with pygame.math.Vector2.angle_to
    
def angle_of_line(x1, y1, x2, y2):
    #return math.degrees(math.atan2(-y1-y2, x2-x1))    # 1: math.atan
    return angle_of_vector(x2-x1, y2-y1)               # 2: pygame.math.Vector2.angle_to
    
pygame.init()
window = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)

angle = 0
radius = 150
vec = (0, radius)

run = True
while run:
    clock.tick(1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False

    cpt = window.get_rect().center #center_point
    pt = cpt[0] + vec[0], cpt[1] + vec[1] # other point
    angle = angle_of_vector(*vec)
    

    window.fill((255, 255, 255))

    pygame.draw.circle(window, (0, 0, 0), cpt, radius, 1) # circle
    pygame.draw.line(window, (0, 255, 0), cpt, (cpt[0], cpt[1]+radius), 3) # the green stationary line
    pygame.draw.line(window, (255, 0, 0), cpt, pt, 3) # moving CCW line

    text_surf = font.render(str(round(angle/5)*5) + "°", True, (255, 0, 0)) # text
    text_surf.set_alpha(127)
    window.blit(text_surf, text_surf.get_rect(bottomleft = (cpt[0]+20, cpt[1]-20)))
    
    pygame.display.flip()

    print(angle,end=' ')
    angle = (angle + 1) % 360
    print(angle, end=' ')
    vec = radius * math.cos(angle*math.pi/180), radius * -math.sin(angle*math.pi/180)
    print(vec)

pygame.quit()
exit()