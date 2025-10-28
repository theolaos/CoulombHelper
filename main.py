import pygame

from src.tleng2 import *

from src.arrow_system import Arrow, Arrows 
from src.coulomb import CalculateForces, ParticleComp, DrawParticles

GlobalSettings.update_resolutions((1280,720), (1280,720))
RendererMethods.load_displays()

EngineMethods.set_caption("Coulomb Visualizer - with multiple particles")

GlobalSettings._debug = True # it is False by default

world = ecs.World()

world.append_resources(
    DisplayCanvasComp(
        (1280,720)
    ),
    FpsComp(60)
)




particle1 = world.spawn(
    ParticleComp( 0.01*10**-6, (10,5)),
    RenderableComp(
        pygame.Surface((10,10)),
        pygame.FRect(0,0,10,10)
    )
)
particle2 = world.spawn(
    ParticleComp( 0.01*10**-6, (-10, -10)),
RenderableComp(
    pygame.Surface((10,10)),
    pygame.FRect(0,0,10,10)
)
)
particle3 = world.spawn(
    ParticleComp( 0.02*10**-6, (40, 40)),
RenderableComp(
    pygame.Surface((10,10)),
    pygame.FRect(0,0,10,10)
)
)
particle4 = world.spawn(
    ParticleComp( 0.01*10**-6, (40, 0)),
RenderableComp(
    pygame.Surface((10,10)),
    pygame.FRect(0,0,10,10)
)
)

scheduler = ecs.Scheduler()

scheduler.add_systems(
    "Update",
    CalculateForces(),
    DrawParticles(),
    Arrow(),
    Arrows()
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