from assets.scripts.engine.Tleng2 import *
#from assets.scripts.engine.settings import *


class Visualizer(Scene, GlobalSettings):
    def __init__(self):
        TlenGame.__init__(self)
        GlobalSettings.__init__(self)

    def on_init(self):
        '''
        Class objects, Entities, 
        '''
        self.charges = []

    def handle_events(self):
        '''
        the handling of basic events
        '''
        for event in pygame.event.get(): #optimazation (i think it can be written better)
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False

    
    def render(self):     
        self._win.fill((180,180,255))
        pygame.display.flip()
    
    def update(self):
        ...


if __name__ == '__main__':
    visualizer = Visualizer()
    visualizer.on_init()
    visualizer.run()