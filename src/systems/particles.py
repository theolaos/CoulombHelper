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


class CalculateForces(ecs.System):
    def parameters(self, world: ecs.World) -> None:
        self.world = world
        # init type shi
        self.vec_zero = pygame.Vector2(0,0)

    def update(self) -> None:
        particles = [particle for e, particle in self.world.single_fast_query(ParticleComp)]
        Stat_Property.charge_vectors(*particles)

        for particle in particles:
            particle.general_vec = sum(particle.vecs, start=self.vec_zero)


class InitDrawParticles(ecs.System):
    def parameters(self, world: ecs.World) -> None:
        self.world = world

    def update(self) -> None:
        for e, (particle, renderables) in self.world.fast_query(ParticleComp, RenderablesComp):
            renderable = RenderableComp()
            
            renderable.surface = pygame.Surface((10,10))
            pygame.draw.circle(renderable.surface, (255,0,0), (5,5), 5)
            renderable.rect.topleft = particle.pos

            renderables.renderable.append(renderable)
            log(f'Initializing entity: {e}', tags=['Entities'])