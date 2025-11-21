from .ECS import *
class Scene:
    EM: EntityManager
    def __init__(self):
        self.storages = {}
        self.systems = []
        self.EM = EntityManager()
    
    def createEntity(self):
        return self.EM.createEntity()

    def registerComponentType(self, ct):
        self.storages[ct] = ComponentStorage()
    
    def addComponent(self, e: Entity, c: Component):
        ct = type(c)
        self.storages[ct].add(e, c)
    
    def storage(self, ct):
        return self.storages[ct]

    def addSystem(self, system: System):
        self.systems.append(system)
    
    def update(self, dt):
        for s in self.systems:
            s.run(self, dt)
