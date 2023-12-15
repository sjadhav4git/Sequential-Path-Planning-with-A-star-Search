#! /usr/bin/env python
import json
import utils.path_generator_rubiks as pg
import utils.path_point_list_generator as pplg
from tqdm import tqdm
'''
 Output : list of 3d point co-ordinates generator
 Tasks  : 1) Read data from database/final_path_dofbot.json
          

'''

class Path_Generate:
    def detailed_path_generate(self,z_touch:int,z_safe:int,dist:int):
        """
        This function generate all 3d points in sequence and store it in detaild_final_path.json
        """
        
        with open("src/database/final_path_dofbot.json",'r') as json_file:
            data = json.load(json_file)
        path_list = data["final_path_dofbot"]
        
        p_list = []
        all_points = pplg.tot_point_list_generate(pg.pt_list(path_list,z_touch,z_safe),dist)
        progress_bar = tqdm(total=len(all_points), desc=("Detailed path genrating with resolution {} mm".format(dist)))
        for pl in all_points:
            p_list.append([round(pt,2) for pt in pl])
            progress_bar.update(1)
        progress_bar.close()

        data ={
            "final_path":p_list
        }

        json_data = json.dumps(data,indent=4)
        with open("src/database/detailed_final_path.json","w") as json_file:
            print("\nFrom : src/dofbot_controller_original_copy/detailed_final_path_gerator.py")
            print("writing_data to detailed_final path")
            json_file.write(json_data)
            print("detailed_final_path (all 3d locations) ready.\nTotal_point: ",len(p_list))




# dist = 5  # distance between two consecutive points in mm
# z_safe = 35
# z_touch = 10

# PG = Path_Generate()
# PG.detailed_path_generate(z_touch,z_safe,dist)

