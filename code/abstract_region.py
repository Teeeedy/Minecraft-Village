from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3

class AbstractRegion():
    def __init__(self, bound1 : Vec3, bound2 : Vec3):
        self.bound1 = bound1
        self.bound2 = bound2

    def __str__(self):
        return f'{self.bound1}, {self.bound2}'
        
    def generate(self, mc : Minecraft) -> bool:
        pass
