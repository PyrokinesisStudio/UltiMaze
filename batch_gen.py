"""
Batch tools for mazes

Available Functions:
    refresh_batch_max - Refreshes number of batch mazes by checking txt file
"""

import random
import time
import math
import os

import bpy

from maze_gen import prep_manager
from maze_gen import time_log
from maze_gen import auto_layout_gen
from maze_gen import txt_img_converter
from maze_gen import tile_maze_gen
from maze_gen import simple_maze_gen

def refresh_batch_max():
    """Refreshes number of batch mazes by checking txt file."""
    my_settings_dir = os.path.join(os.path.dirname(__file__), "settings")
    maze_setups_file = os.path.join(my_settings_dir, "maze_setups.txt")
    
    with open(maze_setups_file, "r") as s:
        settings_text = s.read()
    
    settings_text = settings_text.replace(" && ", "", 1)
    
    split_settings = settings_text.split(" && ")
    
    if settings_text == "":
        bpy.context.scene.num_batch_mazes = 0
    else:
        bpy.context.scene.num_batch_mazes = len(split_settings)
        

class StoreBatchMaze_MG(bpy.types.Operator):
    bl_label = "Store Settings"
    bl_idname = "scene.store_batch_maze"
    bl_description = "Stores a maze to batch generate."
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        wm = context.window_manager
        scene = context.scene
        
        settings_text = (" && wd,{};ht,{};3d,{};al,{};lc,{};ai,{}"
        ";fl,{};lm,{};wl,{}".format(
            scene.mg_width,
            scene.mg_height,
            int(scene.gen_3d_maze),
            int(scene.allow_loops),
            scene.loops_chance,
            int(scene.allow_islands),
            int(scene.use_list_maze),
            scene.list_maze,
            int(scene.write_list_maze)))
        print(settings_text)
       
        my_settings_dir = os.path.join(os.path.dirname(__file__), "settings")
        maze_setups_file = os.path.join(my_settings_dir, "maze_setups.txt")
        
        with open(maze_setups_file, "a") as s:
            s.write(settings_text)

        scene.num_batch_mazes += 1
        
        return {'FINISHED'}


class ClearBatchMazes_MG(bpy.types.Operator):
    bl_label = "Clear Mazes"
    bl_idname = "scene.clear_batch_maze"
    bl_description = "Clears all mazes from batch cache."
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        wm = context.window_manager
        scene = context.scene
        
        my_settings_dir = os.path.join(os.path.dirname(__file__), "settings")
        maze_setups_file = os.path.join(my_settings_dir, "maze_setups.txt")
        
        with open(maze_setups_file, "w") as s:
            s.write("")

        scene.num_batch_mazes = 0
        
        return {'FINISHED'}

class RefreshBatchMazes_MG(bpy.types.Operator):
    bl_label = "Refresh"
    bl_idname = "scene.refresh_batch_num"
    bl_description = "Refreshes number of batches."
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        wm = context.window_manager
        scene = context.scene

        refresh_batch_max()

        return {'FINISHED'}


class LoadBatchMaze_MG(bpy.types.Operator):
    bl_label = "Load Settings"
    bl_idname = "scene.load_batch_maze"
    bl_description = "Loads the maze settings for batch number."
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        wm = context.window_manager
        scene = context.scene
        
        refresh_batch_max()
        
        if scene.num_batch_mazes == 0:
            self.report({'ERROR'}, "No mazes stored!")
            return {'CANCELLED'}
        
        if scene.batch_index > scene.num_batch_mazes:
            scene.batch_index = scene.num_batch_mazes
            self.report({'ERROR'}, "Not a maze index! Setting to highest " +
                "batched maze number...")
            return {'CANCELLED'}
        
        my_settings_dir = os.path.join(os.path.dirname(__file__), "settings")
        maze_setups_file = os.path.join(my_settings_dir, "maze_setups.txt")
        
        with open(maze_setups_file, "r") as s:
            settings_text = s.read()
        
        settings_text = settings_text.replace(" && ", "", 1)
        
        split_settings = settings_text.split(" && ")
        
        maze_setup = split_settings[scene.batch_index - 1]

        maze_setup = maze_setup.split(";")
        
        for slot in maze_setup:
            parts = slot.split(",")

            if parts[0] == "wd":
                scene.mg_width = int(parts[1])
            elif parts[0] == "ht":
                scene.mg_height = int(parts[1])
            elif parts[0] == "3d":
                scene.gen_3d_maze = bool(int(parts[1]))
            elif parts[0] == "al":
                scene.allow_loops = bool(int(parts[1]))
            elif parts[0] == "lc":
                scene.loops_chance = int(parts[1])
            elif parts[0] == "ai":
                scene.allow_islands = bool(int(parts[1]))
            elif parts[0] == "fl":
                scene.use_list_maze = bool(int(parts[1]))
            elif parts[0] == "lm":
                scene.list_maze = parts[1]
            elif parts[0] == "wl":
                scene.write_list_maze = bool(int(parts[1]))
                    
        return {'FINISHED'}


