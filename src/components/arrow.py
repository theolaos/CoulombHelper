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
class ArrowComp:
    vec_pos: pygame.Vector2
    vec_point_to: pygame.Vector2
    color: pygame.Color
    body_width: int = 3
    head_width: int = 15
    head_height: int = 15

@dataclass
class ArrowsComp:
    list_of_arrows: list