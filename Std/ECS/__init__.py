from dataclasses import dataclass
from typing import Dict, Generic, TypeVar
T = TypeVar("T")

# Entity

@dataclass
class Entity:
    id: int

    def __hash__(self) -> int:
        return self.id

class EntityManager:
    next_id: int = 0

    def createEntity(self):
        id = self.next_id
        self.next_id += 1
        return Entity(id)

# Component

@dataclass
class Component:
    pass

class ComponentStorage(Generic[T]):
    def __init__(self):
        self.data: Dict[Entity, T] = {}
    
    def add(self, entity: Entity, component: T):
        self.data[entity] = component
    
    def get(self, entity: Entity):
        return self.data[entity]
    
    def has(self, entity: Entity):
        return entity in self.data
    
    def remove(self, entity: Entity):
        del self.data[entity]

# System

class System:
    required: tuple = ()

    def run(self, world, dt):
        raise NotImplementedError
