from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3

import random
import heapq
import math
import util

from abstract_region import AbstractRegion

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return not self.elements
    
    def put(self, node, priority):
        heapq.heappush(self.elements, (priority, node))
    
    def get(self):
        return heapq.heappop(self.elements)[1]
    
class PathRegion(AbstractRegion):
    def generate(self, mc : Minecraft) -> bool:
        self.mc = mc
        self.A_star(self.bound1, self.bound2, self.unpassableArea)
        return True

    def __init__(self, bound1 : Vec3, bound2 : Vec3, unpassableArea):
        super().__init__(bound1, bound2)
        self.unpassableArea = unpassableArea
        

    # This A_star function was designed very similar to the one on Implementation of A* from Red Blob Games
    # But it is modified to suit our needs in minecraft 
    # https://www.redblobgames.com/pathfinding/a-star/implementation.html

    def A_star(self, startVec : Vec3, endVec : Vec3, unpassableArea):

        unpassableArea = util.vec3ListToTuple(unpassableArea)
        startNode = (int(startVec.x), int(startVec.y), int(startVec.z))
        goalNode = (int(endVec.x), int(endVec.y), int(endVec.z))

        frontier = PriorityQueue()
        frontier.put(startNode, 0)
        came_from = {}
        cost_so_far = {}
        came_from[startNode] = None
        cost_so_far[startNode] = 0
        
        
        

        while not frontier.empty():
            current = frontier.get()
            

            # This is just for debug purposes
            x,y,z = current
            #self.mc.setBlock(x, y, z, 35, random.randint(0,15))

            if current == goalNode:
                print('success')
                path = self.reconstruct_path(came_from, startNode, goalNode)
                self.build_road(path, 208, unpassableArea)
                break

            

            for next in self.neighbours(current):
                x,y,z = next

                # These are the unpassable block ids like water
                unpassableTypes = [8, 18, 10, 80]

                # If the neighbour block is in restricted area skip to next neighbour
                if next in unpassableArea:
                    continue

                # This is to check what block id it is
                # if mc.getBlock(x,y,z) in unpassableTypes:
                #     continue

                
                new_cost = cost_so_far[current] + self.movement_cost(current, next)
                
                
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.h(next, goalNode)
                    frontier.put(next, priority)
                    came_from[next] = current
    

    
    # Debug messages
    # print('failed')
    # print(frontier.empty())
    # print('-------------------------------------------')

    # This is just the queue for the A_star algorithm 
    # This queue was designed from Implementation of A* from Red Blob Games
    # https://www.redblobgames.com/pathfinding/a-star/implementation.html

    # Gets the highest blocks around target block depending on the specified area (width = x, height = z)
    def map(self, node, length, width):
        x,y,z = node
        height_map = self.mc.getHeights(x+length,z+width,x-length,z-width)

        result = set()

        count = 0
    # code for statespace
        
        for i in range(x-length, x+(length+1)):
            for j in range(z-width, z+(width+1)):
                result.add((i, height_map[count], j))
                count+=1

        return result



    # This is the heuristic for the A_star algorithm. 
    # We use the Euclidean distance heuristic for this
    def h(self, nodeA, nodeB):
        x1,y1,z1 = nodeA
        x2,y2,z2 = nodeB
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        dz = abs(z1 - z2)
        D = 1

        
        # Euclidean distance heuristic
        return math.sqrt(dx * dx + dz * dz + dy * dy) 


    # This is the cost of moving from one block to another
    # Made it so that moving to a higher block will take more effort
    def movement_cost(self, nodeA, nodeB):
        x1,y1,z1 = nodeA
        x2,y2,z2 = nodeB

        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        dz = abs(z1 - z2)

    # Chebyshev distance
        return dy * dy * max(dx,dz)

        


    def neighbours(self, node):

        # # this is the code with mc.getHeights as the neighbours

        x,y,z = node
        

        surrNodes = set()

        neighbours = self.map(node, 1, 1)

        neighbours.remove((x,self.mc.getHeight(x,z),z))
        

        for node in neighbours:
            surrNodes.add(node)


        return surrNodes




    # This reoncstruct_path function was designed from Implementation of A* from Red Blob Games
    # https://www.redblobgames.com/pathfinding/a-star/implementation.html
    def reconstruct_path(self, came_from, startNode, goalNode):
        current = goalNode
        path = []

        if goalNode not in came_from:
            return []
        
        while current != startNode:
            path.append(current)
            current = came_from[current]
        
        return path



    # Function to build a road with block of choice
    def build_road(self, path, blockOfChoice, unpassableArea):
        # Removes the goal block from the road generation
        path.pop(0)
        path.pop(0)

        # Building the road
        for node in path:
            x,y,z = node
            for i in range(x-1, x+2):
                for j in range(z-1, z+2):
                    # If the block is in a restricted area do not change
                    if (i,y,j) in unpassableArea:
                        continue
                    
                    self.mc.setBlock(i,y,j,blockOfChoice)
                    self.mc.setBlock(i,y+1,j,0)
                    self.mc.setBlock(i,y+2,j,0)
                    self.mc.setBlock(i,y+3,j,0)

                    # This code is just to build the supports for the path if it has to go in the air or over water
                    # Block id 98 is stone brick
                    self.mc.setBlock(i,y-1,j,98)
                    self.mc.setBlock(i,y-2,j,98)
                    self.mc.setBlock(i,y-3,j,98)
                    self.mc.setBlock(i,y-4,j,98)
                    self.mc.setBlock(i,y-5,j,98)
                    self.mc.setBlock(i,y-6,j,98)
                    self.mc.setBlock(i,y-7,j,98)
                    self.mc.setBlock(i,y-8,j,98)
                    self.mc.setBlock(i,y-9,j,98)
                    self.mc.setBlock(i,y-10,j,98)
                    self.mc.setBlock(i,y-11,j,98)
                    self.mc.setBlock(i,y-12,j,98)
            
