import json
import utils.Algorithm as algo
import cv2
import utils.color_pallet_image_generator as cpig


ALGO = algo.Algorithm()
CPIG = cpig.image_generator()

class functinos:
    def read_unsolved_target_list_list(self):
        with open("src/database/unsolved_target_lists_random_shuffle.json","r") as json_file:
            data1 = json.load(json_file)
        return data1["unsolved_target_list_lists"]
    
    def read_patterns(self):
        with open("src/database/patterns.json","r") as json_file_1:
            data = json.load(json_file_1)
        puzzle_pattern = data["puzzle_pattern"]
        target_pattern = data["target_pattern"]
        return puzzle_pattern,target_pattern
    

    def solve_by_target_list(self,unsolved_target_list):
        puzzle_pattern,target_pattern= self.read_patterns()
        lock_positions = []
        blank_path_list = ALGO.solve_puzzle(puzzle_pattern,target_pattern,unsolved_target_list,lock_positions)
        return blank_path_list
    

    def visualize(self,WaitKey):
        # print("visualizing...")
        
        with open("src/database/final_path_dofbot.json","r") as json_file:
            data = json.load(json_file)
        blank_path_list = data["blank_path_list_final"]


        with open("src/database/patterns.json","r") as json_file:
            data = json.load(json_file)
        raw_target_pattern = data["raw_target_pattern"]
        original_puzzle_pattern = data["puzzle_pattern"]
        target_canvas = CPIG.generate_image(raw_target_pattern, 3)
        cv2.imshow("target_canvas",target_canvas)
        ALGO.puzzle_solve_step_by_step(blank_path_list,original_puzzle_pattern,WaitKey)
        # print("visualization_complete\n\n")


    def solving_lock_position_sequence(self, final_pattern):
        unsolved_target_list = [[0,0],[1,0],[2,0],
                            [0,1],[1,1],[2,1],
                            [0,2],[1,2],[2,2]]
        ind_list = []
        for element in final_pattern:
            ind = unsolved_target_list.index(element)
            ind_list.append(ind)
        
        return ind_list 
    
    def save_final_path(self, final_path_movements:list,blank_path_list_final:list)->list:
        """ Save final_path_dofbot in final_path_dofbot.json file and return final_paht_dofbot
        """
        final_path_dofbot = []
        cord_dict = {1: [0, 0], 2: [1, 0], 3: [2, 0], 4: [3, 0], 5: [4, 0], 6: [0, 1], 7: [1, 1], 8: [2, 1], 9: [3, 1], 10: [4, 1], 
                     11: [0, 2], 12: [1, 2], 13: [2, 2], 14: [3, 2], 15: [4, 2], 16: [0, 3], 17: [1, 3], 18: [2, 3], 19: [3, 3], 
                     20: [4, 3], 21: [0, 4], 22: [1, 4], 23: [2, 4], 24: [3, 4], 25: [4, 4]}
        def find_key(cord_dict, target_val):
            for key,val in cord_dict.items():
                if val == target_val:
                    return key
        for ele in final_path_movements:
            val1 = find_key(cord_dict, ele[0])    
            val2 = find_key(cord_dict, ele[1])
            final_path_dofbot.append([val1,val2])


        data = {
            "final_path_dofbot" : final_path_dofbot,
            "blank_path_list_final": blank_path_list_final
        }
        with open("src/database/final_path_dofbot.json","w") as json_file:
            print("loding data to final_path_dofbot")
            json.dump(data,json_file,indent=4)
            print("loded successfully")
        return final_path_dofbot


