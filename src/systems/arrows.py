# CoulombHelper: A simple electronic physics simulator
# Copyright (C) 2026  theolaos

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pygame
import math

from dataclasses import dataclass

from .tleng2 import *

from .coulomb import ParticleComp

@dataclass
class ArrowComp:
    color: pygame.Color
    body_width: int = 2
    head_width: int = 4
    head_height: int = 2

class ArrowsComp:
    color: pygame.Color
    body_width: int = 2
    head_width: int = 4
    head_height: int = 2


def draw_arrow(
        start: pygame.Vector2,
        end: pygame.Vector2,
        color: pygame.Color,
        body_width: int = 2,
        head_width: int = 4,
        head_height: int = 2,
    ) -> tuple[pygame.Surface, pygame.Vector2, tuple[int,int]]:
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

    # vector from end to start (kept from original logic)
    arrow = start - end

    # compute AABB for start/end and expand by padding to fit rotated head/body
    min_x = min(start.x, end.x)
    min_y = min(start.y, end.y)
    max_x = max(start.x, end.x)
    max_y = max(start.y, end.y)
    pad = max(body_width, head_width, head_height) / 2 + 2
    top_left = pygame.Vector2(math.floor(min_x - pad), math.floor(min_y - pad))
    size = (max(1, math.ceil(max_x - min_x + pad * 2)), max(1, math.ceil(max_y - min_y + pad * 2)))
    
    # create temporary surface with per-pixel alpha and draw there
    temp_surf = pygame.Surface(size, pygame.SRCALPHA)
    shifted_start = start - top_left
    shifted_end = end - top_left

    # reuse shifted positions below when building verts
    draw_surface = temp_surf

    # angle difference from arrow vector to up vector
    angle = arrow.angle_to(pygame.Vector2(0, -1))  
    body_length = arrow.length() - head_height

    # Create the triangle head around the origin (local coords)
    head_verts = [
        pygame.Vector2(0, head_height / 2),  # Center
        pygame.Vector2(head_width / 2, -head_height / 2),  # Bottomright
        pygame.Vector2(-head_width / 2, -head_height / 2),  # Bottomleft
    ]

    # Rotate and translate the head into place relative to shifted_start
    translation = pygame.Vector2(0, arrow.length() - (head_height / 2)).rotate(-angle)
    for i in range(len(head_verts)):
        head_verts[i].rotate_ip(-angle)
        head_verts[i] += translation
        head_verts[i] += shifted_start

    pygame.gfxdraw.aapolygon(draw_surface, head_verts, color)
    pygame.draw.polygon(draw_surface, color, head_verts)

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
            body_verts[i] += shifted_start

        pygame.gfxdraw.aapolygon(draw_surface, body_verts, color)
        pygame.draw.polygon(draw_surface, color, body_verts)

    # blit the temporary surface onto the real surface
    # surface.blit(temp_surf, (int(top_left.x), int(top_left.y)))

    return temp_surf, top_left, size




class DrawArrows(ecs.System):
    def parameters(self, world: ecs.World) -> None:
        self.world = world
    
    def update(self) -> None:
        for e, (particle, arrow_conf, renderable) in self.world.fast_query(ParticleComp, ArrowsComp, RenderablesComp):
            ...


class InitDrawArrow(ecs.System):
    def parameters(self, world: ecs.World) -> None:
        self.world = world

    def update(self) -> None:
        for e, rsc in self.world.query(RenderablesComp, has=(ArrowComp, ParticleComp)):
            ...


class DrawArrow(ecs.System):
    def parameters(self, world: ecs.World) -> None:
        self.world = world
    
    def update(self) -> None:
        for e, (particle, arrow, rsc) in self.world.fast_query(ParticleComp, ArrowComp, RenderablesComp):
            start = particle.self_vec
            
            end = (particle.self_vec + particle.general_vec)

            color = arrow.color
            body_width = arrow.body_width
            head_width = arrow.head_width
            head_height = arrow.head_height

            surface, topleft, size = draw_arrow(start, end, color, body_width, head_width, head_height)
            rc = RenderableComp(
                surface
            )
            rc.rect = topleft
            rc.size = size
            
            rsc.renderable[1].append(rc)