class DeleteBatchMaze_MG(bpy.types.Operator):
    bl_label = "Delete Setting"
    bl_idname = "scene.delete_batch_maze"
    bl_description = "Deletes the maze settings for batch number."
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        wm = context.window_manager
        scene = context.scene
        
        refresh_batch_max()
        
        if scene.num_batch_mazes == 0:
            self.report({'ERROR'}, "No mazes stored!")
            return {'CANCELLED'}
        
        if scene.batch_index > scene.num_batch_mazes:
            scene.batch_index = scene.num_batch_mazes
            self.report({'ERROR'}, "Not a maze index! Setting to highest " +
                "batched maze number...")
            return {'CANCELLED'}
        
        
        # read text
        my_settings_dir = os.path.join(os.path.dirname(__file__), "settings")
        maze_setups_file = os.path.join(my_settings_dir, "maze_setups.txt")
        
        with open(maze_setups_file, "r") as s:
            settings_text = s.read()
        
        settings_text = settings_text.replace(" && ", "", 1)
        
        split_settings = settings_text.split(" && ")
                
        # delete setting
        del split_settings[scene.batch_index - 1]

        # create string
        new_settings_text = ""
        for i in split_settings:
            new_settings_text = new_settings_text + " && " + i
        
        # write out new text
        my_settings_dir = os.path.join(os.path.dirname(__file__), "settings")
        maze_setups_file = os.path.join(my_settings_dir, "maze_setups.txt")
        
        with open(maze_setups_file, "w") as s:
            s.write(new_settings_text)
        
        refresh_batch_max()
        
        return {'FINISHED'}


class BatchGenerateMaze_MG(bpy.types.Operator):
    bl_label = "Batch Generate"
    bl_idname = "scene.batch_generate_maze"
    bl_description = "Generates a maze for each stored setting."
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        wm = context.window_manager
        scene = context.scene
        
        my_settings_dir = os.path.join(os.path.dirname(__file__), "settings")
        maze_setups_file = os.path.join(my_settings_dir, "maze_setups.txt")
        
        with open(maze_setups_file, "r") as s:
            settings_text = s.read()
        
        settings_text = settings_text.replace(" && ", "", 1)
        
        split_settings = settings_text.split(" && ")
        
        # check for if no mazes are stored
        if split_settings[0] == "":
            self.report({'ERROR'},"No mazes stored! Click store settings to " +
                "store current maze settings.")
            return {'CANCELLED'}
        
        time_start = time.time()
        for maze_setup in split_settings:

            maze_setup = maze_setup.split(";")
            
            for slot in maze_setup:
                parts = slot.split(",")

                if parts[0] == "wd":
                    scene.mg_width = int(parts[1])
                elif parts[0] == "ht":
                    scene.mg_height = int(parts[1])
                elif parts[0] == "3d":
                    scene.gen_3d_maze = bool(int(parts[1]))
                elif parts[0] == "al":
                    scene.allow_loops = bool(int(parts[1]))
                elif parts[0] == "lc":
                    scene.loops_chance = int(parts[1])
                elif parts[0] == "ai":
                    scene.allow_islands = bool(int(parts[1]))
                elif parts[0] == "fl":
                    scene.use_list_maze = bool(int(parts[1]))
                elif parts[0] == "lm":
                    scene.list_maze = parts[1]
                elif parts[0] == "wl":
                    scene.write_list_maze = bool(int(parts[1]))
                    
            # GENERATE MAZE HERE
            tiles_exist = False

            if scene.tile_based and scene.gen_3d_maze:
                tiles_exist = prep_manager.check_tiles_exist()

                # if missing tiles: terminate operator
                if not tiles_exist:
                    self.report({'ERROR'},"One or more tile objects is missing " +
                        "or is not a mesh! Please assign a valid object or " +
                        "disable 'Use Modeled Tiles'.")
                    return {'CANCELLED'}

            if scene.use_list_maze:
                list_exist = prep_manager.check_list_exist()

                # if missing list: terminate operator
                if not list_exist:
                    self.report({'ERROR'},"List missing! Please assign a valid " +
                        "text data block or disable 'Generate Maze From List'.")
                    return {'CANCELLED'}
                
            # save files
            save_return, bad_file = prep_manager.always_save()
            if save_return == "BLEND_ERROR":
                self.report({'ERROR'}, "Save file or disable always save " +
                    "in user prefs.")
                return {'CANCELLED'}
            
            elif save_return == "IMAGE_ERROR":
                self.report({'ERROR'}, "Image '" + bad_file.name + 
                    "' does not have a valid file path (for saving). Assign " +
                    "a valid path, pack image, or disable save images in " +
                    "user prefs")
                return {'CANCELLED'}
            
            elif save_return == "TEXT_ERROR":
                self.report({'ERROR'}, "Text '" + bad_file.name + 
                    "' does not have a valid file path (for saving). " +
                    "Assign a valid path or disable save texts in user prefs")
                return {'CANCELLED'}
            
            if scene.use_list_maze:
                maze = txt_img_converter.convert_list_maze()
            elif scene.gen_3d_maze or scene.use_list_maze or scene.write_list_maze:
                maze = auto_layout_gen.make_list_maze()

            if scene.allow_loops:
                maze = auto_layout_gen.add_loops(maze)

            # 3D generation
            if bpy.context.scene.gen_3d_maze:
                
                if scene.tile_based:
                    tile_maze_gen.make_tile_maze(maze)
                else:
                    simple_maze_gen.make_3Dmaze(maze)
                    
            # log time
            if scene.gen_3d_maze:
                time_log.log_time(time.time() - time_start)
            
            if scene.gen_3d_maze or scene.write_list_maze:
                self.report({'INFO'},"Finished generating maze in "+
                    str(time.time() - time_start)+" seconds")

            # write list maze if enabled
            if scene.write_list_maze:
                text_block_name = txt_img_converter.str_list_maze(maze)
                self.report({'INFO'}, "See '"+str(text_block_name) + 
                    "' in the text editor")
        
        return {'FINISHED'}