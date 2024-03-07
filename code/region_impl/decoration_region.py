from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
from mcpi.block import Block

from abstract_region import AbstractRegion
import util

class DecorationRegion(AbstractRegion):
    def generate(self, mc : Minecraft) -> bool:
        num = util.randInt(1, 3)
        if num == 1:
            self.create_tree(self.bound1, mc)
        elif num == 2:
            self.create_flowerbed(self.bound1, mc)
        else:
            self.create_lamppost(self.bound1, mc)
        return True



    def create_tree(self, vec : Vec3, mc : Minecraft):
        block = util.vec3_to_tuple(vec)
        x,y,z = block

        mc.doCommand(f"setblock {int(x)} {int(y)} {int(z)} minecraft:oak_log")
        mc.doCommand(f"setblock {int(x)} {int(y+1)} {int(z)} minecraft:oak_log")
        mc.doCommand(f"setblock {int(x)} {int(y+2)} {int(z)} minecraft:oak_log")
        mc.doCommand(f"setblock {int(x)} {int(y+3)} {int(z)} minecraft:oak_log")
        mc.doCommand(f"setblock {int(x)} {int(y+4)} {int(z)} minecraft:oak_log")


        a,b,c = (x,y+4,z)
        for i in range(-1, 2):
            for j in range(-1,2):
                for k in range(-1,2):
                    mc.doCommand(f"setblock {int(a+j)} {int(b+i)} {int(c+k)} minecraft:oak_leaves")



        perimiter = set()

        for i in range(-1, 2):
            for j in range(-1, 2):
                perimiter.add((x+i, y, z+j))

        perimiter.remove((x,y,z))

        for block in perimiter:
            x,y,z = block
            mc.doCommand(f"setblock {int(x)} {int(y)} {int(z)} minecraft:barrel[facing=down]")

        lantern_block = perimiter.pop()
        x,y,z = lantern_block
        lantern_block = (x, y+1, z)
        mc.doCommand(f"setblock {int(x)} {int(y+1)} {int(z)} minecraft:lantern")


    def create_flowerbed(self, vec : Vec3, mc : Minecraft):
        block = util.vec3_to_tuple(vec)
        x,y,z = block

        fence = set()
        for i in range(-2, 3):
            for j in range(-2, 3):
                fence.add((x+i, y, z+j))

        
        for i in range(-1, 2):
            for j in range(-1, 2):
                fence.remove((x+i, y, z+j))


        for blocks in fence:
            x,y,z = blocks
            mc.doCommand(f"setblock {int(x)} {int(y)} {int(z)} minecraft:oak_fence")
            mc.doCommand(f"setblock {int(x)} {int(y-1)} {int(z)} minecraft:grass_block")


        x,y,z = block
        perimiter = set()

        for i in range(-1, 2):
            for j in range(-1, 2):
                perimiter.add((x+i, y, z+j))

        for blocks in perimiter:
            x,y,z = blocks
            flowers = ["minecraft:dandelion", "minecraft:poppy", "minecraft:blue_orchid", "minecraft:allium", "minecraft:azure_bluet", "minecraft:red_tulip", "minecraft:oxeye_daisy"]
            mc.doCommand(f"setblock {int(x)} {int(y-1)} {int(z)} minecraft:grass_block")
            mc.doCommand(f"setblock {int(x)} {int(y)} {int(z)} {flowers[util.randInt(0, len(flowers)-1)]}")



        
    def create_lamppost(self, vec : Vec3, mc : Minecraft):
        block = util.vec3_to_tuple(vec)
        x,y,z = block

        for i in range(0,8):
            mc.doCommand(f"setblock {int(x)} {int(y+i)} {int(z)} minecraft:oak_fence")

        mc.doCommand(f"setblock {int(x+1)} {int(y+i-1)} {int(z)} minecraft:lantern[hanging=true]")
        mc.doCommand(f"setblock {int(x-1)} {int(y+i-1)} {int(z)} minecraft:lantern[hanging=true]")
        mc.doCommand(f"setblock {int(x)} {int(y+i-1)} {int(z+1)} minecraft:lantern[hanging=true]")
        mc.doCommand(f"setblock {int(x)} {int(y+i-1)} {int(z-1)} minecraft:lantern[hanging=true]")

        mc.doCommand(f"setblock {int(x+1)} {int(y+i)} {int(z)} minecraft:oak_fence")
        mc.doCommand(f"setblock {int(x-1)} {int(y+i)} {int(z)} minecraft:oak_fence")
        mc.doCommand(f"setblock {int(x)} {int(y+i)} {int(z+1)} minecraft:oak_fence")
        mc.doCommand(f"setblock {int(x)} {int(y+i)} {int(z-1)} minecraft:oak_fence")

