import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from math import sqrt

def print_debug( *kargs, sep: str | None = " ", endl: str | None = "\n" ):
    if Config.debug is True:
        for i in kargs:
            print( i,end=sep )    
        print( end=endl )

class Config:
    k = 8.98755*10**9
    debug = False


class Particle:
    def __init__(self, q, pos : (int,int)):
        self.q = q
        self.pos = pos # X -> Y ->  Z
        self.vecs = []
        self.general_vec = pygame.math.Vector2(0, 0)
        self.self_vec = pygame.math.Vector2(self.pos[0], self.pos[1])


class Stat_Property:
    @staticmethod
    def law_coulomb(q1 : int|float, q2 : int|float, r : int|float, k = Config.k, F = None, absl:bool=True) -> float:
        if q1 != None and q2 != None and r != None and F == None: 
            print_debug( "Solving for F (force, Newtons): ", endl="" )
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
    def possibilities_law_coulomb(q1 : int|float, q2 : int|float, r : int|float, k = Config.k, F = None) -> float:
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
                print_debug( "Assuming that both charges are equal", endl="" )
            else:
                q = known_charges[0]
            
            print_debug( f"Solving for q (charge, Coulomb): ", endl="" )
            return (F*r**2)/(q*k)

        elif F != None and r == None and len(anon_charges) == 0: # we know everything but the distance
            print_debug( "Solving for r (distance, meters): ", endl="" )
            return sqrt( (k* abs(q1)* abs(q2))/F )
        
        else:                                                   # we know everything
            return Stat_Property.law_coulomb(q1=q1, q2=q2, r=r, k=k, F=F)    


    @staticmethod
    def choose_dist_calc(partcl1:Particle, partcl2:Particle) -> float:
        if len(partcl1.pos) > len(partcl2.pos) or len(partcl1.pos) < len(partcl2.pos):
            pass
        else:
            pass

    @staticmethod
    def distance_calc1(partcl1:Particle, partcl2:Particle) -> float:
        """One dimansion"""
        return partcl2.pos[0] - partcl1.pos[0]


    @staticmethod
    def distance_calc2(partcl1:Particle, partcl2:Particle) -> float:
        """Two dimensions"""
        return sqrt( (partcl2.pos[0] - partcl1.pos[0])**2 + (partcl2.pos[1] - partcl1.pos[1])**2 )


    @staticmethod
    def distance_calc3(partcl1:Particle, partcl2:Particle) -> float:
        """Three dimensions"""
        return sqrt( (partcl2.pos[0] - partcl1.pos[0])**2 + (partcl2.pos[1] - partcl1.pos[1])**2 + (partcl2.pos[2] - partcl1.pos[2])**2 )
    
    # vectors stuff

    @staticmethod
    def charge_vectors(*charges:Particle, k1:int|None=None)->None:
        k = k1 if k1 != None else Config.k

        temp_charges = charges
        secondary_charges = list(charges)
        for charge1 in temp_charges:
            for charge2 in temp_charges:
                if charge1 != charge2:
                    r = Stat_Property.distance_calc2(charge1,charge2)
                    F = Stat_Property.law_coulomb( charge1.q, charge2.q, r, k ,absl=False)
                    print(F)

                    # charge1 end of the vector charge 2 the start
                    temp_vec = charge1.self_vec - charge2.self_vec
                    print(temp_vec)
                    # vector scalars? (idk)
                    d = F/temp_vec.length()
                    print("distance: ",d)
                    # smt ig
                    new_vec1 = (d*(temp_vec))
                    new_vec2 = (-d*(temp_vec))
                    print(new_vec1,new_vec2)
                    charge1.vecs += [new_vec1]
                    charge2.vecs += [new_vec2]

            secondary_charges.pop(0)

    
    @staticmethod
    def general_vector(charge:Particle)->pygame.math.Vector2:
        temp_vec = pygame.math.Vector2(0,0)
        for vec in charge.vecs:
            temp_vec += vec
        print(temp_vec)
        return temp_vec

    @staticmethod
    def get_vectors(*charges:Particle, original_vec:bool=True):
        """
        Returns every vector with the added self vector.
        """
        temp_vecs = []
        for charge in charges:
            if original_vec:
                temp_vecs += [Stat_Property.general_vector(charge)+charge.self_vec] 
            else:
                temp_vecs += [Stat_Property.general_vector(charge)]
        return temp_vecs

class Property(Stat_Property):
    pass
            

def main():
    charge1 = Particle( 0.01*10**-6, (0,        4*10**-2))
    charge2 = Particle( 0.01*10**-6, (8*10**-2, 4*10**-2))
    charge3 = Particle( 0.02*10**-6, (4*10**-2, 4*10**-2))
    charge4 = Particle( 0.01*10**-6, (4*10**-2, 0))
    r = Stat_Property.distance_calc2(charge1,charge2)
    k = 9*10**9

    print( Stat_Property.law_coulomb( charge1.q, charge2.q, r, k ) )

    print( Stat_Property.possibilities_law_coulomb( charge1.q, charge2.q, None, k , k ) )

    Stat_Property.charge_vectors(charge1,charge2,charge3,charge4,k1=k)
    print(Stat_Property.get_vectors(charge1,charge2,charge3,charge4))
    print(Stat_Property.get_vectors(charge1,charge2,charge3,charge4, original_vec=False))


if __name__ == "__main__":
    main()

# 8987551787 what
