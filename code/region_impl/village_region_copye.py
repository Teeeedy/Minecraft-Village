from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
from mcpi.block import Block

from abstract_region import AbstractRegion
from region_impl.region_map import RegionMap

import util
import math
import sys

#Constants
VILLAGE_SCALING_FACTOR_MIN = 10
VILLAGE_SCALING_FACOTR_MAX = 15

MIN_HOUSE_SIZE = 10
SCALING_FACTOR_MIN = 3
SCALING_FACTOR_MAX = 7

SPACING_FACTOR_MIN = 5
SPACING_FACTOR_MAX = 7

REGION_ITERATOR_SIZE = 16

MAXIMUM_BOUND_ATTEMPTS = 50
BORDER_BLOCK_ID = 103

class VillageRegion(AbstractRegion):

    #Constructor without region size
    #constructor will determine region size
    def __init__(self, *args):
        bound1 = None
        bound2 = None
        self.house_regions = []

        if(len(args) == 2):
            bound1 = args[0]
            bound2 = args[1]
        else:
            bound1 = None

        self.init(bound1, bound2)

    def init(self, bound1 : Vec3, bound2 : Vec3):
        super().__init__(bound1, bound2)
        self.scaling_factor = util.randInt(SCALING_FACTOR_MIN, SCALING_FACTOR_MAX)
        self.spacing_factor = util.randInt(SPACING_FACTOR_MIN, SPACING_FACTOR_MAX)
        self.village_scaling_factor = util.randInt(VILLAGE_SCALING_FACTOR_MIN, VILLAGE_SCALING_FACOTR_MAX)

    #Returns all regions of town
    def getHouseRegions(self):
        return self.house_regions

    def generate(self, mc: Minecraft) -> bool:
        util.debug_text(mc, "Village Generating...")
        util.debug_text(mc, f'Village Bound 1: {util.vec3_to_str(self.bound1)}')
        util.debug_text(mc, f'Village Bound 2: {util.vec3_to_str(self.bound2)}')
        util.debug_text(mc, '')

        player_pos = mc.player.getPos()
        util.debug_text(mc, f'Player Position: {util.vec3_to_str(player_pos)}')
        util.debug_text(mc, '')

        util.debug_text(mc, f'Village Scaling Factor: {self.village_scaling_factor}')
        util.debug_text(mc, f'Building Scaling Factor: {self.scaling_factor}')
        util.debug_text(mc, f'Buidling Spacing Factor: {self.spacing_factor}')
        
        target_block_size = (self.scaling_factor * self.village_scaling_factor) ** 2
        util.debug_text(mc, '')
        util.debug_text(mc, f'Target Block Size: {target_block_size}')

        #TODO: Marching cubes to find village area
        #Take into account average height of area and whether it is suitable to build on

        region_map = RegionMap()

        highest_y = mc.getHeight(player_pos.x, player_pos.z)
        highest_y_offset = mc.getHeight(player_pos.x + REGION_ITERATOR_SIZE, player_pos.z + REGION_ITERATOR_SIZE)

        bound1 = Vec3(player_pos.x                       , highest_y + 1       , player_pos.z)
        bound2 = Vec3(player_pos.x + REGION_ITERATOR_SIZE, highest_y_offset + 1, player_pos.z + REGION_ITERATOR_SIZE)

        reg = AbstractRegion(bound1, bound2)
        #util.circlePerimLowest(mc, reg.bound1, reg.bound2, BORDER_BLOCK_ID)
        
        region_map.set(0, 0, reg)

        target_bound_areas = target_block_size/REGION_ITERATOR_SIZE
        targed_bound_areas_sqr = int(math.sqrt(target_bound_areas))
        util.debug_text(mc, '')
        util.debug_text(mc, f'Target bound areas: {target_bound_areas}')
        util.debug_text(mc, f'Target bound areas sqr: {int(targed_bound_areas_sqr/2)}')
        util.debug_text(mc, '')

        region_map.populateEmpty(int(targed_bound_areas_sqr/2))
        #region_map.display()

        reg_arr = region_map.asArray()

        maxAreaX = -sys.maxsize
        minAreaX = sys.maxsize
        maxAreaZ = -sys.maxsize
        minAreaZ = sys.maxsize

        try:
            for k, v in util.circle_around(reg_arr):
                x, z = v
                #Determine whether bounding area is suitable for village
                bound_area_1 = Vec3(bound1.x + (REGION_ITERATOR_SIZE * (x + 0)), player_pos.y, bound1.z + (REGION_ITERATOR_SIZE * (z + 0) ))
                bound_area_2 = Vec3(bound1.x + (REGION_ITERATOR_SIZE * (x + 1)), player_pos.y, bound1.z + (REGION_ITERATOR_SIZE * (z + 1) ))

                #util.circlePerim(mc, bound_area_1, bound_area_2, BORDER_BLOCK_ID)
                reg_arr[x][z] = "X"
                #print(*reg_arr, sep=",\n")
                minX = int(min(bound_area_1.x, bound_area_2.x))
                maxX = int(max(bound_area_1.x, bound_area_2.x))

                minZ = int(min(bound_area_1.z, bound_area_2.z))
                maxZ = int(max(bound_area_1.z, bound_area_2.z))

                maxAreaX = int(max(bound_area_1.x, maxAreaX))
                maxAreaX = int(max(bound_area_2.x, maxAreaX))
                minAreaX = int(min(bound_area_1.x, minAreaX))
                minAreaX = int(min(bound_area_2.x, minAreaX))

                maxAreaZ = int(max(bound_area_1.z, maxAreaZ))
                maxAreaZ = int(max(bound_area_2.z, maxAreaZ))
                minAreaZ = int(min(bound_area_1.z, minAreaZ))
                minAreaZ = int(min(bound_area_2.z, minAreaZ))

                y = mc.getHeight(bound_area_1.x, bound_area_1.z)
                subsect = mc.getBlocks(bound_area_1.x, y - 5, bound_area_1.z, bound_area_2.x, y + 5, bound_area_2.z)
                mc.getHeights
                #Check subsect  
        except IndexError:
            #Spiral algorith has finished
            #print("finished")   
            pass

        cur_regions = []
        tries = 0
        while len(cur_regions) < self.village_scaling_factor and tries < MAXIMUM_BOUND_ATTEMPTS + self.village_scaling_factor:
            tries = tries + 1
            #define house region
            rand_area = util.random_vec_in(Vec3(maxAreaX, 0, maxAreaZ), Vec3(minAreaX, 0 ,minAreaZ))
            house_size = util.randInt(MIN_HOUSE_SIZE, MIN_HOUSE_SIZE + self.scaling_factor)

            flagged = False
            for region in cur_regions:
                util.debug_text(mc, "Finding region")
                util.debug_text(mc, rand_area)
                util.debug_text(mc, region)
                reg = AbstractRegion(rand_area, rand_area + Vec3(house_size, 0, house_size))
                if util.bound_in_bound(reg, region):
                    flagged = True

                corner1 = Vec3(maxAreaX, mc.getHeight(maxAreaX, maxAreaZ), maxAreaZ)
                corner2 = Vec3(minAreaX, mc.getHeight(minAreaX, minAreaZ), minAreaZ)

                block1 = mc.getBlock(corner1.x, corner1.y, corner1.z)
                block2 = mc.getBlock(corner2.x, corner2.y, corner2.z)
                if(block1 == 9 or block2 == 9):
                    #block is water
                    flagged = True

            
            if not flagged:
                region = AbstractRegion(rand_area, rand_area + Vec3(house_size, 0, house_size))
                cur_regions.append(region)
                util.circlePerimLowest(mc, region.bound1, region.bound2, BORDER_BLOCK_ID)

        #clear bound
        for reg in cur_regions:
                bound1 = reg.bound1
                bound2 = reg.bound2
                minX = int(min(bound1.x, bound2.x))
                maxX = int(max(bound1.x, bound2.x))

                minZ = int(min(bound1.z, bound2.z))
                maxZ = int(max(bound1.z, bound2.z))

                heights = mc.getHeights(maxX, maxZ, minX, minZ)
                avg = sum(heights) / len(heights)
                #mc.setBlocks(minX, avg, minZ, maxX, avg + 13, maxZ, 0)


        self.house_regions = cur_regions
        #util.debug_text(mc, f'Region Size: {(len(bound_regions) * REGION_ITERATOR_SIZE) ** 2}')

        util.debug_text(mc, f'Successfully Generated {len(self.house_regions)} regions.')


        return True
