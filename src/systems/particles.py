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

from math import sqrt

from ..log import *

from ..tleng2 import *

from ..components import ParticleComp, ArrowComp
from ..coulomb import CoulombCalc


class CalculateForces(ecs.System):
    def parameters(self, world: ecs.World) -> None:
        self.world = world

        self.vec_zero = pygame.Vector2(0,0)

    def update(self) -> None:
        ent_comp = self.world.single_fast_query(ParticleComp)
        particles = [particle for e, particle in ent_comp]
        CoulombCalc.charge_vectors(*particles)

        # I hope this doesn't bite me in the butt
        for e, particle in ent_comp:
            particle.general_vec = sum(particle.vecs, start=self.vec_zero)

            if not self.world.has_component(e, ArrowComp):
                self.world.add_component(e, ArrowComp(particle.self_vec, particle.general_vec, pygame.Color(0,0,255)))
            else:
                arrow = self.world.get_component(e, ArrowComp)
                arrow.vec_pos = particle.self_vec
                arrow.vec_point_to = particle.general_vec


class InitDrawParticles(ecs.System):
    def parameters(self, world: ecs.World) -> None:
        self.world = world

    def update(self) -> None:
        for e, (particle, renderables) in self.world.fast_query(ParticleComp, RenderablesComp):
            renderable = RenderableComp()
            
            renderable.surface = pygame.Surface((10,10))
            pygame.draw.circle(renderable.surface, (255,0,0), (5,5), 5)
            renderable.rect.center = particle.pos

            renderables.renderable.append(renderable)
            log(f'Initializing entity: {e}', tags=['Entities'])