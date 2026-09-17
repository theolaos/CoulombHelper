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

from dataclasses import dataclass, field

@dataclass
class ParticleComp:
    q: float
    pos: tuple[float, float]
    vecs: list[pygame.Vector2] = field(default_factory=list)
    general_vec: pygame.Vector2 = field(default_factory=lambda: pygame.math.Vector2)
    self_vec: pygame.Vector2 = field(default_factory=lambda: pygame.math.Vector2)
    
    def __post_init__(self) -> None:
        self.self_vec: pygame.Vector2 = pygame.math.Vector2(self.pos[0], self.pos[1])