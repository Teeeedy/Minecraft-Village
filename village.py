# Assignment 1 main file
# Feel free to add additional modules/files as you see fit.

from mcpi.minecraft import Minecraft

mc = Minecraft.create()


x, y, z = mc.player.getPos()
width = 10
height = 5
depth = 8

mc.setBlocks(x, y, z, x+width, y+height, z+depth, 98)
mc.setBlocks(x+1, y, z+1, x+width-1, y+height-1, z+depth-1, 0)
mc.setBlocks(x, y-1, z, x+width, y-1, z+depth, 5)

for i in range(width):
    for j in range(depth):
        mc.setBlock(x+i, y+height+i/2, z+j, 126, 0)

mc.setBlocks(x+3, y+1, z, x+4, y+2, z, 20)
mc.setBlocks(x+width-4, y+1, z, x+width-3, y+2, z, 20)

mc.setBlock(x+1, y+1, z+height/2, 64, 0)
mc.setBlock(x+1, y+2, z+height/2, 64, 8)

mc.player.setPos(x+width/2, y+1, z+depth/2)
mc.player.setDirection(2)
mc.postToChat("House built!")
