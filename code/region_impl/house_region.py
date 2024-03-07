from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
from mcpi.block import Block

from region_impl.rooms import Rect, VisitedNodes, WallsNode, WallsGraph, mk_walls, mk_graph, dfs, divide_rect
from abstract_region import AbstractRegion

import util
import math
import random

# Block IDs
GLASS = 20
BRICK = 45
SANDSTONE = 24
WOOD_LOG = 17
MUSHROOM = 100
MOSS_STONE = 48
OBSIDIAN = 49
STONE_BRICKS = 98
MELON = 103
OAK_WOOD = 5
AIR = 0
BED = 26
TORCH = 50
BOOKSHELF = 47
FENCE = 85
STAIRS = 53
PRESSURE_PLATE = 72
CHEST = 54
FURNACE = 61
MIN_HOUSE_SPACING = 5

# A class for generating a generic cubic house


class HouseRegion(AbstractRegion):
    def generate(self, mc: Minecraft) -> bool:
        self.mc = mc

        self.bound1.y = mc.getHeight(self.bound1.x, self.bound1.z)
        self.pos = self.bound1 + Vec3(MIN_HOUSE_SPACING, 0, MIN_HOUSE_SPACING)
        x = abs(self.bound1.x - self.bound2.x) - MIN_HOUSE_SPACING
        z = abs(self.bound1.z - self.bound2.z) - MIN_HOUSE_SPACING

        self.size = Vec3(x, 6, z) - Vec3(MIN_HOUSE_SPACING,
                                         0, MIN_HOUSE_SPACING)
        self.rooms = divide_rect(
            Rect((self.pos.x, self.pos.z), self.size.x, self.size.z))
        self.door_pos = mk_graph(self.rooms)
        self.build()
        return True

    def get_door_loc(self) -> Vec3:
        return self.door_loc

    def build_one_floor(self):
        # Randomised building material
        building_mat = [BRICK, OAK_WOOD, SANDSTONE, WOOD_LOG,
                        OBSIDIAN, STONE_BRICKS, MUSHROOM, MOSS_STONE, MELON]
        building_mat_choice = random.choice(building_mat)
        roof_choice = random.choice(building_mat)

        # Randomised number of stories the house has
        number_of_stories = [1, 2, 3, 4]
        num_stories_choice = random.choice(number_of_stories)

        # The origin block starts inside the empty space of the corner in the room. The length and width does not include the walls, only the room inside.
        for room in self.rooms:
            o_x = room.origin[0]-1
            o_z = room.origin[1]-1
            e_x = o_x + room.width + 1
            e_z = o_z + room.length + 1

            for i in range(1, num_stories_choice+1):
                #  Tried Cubic loop but inefficient, therefore each line sets a wall of the room, completing the house
                self.mc.setBlocks(o_x, self.pos.y + (self.size.y*(i-1)), o_z, e_x,
                                  self.pos.y + (self.size.y*i), o_z, building_mat_choice)
                self.mc.setBlocks(o_x, self.pos.y + (self.size.y*(i-1)), e_z, e_x,
                                  self.pos.y + (self.size.y*i), e_z, building_mat_choice)
                self.mc.setBlocks(o_x, self.pos.y + (self.size.y*(i-1)), o_z, o_x,
                                  self.pos.y + (self.size.y*i), e_z, building_mat_choice)
                self.mc.setBlocks(e_x, self.pos.y + (self.size.y*(i-1)), o_z, e_x,
                                  self.pos.y + (self.size.y*i), e_z, building_mat_choice)
                if i == num_stories_choice:
                    # Ceiling
                    self.mc.setBlocks(self.pos.x-2, self.pos.y + (self.size.y*(i)) + 1, self.pos.z-2, self.pos.x +
                                      self.size.x + 1, self.pos.y + (self.size.y*(i)) + 1, self.pos.z + self.size.z + 1, roof_choice)
                    self.mc.setBlocks(self.pos.x-1, self.pos.y + (self.size.y*(i)) + 2, self.pos.z-1, self.pos.x +
                                      self.size.x, self.pos.y + (self.size.y*(i)) + 2, self.pos.z + self.size.z, roof_choice)
                # Floor
                self.mc.setBlocks(self.pos.x-1, self.pos.y + (self.size.y*(i-1)), self.pos.z-1, self.pos.x +
                                  self.size.x, self.pos.y + (self.size.y*(i-1)), self.pos.z + self.size.z, roof_choice)

        # Create doors to connect every room in the house
        visited = VisitedNodes(set())
        door_coords = []
        d_p = dfs(self.rooms[0], self.door_pos, visited, door_coords)
        for i in range(len(d_p)):
            self.mc.setBlock(d_p[i][0], self.pos.y+1, d_p[i][1], AIR)
            self.mc.setBlock(d_p[i][0], self.pos.y+2, d_p[i][1], AIR)

        # Add a torch above each door
            self.mc.setBlock(d_p[i][0], self.pos.y+3, d_p[i][1], 123)
            self.mc.setBlock(d_p[i][0], self.pos.y+4, d_p[i][1], 152)

        # Entrance to the house
        # Create a list of corners of the house
        house_corners = []
        # North-West North
        house_corners.append(Vec3(self.pos.x + 2, self.pos.y, self.pos.z-1))
        # North-West West
        house_corners.append(Vec3(self.pos.x, self.pos.y, self.pos.z+2-1))
        # North-East North
        house_corners.append(
            Vec3(self.pos.x + self.size.x - 2, self.pos.y, self.pos.z-1))
        # North-East East
        house_corners.append(
            Vec3(self.pos.x + self.size.x, self.pos.y, self.pos.z + 2-1))
        # South-West South
        house_corners.append(
            Vec3(self.pos.x + 2, self.pos.y, self.pos.z + self.size.z-1))
        # South-West West
        house_corners.append(
            Vec3(self.pos.x, self.pos.y, self.pos.z + self.size.z - 1-1))
        # South-East South
        house_corners.append(
            Vec3(self.pos.x + self.size.x - 2, self.pos.y, self.pos.z + self.size.z-1))
        # South-East East
        house_corners.append(
            Vec3(self.pos.x + self.size.x, self.pos.y, self.pos.z + self.size.z - 1-1))

        random_corner = random.choice(house_corners)
        self.door_loc = random_corner
        self.mc.setBlocks(random_corner.x, random_corner.y + 1, random_corner.z,
                          random_corner.x, random_corner.y + 2, random_corner.z, 0)
        # Making windows

        for i in range(0, 8, 2):
            if i == 0 or i == 2 or i == 4 or i == 6:
                self.mc.setBlocks(
                    house_corners[i].x+1, house_corners[i].y+2, house_corners[i].z, house_corners[i].x+1, house_corners[i].y+3, house_corners[i].z, GLASS)

    def clear_volume(self):
        self.mc.setBlocks(self.pos.x, self.pos.y, self.pos.z, self.pos.x +
                          self.size.x, self.pos.y + self.size.y, self.pos.z + self.size.z, AIR)

    def build(self):
        self.clear_volume()
        self.build_one_floor()
