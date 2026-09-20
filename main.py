import pygame

from src.tleng2 import *
from src.log import *

from src.components import *
from src.systems import *

from src.coulomb import CoulombCalc, ParticleCalc

from src.constants import *


flush_log_file()

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
    ParticleComp(0.01*micro, (100,120)),
    RenderablesComp()
)

particle2 = world.spawn(
    ParticleComp(0.01*micro, (100, 100)),
    RenderablesComp()
)

particle3 = world.spawn(
    ParticleComp(0.02*micro, (40, 40)),
    RenderablesComp()
)

particle4 = world.spawn(
    ParticleComp(0.01*micro, (40, 20)),
    RenderablesComp()
)

scheduler = ecs.Scheduler()

# Particle Renderable priority list.
# 0: Circle
# 1: Arrow
scheduler.add_init_systems(
    InitDrawParticles(),
    CalculateForces(),
    DrawArrow()
)

scheduler.add_systems(
    "Update",
)


main_scene = ecs.SceneComp(
    world,
    scheduler
)


def main():
    sim = App()

    sim.register_events(
        *events.default_events_bundle()
    )

    sim.use_plugins(
        tleng_base_plugin
    )

    sim.load_scenes(
        start_with="main_scene",
        main_scene=main_scene
    )

    sim.run()


if __name__ == '__main__':
    main()