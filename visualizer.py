from src.config import *
from src.coulomb import *

class Property_visualization(Stat_Property):
    """
    Abstracting the visualization part:
    """
    def __init__(self, *list_charges:Particle) -> None:
        self.charges = list_charges
        

"""
Arrow:
Polygon consisting of Vectors for ArrowHead
    Bcz arrowhead is from vectors you are able to custumize it.
        - inward arrow
        - default arrow
        - stick arrow (line)
        
Polygon consisting of Vectors for ArrowBody
    Options as well?
        -line
        -polygon
        -shape for the start of arrow

***Also because they are polygons we can AntiAlias them (Expiremental, from the gfxdraw library of pygame)***

Get position of mouse, rotate HeadPolygon to Mouse and rotate BodyPolygon to Mouse

add both byproducts of the rotation to get the final arrow! 

"""

