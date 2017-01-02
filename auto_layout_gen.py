"""
Generates maze layout.

Available Functions:
    add_loops - Adds the ability to walk in circles by removing walls
    make_list_maze - Constructs a python list maze based on maze gen settings
"""

import random

import bpy
from maze_gen import maze_tools


def add_loops(maze):
    """Adds the ability to walk in circles by removing walls.

    Args:
        maze - python list in the format:
            [[(space in maze - x, y), is path, is walkable, active path],
            [(space in maze - x, y), is path, is walkable, active path], ...]

    Returns:
        updated maze
    """
    chance = bpy.context.scene.mg.loops_chance
    for row in range(maze.width):
        for column in range(maze.height):
            directions = maze.find_touching_path_dirs(row, column)
            if directions == ['N', 'S'] or directions == ['W', 'E']:
                random_num = random.randint(1, chance)
                if random_num == 1:
                    maze.make_path(row, column)
    return maze


def make_list_maze():
    """Constructs a python list maze based on maze gen settings.

    Returns:
        maze - python list in the format:
            [[(space in maze - x, y), is path],
            [(space in maze - x, y), is path], ...]
    """
    scene = bpy.context.scene
    mg = scene.mg
    x_dim = mg.mg_width
    y_dim = mg.mg_height
    debug = bpy.context.user_preferences.addons['maze_gen'].preferences.debug_mode

    if mg.algorithm == 'BREADTH_FIRST':
        m = maze_tools.BreadthFirstMaze(debug=debug,
                                        width=x_dim,
                                        height=y_dim,
                                        bias_direction=mg.bias_direction,
                                        bias=mg.bias)

    elif mg.algorithm == 'DEPTH_FIRST':
        m = maze_tools.DepthFirstMaze(debug=debug,
                                      width=x_dim,
                                      height=y_dim,
                                      bias_direction=mg.bias_direction,
                                      bias=mg.bias)

    elif mg.algorithm == 'PRIMS':
        m = maze_tools.PrimsMaze(debug=debug,
                                 width=x_dim,
                                 height=y_dim,
                                 bias_direction=mg.bias_direction,
                                 bias=mg.bias)

    elif mg.algorithm == 'BINARY_TREE':
        m = maze_tools.BinaryTreeMaze(debug=debug,
                                      width=x_dim,
                                      height=y_dim,
                                      directions=mg.binary_dir,
                                      tileable=mg.tileable)

    elif mg.algorithm == 'KRUSKALS':
        m = maze_tools.KruskalsMaze(debug=debug,
                                    width=x_dim,
                                    height=y_dim)

    elif mg.algorithm == 'ELLERS':
        m = maze_tools.EllersMaze(debug=debug,
                                  width=x_dim,
                                  height=y_dim,
                                  bias=mg.bias)

    maze = m.get()

    return maze
