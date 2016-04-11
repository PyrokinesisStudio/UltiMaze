import os

import bpy


def log_time(elapsed_time):
    
    # get text from file
    my_settings_dir = os.path.join(os.path.dirname(__file__), "settings")
    time_log_file = os.path.join(my_settings_dir, "estimate_time_log.txt")
    
    with open(time_log_file, "r") as t:
        time_log = t.read()
    
    log_list = time_log.split(";")

    # delete the last one that gets created because of extra ";" at end
    del log_list[len(log_list) - 1]
    
    log_list += [str(bpy.context.scene.mg_width * 
        bpy.context.scene.mg_height) + "," + str(elapsed_time)]
    
    
    # convert into normal list
    i = 0
    for log in log_list:
        split_log = log.split(",")
        log_list[i] = (int(split_log[0]), float(split_log[1]))
        i += 1
    
    # sort
    log_list.sort()
    
    # average doubles
    i = 0
    for log in log_list:
        if log_list[i][0] == log_list[i-1][0]:
            
            log_list[i] = (log_list[i][0], (log_list[i][1] + 
                log_list[i-1][1]) / 2)
                
            del log_list[i-1]
        i += 1

    # convert to string
    str_log_list = ""
    i = 0
    for log in log_list:
        str_log_list = str_log_list + str(log[0]) + "," + str(log[1]) + ";"
        i += 1
        
    # write text to file
    with open(time_log_file, "w") as t:
        time_log_text.write(str_log_list)

 
def read_log_file():
    # get text from file
    my_settings_dir = os.path.join(os.path.dirname(__file__), "settings")
    time_log_file = os.path.join(my_settings_dir, "estimate_time_log.txt")
    
    with open(time_log_file, "r") as t:
        time_log = t.read()
    
    log_list = time_log.split(";")

    # delete the last one that gets created because of extra ";" at end
    del log_list[len(log_list) - 1]
    
    # convert into normal list
    i = 0
    for log in log_list:
        split_log = log.split(",")
        log_list[i] = (int(split_log[0]), float(split_log[1]))
        i += 1
        
    return log_list


# Time estimate
class EstimateTime_MG(bpy.types.Operator):
    bl_label = "Estimate Time"
    bl_idname = "object.estimate_time_mg"
    bl_description = ("Estimates the number of seconds the maze " +
        "generator will take")
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self,context):
        X_dim = context.scene.mg_width
        Y_dim = context.scene.mg_height
        estimated_loops = round((X_dim*Y_dim*1.25))
        self.report({'INFO'}, "Estimated Loops: " + str(estimated_loops) +
            " loops")

        # get log_list stored as [(size0, time0),(size1, time1),(size2, time2)]
        log_list = read_log_file()
        
        maze_size = X_dim * Y_dim
        
        # find logs that are closest and on either side of maze_size
        small_size = 8
        small_time = 0.01
        large_size = 1000001
        large_time = 300000
        for log in log_list:
            if log[0] == maze_size:
                small_size = log[0]
                small_time = log[1]
                large_size = log[0]
                large_time = log[1]
            elif log[0] < maze_size and log[0] > small_size:
                small_size = log[0]
                small_time = log[1]
            elif log[0] > maze_size and log[0] < large_size:
                large_size = log[0]
                large_time = log[1]
                
        # make sure large_size is not small size (div by 0 error)
        if large_size != small_size:
            maze_time = (small_time + (((maze_size - small_size) / 
                (large_size - small_size)) * (large_time - small_time)))
        else:
            maze_time = large_time
            
        time_est = (str(int(maze_time/3600)) + " hours, " + str(int((maze_time
            % 3600)/60)) + " minutes, " + str(int(maze_time % 60)) + 
            " seconds")
            
        self.report({'INFO'}, "Estimated Time: " + time_est)
        
        return {'FINISHED'}