import mcpi.minecraft as minecraft
import mcpi.block as block

from dataclasses import dataclass
from random import randrange
from typing import List, Tuple, Set

import math
import random

MIN_ROOM_SIZE = 4


@dataclass
class Rect:
    origin: Tuple[int, int]
    width: int
    length: int


def divide_rect(rect: Rect, width: bool = True) -> List[Rect]:
    if rect.width <= MIN_ROOM_SIZE * 2 and rect.length <= MIN_ROOM_SIZE * 2:
        return [rect]
    if width:
        if rect.width <= MIN_ROOM_SIZE * 2:
            return divide_rect(rect, not width)
        sub = randrange(MIN_ROOM_SIZE, rect.width - MIN_ROOM_SIZE)
        r1 = Rect(rect.origin, sub, rect.length)
        r1_list = divide_rect(r1, not width)
        r2_orig = (rect.origin[0] + sub+1, rect.origin[1])
        r2 = Rect(r2_orig, rect.width - sub - 1, rect.length)
        r2_list = divide_rect(r2, not width)
        r1_list.extend(r2_list)
        return r1_list

    if rect.length <= MIN_ROOM_SIZE * 2:
        return divide_rect(rect, not width)
    sub = randrange(MIN_ROOM_SIZE, rect.length - MIN_ROOM_SIZE)
    r1 = Rect(rect.origin, rect.width, sub)
    r1_list = divide_rect(r1, not width)
    r2_orig = (rect.origin[0], rect.origin[1] + sub + 1)
    r2 = Rect(r2_orig, rect.width, rect.length - sub - 1)
    r2_list = divide_rect(r2, not width)
    r1_list.extend(r2_list)
    return r1_list


@dataclass
class WallsNode:
    idx: int
    walls: Set[Tuple[int, int]]
    children: Set[int]


@dataclass
class WallsGraph:
    nodes: List[WallsNode]


@dataclass
class VisitedNodes:
    visited: Set[int]


def mk_walls(room: Rect) -> Set[Tuple[int, int]]:
    o_x = room.origin[0] - 1
    o_z = room.origin[1] - 1
    e_x = o_x + room.width + 1
    e_z = o_z + room.length + 1
    rv = set((x, o_z) for x in range(o_x+1, e_x))
    rv |= set((x, e_z) for x in range(o_x+1, e_x))
    rv |= set((o_x, x) for x in range(o_z+1, e_z))
    rv |= set((e_x, x) for x in range(o_z+1, e_z))
    return rv


def mk_graph(rooms: List[Rect]) -> WallsGraph:
    walls = [mk_walls(x) for x in rooms]
    nodes = [WallsNode(i, x, set()) for i, x in enumerate(walls)]
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            if len(nodes[i].walls.intersection(nodes[j].walls)) != 0:
                nodes[i].children.add(j)
                nodes[j].children.add(i)
    return WallsGraph(nodes)


def dfs(node: WallsNode, graph: WallsGraph, visited: VisitedNodes, door_coords: List[Tuple[int, int]]):
    if len(visited.visited) == len(graph.nodes):
        return door_coords
    for node in graph.nodes:
        if node.idx not in visited.visited:
            visited.visited.add(node.idx)
            for i in node.children:
                visited.visited.add(i)
                x = node.walls.intersection(graph.nodes[i].walls)
                door_pos = random.choice(list(x))
                door_coords.append(door_pos)
            return dfs(node, graph, visited, door_coords)
