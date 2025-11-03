import pygame

from src.tleng2 import *

from src.arrow_system import DrawArrow, DrawArrows 
from src.coulomb import CalculateForces, ParticleComp, InitDrawParticles

RendererMethods.load_displays()

EngineMethods.set_caption("Charges Visualizer - with multiple particles")

GlobalSettings._debug = True # it is False by default

world = ecs.World()

world.append_resources(
    DisplayCanvasComp(
        (1280,720)
    ),
    FpsComp(60)
)


particle1 = world.spawn(
    ParticleComp(0.01*10**-6, (10,5)),
    RenderablesComp()
)
particle2 = world.spawn(
    ParticleComp(0.01*10**-6, (100, 100)),
    RenderablesComp()
)
particle3 = world.spawn(
    ParticleComp(0.02*10**-6, (40, 40)),
    RenderablesComp()
)
particle4 = world.spawn(
    ParticleComp(0.01*10**-6, (40, 0)),
    RenderablesComp()
)

scheduler = ecs.Scheduler()

# Particle Renderable priority list.
# 0: Circle
# 1: Arrow
scheduler.add_init_systems(
    InitDrawParticles()
    
)

scheduler.add_systems(
    "Update",
    CalculateForces(),
    # DrawParticles(),
    DrawArrow(),
    DrawArrows()
)


main_scene = ecs.SceneComp(
    world,
    scheduler
)


def main():
    vis = App()

    vis.register_events(
        *events.default_events_bundle()
    )

    vis.use_plugins(
        tleng_base_plugin
    )

    vis.load_scenes(
        start_with="main_scene",
        main_scene=main_scene
    )

    vis.run()


if __name__ == '__main__':
    main()