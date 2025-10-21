import pygame
pygame.init()

from src.tleng2 import *

from src.arrow_system import Arrow, Arrows 
from src.coulomb import CalculateForces, ParticleComp

GlobalSettings.update_bresolution((1280,720))
RendererMethods.load_displays()

EngineMethods.set_caption("Coulomb Visualizer - with multiple particles")

GlobalSettings._debug = True # it is False by default

world = ecs.World()

world.append_resources(
    DisplayCanvasComp(
        (1280,720)
    )
)

particle1 = world.spawn(
    ParticleComp( 0.01*10**-6, (0,4*10**-2))
)
particle2 = world.spawn(
    ParticleComp( 0.01*10**-6, (8*10**-2, 4*10**-2))
)
particle3 = world.spawn(
    ParticleComp( 0.02*10**-6, (4*10**-2, 4*10**-2))
)
particle4 = world.spawn(
    ParticleComp( 0.01*10**-6, (4*10**-2, 0))
)

scheduler = ecs.Scheduler()

scheduler.add_systems(
    "Update",
    CalculateForces(),
    Arrow(),
    Arrows()
)


main_scene = ecs.SceneComp(
    world,
    scheduler
)


def main():
    vis = App()

    vis.use_plugins(
        tleng_base_plugin
    )

    vis.load_scenes(
        start_with="main_scene",
        main_scene=main_scene
    )

    vis.run()



if __name__ == '__main__':
    # simul = TlenGame({'main':Visualizer})
    # simul.on_init()
    # simul.run()
    main()