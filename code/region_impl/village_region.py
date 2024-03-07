from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
from mcpi.block import Block

from abstract_region import AbstractRegion
from region_impl.house_region import HouseRegion
from region_impl.decoration_region import DecorationRegion
from typing import List, Tuple, Set

import util

MIN_VILLAGE_SIZE = 50
MAX_VILLAGE_SIZE = 150

MIN_DECOR_SIZE = 5
MAX_DECOR_SIZE = 5

MIN_HOUSE_SIZE = 10
MAX_HOUSE_SIZE = 30

HOUSE_DENSITY = 20
DECOR_DENSITY = 20

MAX_HOUSE_ATTEMPS = 50
MAX_DECOR_ATTEMPTS = 100
MAX_HEIGHT_DIFFERENCE = 3
MIN_HOUSE_SPACING = 5
MAX_HEIGHT_VIOLATIONS = 30

BORDER_BLOCK_ID = 103

class VillageRegion(AbstractRegion):

    #Constructor without region size
    #constructor will determine region size
    def __init__(self, *args):
        bound1 = None
        bound2 = None
        self.house_regions = []
        self.decor_regions = []
        self.town_center = None

        if(len(args) == 2):
            bound1 = args[0]
            bound2 = args[1]
        else:
            bound1 = None

        self.init(bound1, bound2)

    def init(self, bound1 : Vec3, bound2 : Vec3):
        super().__init__(bound1, bound2)

    #Returns all regions of town
    def getHouseRegions(self) -> List[HouseRegion]:
        return self.house_regions

    def getDecorRegions(self) -> List[DecorationRegion]:
        return self.decor_regions

    def getTownCenter(self) -> Vec3:
        return self.town_center

    def generate(self, mc: Minecraft) -> bool:
        center = mc.player.getPos()
        center.y = mc.getHeight(center.x, center.z)

        village_size = util.randInt(MIN_VILLAGE_SIZE, MAX_VILLAGE_SIZE)
        target_house_no = int(village_size/HOUSE_DENSITY)
        target_decor_no = int(village_size/DECOR_DENSITY)

        minX = center.x - village_size/2
        maxX = center.x + village_size/2

        minZ = center.z - village_size/2
        maxZ = center.z + village_size/2

        self.bound1 = Vec3(minX, 0, minZ)
        self.bound2 = Vec3(maxX, 0, maxZ)

        house_attempts = 0
        decor_attempts = 0
        cur_houses = []
        cur_decor = []

        #Generate houses

        while len(cur_houses) < target_house_no and house_attempts < MAX_HOUSE_ATTEMPS:
            house_attempts = house_attempts + 1

            rand_area = util.random_vec_in_region(self)

            house_size = util.randInt(MIN_HOUSE_SIZE + (MIN_HOUSE_SPACING * 2), MAX_HOUSE_SIZE + (MIN_HOUSE_SPACING * 2))

            region = HouseRegion(rand_area, rand_area + Vec3(house_size, 0, house_size))
            minX, minZ, maxX, maxZ = util.get_region_minmax(region)

            flagged = False
            #Check if bounds do not intercept with current houses
            for current_house in cur_houses:
                if(util.reg_in_reg(region, current_house)):
                    #House bounds are in
                    flagged = True

            if(flagged):
                continue

            #Ensure corners aren't on water
            corner1_height = mc.getHeight(minX, minZ)
            corner2_height = mc.getHeight(minX, maxZ)
            corner3_height = mc.getHeight(maxX, minZ)
            corner4_height = mc.getHeight(maxX, maxZ)

            corner1_block = mc.getBlock(minX, corner1_height, minZ)
            corner2_block = mc.getBlock(minX, corner2_height, maxZ)
            corner3_block = mc.getBlock(maxX, corner3_height, minZ)
            corner4_block = mc.getBlock(maxX, corner4_height, maxZ)

            if abs(corner1_height - corner2_height) > MAX_HEIGHT_DIFFERENCE:
                flagged = True

            if abs(corner1_height - corner3_height) > MAX_HEIGHT_DIFFERENCE:
                flagged = True

            if abs(corner1_height - corner4_height) > MAX_HEIGHT_DIFFERENCE:
                flagged = True

            blacklisted_blocks = [9,8]
            if corner1_block in blacklisted_blocks or corner2_block in blacklisted_blocks or corner3_block in blacklisted_blocks or corner4_block in blacklisted_blocks:
                flagged = True

            #check if flagged multiple times to avoid unecessary code execution
            if(flagged):
                continue
            
            if True:
                heights = util.get_heights_region(mc, region).val_list()
                avg_height = sum(heights) / len(heights)
                out_count = 0
                heightcnt = 0
                for height in heights:
                    heightcnt = heightcnt + 1
                    if height < avg_height - MAX_HEIGHT_DIFFERENCE:
                        out_count = out_count + 1
                print(out_count)

                if(out_count > MAX_HEIGHT_VIOLATIONS):
                    flagged = True

            if(flagged):
                continue

            #Clear area
            minY = min(mc.getHeight(minX, minZ), mc.getHeight(maxX, maxZ))
            #mc.setBlocks(minX, minY + 1, minZ, maxX, minY + 13, maxZ, 0)
            cur_houses.append(region)
            #util.circlePerimLowest(mc, region, BORDER_BLOCK_ID)

        #Generate decoration reigons
        decor_attempts = 0
        while len(cur_decor) < target_decor_no and decor_attempts < MAX_DECOR_ATTEMPTS:
            decor_attempts = decor_attempts + 1

            rand_area = util.random_vec_in_region(self)
            rand_area.y = mc.getHeight(rand_area.x, rand_area.z) + 1

            house_size = util.randInt(MIN_DECOR_SIZE, MAX_DECOR_SIZE)
            region = DecorationRegion(rand_area, rand_area + Vec3(house_size, 0, house_size))

            minX, minZ, maxX, maxZ = util.get_region_minmax(region)
            corner1_height = mc.getHeight(minX, minZ)
            corner2_height = mc.getHeight(minX, maxZ)
            corner3_height = mc.getHeight(maxX, minZ)
            corner4_height = mc.getHeight(maxX, maxZ)

            corner1_block = mc.getBlock(minX, corner1_height, minZ)
            corner2_block = mc.getBlock(minX, corner2_height, maxZ)
            corner3_block = mc.getBlock(maxX, corner3_height, minZ)
            corner4_block = mc.getBlock(maxX, corner4_height, maxZ)

            flagged = False
            blacklisted_blocks = [9,8]
            if corner1_block in blacklisted_blocks or corner2_block in blacklisted_blocks or corner3_block in blacklisted_blocks or corner4_block in blacklisted_blocks:
                flagged = True

            #Check if bounds do not intercept with current houses
            for current_house in cur_houses:
                if(util.reg_in_reg(region, current_house)):
                    #House bounds are in
                    flagged = True

            for current_region in cur_decor:
                if(util.reg_in_reg(region, current_region)):
                    #House bounds are in
                    flagged = True

            if(flagged):
                continue
            cur_decor.append(region)
        
        while not self.town_center:
            rand_area = util.random_vec_in_region(self)   

            flagged = False
            #Check if bounds do not intercept with current houses
            for current_house in cur_houses:
                if(util.within_bounds(rand_area, current_house)):
                    #House bounds are in
                    flagged = True

            for current_region in cur_decor:
                if(util.within_bounds(rand_area, current_region)):
                    #House bounds are in
                    flagged = True

            if(flagged):
                continue

            self.town_center = Vec3(rand_area.x, mc.getHeight(rand_area.x, rand_area.z), rand_area.z)


        self.house_regions = cur_houses
        self.decor_regions = cur_decor

        util.debug_text(mc, f'Village Size: {village_size}')
        util.debug_text(mc, f'Target house number: {target_house_no}')
        util.debug_text(mc, f'Decor Attempts: {decor_attempts}')
        util.debug_text(mc, f'House Attempts: {house_attempts}')
        util.debug_text(mc, f'Found: {len(cur_houses)}')
        return len(cur_houses) > 0 and len(cur_decor) > 0 and self.town_center
