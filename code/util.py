import random

from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
from mcpi.block import Block

from abstract_region import AbstractRegion
from region_impl.region_map import RegionMap

debug_mode = True

def clear_chat(mc : Minecraft):
    if not debug_mode:
        return

    for i in range(0, 100):
        mc.postToChat(" ")

def debug_text(mc : Minecraft, val : str):
    if debug_mode:
        mc.postToChat(val)





def randInt(a : int, b : int) -> int:
    return random.randint(int(min(a, b)), int(max(a, b)))

def circlePerimLowest(mc : Minecraft, region : AbstractRegion, data : Block):
    for pos in get_perim(mc, region):
        mc.setBlock(pos.x, pos.y + 1, pos.z, data)

def vec3ListToTuple(list):
    tups = []
    for vec in list:
        if type(vec) == Vec3:
            tups.append( (vec.x, vec.y, vec.z) )
    return tups

def vec3_to_tuple(vec : Vec3):
    return (vec.x, vec.y, vec.z)


def get_region_minmax(region : AbstractRegion):
    bound1 = region.bound1
    bound2 = region.bound2
    
    minX = int(min(bound1.x, bound2.x))
    maxX = int(max(bound1.x, bound2.x))

    minZ = int(min(bound1.z, bound2.z))
    maxZ = int(max(bound1.z, bound2.z))

    return (minX, minZ, maxX, maxZ)

def within_bounds(pos : Vec3, region : AbstractRegion) -> bool:
    minX, minZ, maxX, maxZ = get_region_minmax(region)
    return not (pos.x > maxX or pos.x < minX or pos.z > maxZ or pos.z < minZ)

def reg_in_reg(reg1 : AbstractRegion, reg2 : AbstractRegion) -> bool:
    xAMin, zAMin, xAMax, zAMax= get_region_minmax(reg1)
    xBMin, zBMin, xBMax, zBMax= get_region_minmax(reg2)

    if ((xAMin >= xBMin and xAMin <= xBMax) or (xAMax >= xBMin and xAMax <= xBMax)
    or (zAMin >= zBMin and zAMin <= zBMax) or (zAMax >= zBMin and zAMax <= zBMax)):
      return True

    return False

def random_vec_in_region(region : AbstractRegion) -> tuple:
    minX, minZ, maxX, maxZ = get_region_minmax(region)
    x = randInt(minX, maxX)
    y = 0
    z = randInt(minZ, maxZ)
    return Vec3(x, y, z)

def get_perim(mc : Minecraft, region : AbstractRegion):
    positions = []
    minX, minZ, maxX, maxZ = get_region_minmax(region)
    height_map = get_heights_region(mc, region)

    for x in range(minX, maxX):
        for z in range(minZ, maxZ):
            if x == minX or x == maxX - 1 or z == minZ or z == maxZ - 1:
                y = height_map.get_val(x, z)
                positions.append(Vec3(x, y-1, z))
    return positions

def get_heights_region(mc : Minecraft, region : AbstractRegion) -> RegionMap:
    minX, minZ, maxX, maxZ = get_region_minmax(region)

    map = RegionMap()
    map.populateEmpty(abs(minX - maxX), 0)

    heights = mc.getHeights(minX, minZ, maxX, maxZ)


    index = 0
    for x in range(minX, maxX):
        for z in range(minZ, maxZ):
            map.set(x, z, heights[index])
            index = index + 1
    return map