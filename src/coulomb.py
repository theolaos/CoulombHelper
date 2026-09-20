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
from dataclasses import dataclass, field

from .tleng2 import *
from .constants import *
from .log import *

from .components import ParticleComp


class ParticleCalc:
    @staticmethod
    def distance_calc1(partcl1: ParticleComp, partcl2: ParticleComp) -> float:
        """One dimansion"""
        return partcl2.pos[0] - partcl1.pos[0]


    @staticmethod
    def distance_calc2(partcl1: ParticleComp, partcl2: ParticleComp) -> float:
        """Two dimensions"""
        return sqrt( (partcl2.pos[0] - partcl1.pos[0])**2 + (partcl2.pos[1] - partcl1.pos[1])**2 )


    @staticmethod
    def distance_calc3(partcl1: ParticleComp, partcl2: ParticleComp) -> float:
        """Three dimensions"""
        return sqrt( (partcl2.pos[0] - partcl1.pos[0])**2 + (partcl2.pos[1] - partcl1.pos[1])**2 + (partcl2.pos[2] - partcl1.pos[2])**2 )


    @staticmethod
    def general_vector(charge: ParticleComp)->pygame.math.Vector2:
        temp_vec = pygame.math.Vector2(0,0)
        for vec in charge.vecs:
            temp_vec += vec
        log(temp_vec)
        return temp_vec


    @staticmethod
    def get_vectors(*charges: ParticleComp, original_vec: bool = True):
        """
        Returns every vector with the added self vector.
        """
        temp_vecs = []
        for charge in charges:
            if original_vec:
                temp_vecs += [ParticleCalc.general_vector(charge)+charge.self_vec] 
            else:
                temp_vecs += [ParticleCalc.general_vector(charge)]
        return temp_vecs
    

    @staticmethod
    def return_vectors_length(list_vecs):
        temp_list = []
        for vec in list_vecs:
            temp_list += [vec.length()]
        return temp_list



class CoulombCalc:
    @staticmethod
    def law_coulomb(
        q1: int | float, 
        q2: int | float, 
        r: int | float, 
        F = None, 
        absl: bool = True
    ) -> float:
        print("F", F)
        if q1 != None and q2 != None and r != None and F == None: 
            log( "Solving for F (force, Newtons): ")
            if absl:
                return ( k* abs(q1)* abs(q2) )/r**2 
            else:
                return ( k* q1* q2 )/r**2
        else:
            raise Exception(f"Something is missing: \n"+
                            f"->{q1 != None, q2 != None, r != None, F == None} \n" +
                            f"->{q1, q2 , r , F }\n" +
                             "->q1 != None and q2 != None and r != None and F == None")


    @staticmethod
    def possibilities_law_coulomb(
            q1: int|float, 
            q2: int|float, 
            r : int|float,  
            F = None
        ) -> float:
        anon_charges = []
        known_charges = []

        for q in (q1, q2):
            if q == None:
                anon_charges += [q]
            else:
                known_charges += [q]

        if F != None and len(anon_charges) > 0 and r != None: # we know everything but the charges
            if len(anon_charges) == 2:
                q = 2
                log("Assuming that both charges are equal")
            else:
                q = known_charges[0]
            
            log(f"Solving for q (charge, Coulomb): ")
            return (F*r**2)/(q*k)

        elif F != None and r == None and len(anon_charges) == 0: # we know everything but the distance
            log( "Solving for r (distance, meters): ")
            return sqrt( (k* abs(q1)* abs(q2))/F )
        
        else:                                                   # we know everything except the Force
            return CoulombCalc.law_coulomb(q1=q1, q2=q2, r=r, k=k, F=F)    


    @staticmethod
    def charge_vectors(*charges: ParticleComp) -> None:
        temp_charges = charges
        secondary_charges = list(charges)
        for charge1 in temp_charges:
            for charge2 in temp_charges:
                if charge1 != charge2:
                    r = ParticleCalc.distance_calc2(charge1,charge2) # optimization, same thing *
                    print("charge 1:", charge1)
                    print("charge 2:", charge2)
                    F = CoulombCalc.law_coulomb( charge1.q, charge2.q, r, absl=False)
                    # charge1 end of the vector charge 2 the start
                    temp_vec = charge1.self_vec - charge2.self_vec
                    # vector scalars? (idk)
                    d = F/temp_vec.length() # optimization, same thing *
                    # smt ig
                    new_vec1 = (d*(temp_vec))
                    new_vec2 = (-d*(temp_vec))
                    charge1.vecs += [new_vec1]
                    charge2.vecs += [new_vec2]

                    log(f"vector scalar: {d} \n" +
                                f"distance (r): {r}\n" +
                                f"force (f): {F}\n"+
                                f"temporal vector: {temp_vec}")
                    log(new_vec1,new_vec2)

            secondary_charges.pop(0)
