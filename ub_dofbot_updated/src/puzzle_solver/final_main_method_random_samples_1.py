
import utils.Algorithm as Algorithm
import time
import utils.unsolved_list_list_creator_random_with_shuffle as random_unsolved_shuffle
import json
import cv2
import utils.color_pallet_image_generator as cpig
from tqdm import tqdm

ALGO = Algorithm.Algorithm()
CPIG = cpig.image_generator()

class functions:
    def __init__(self):
        pass


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
    

    def solving_lock_position_sequence(self, final_pattern):
        unsolved_target_list = [[0,0],[1,0],[2,0],
                            [0,1],[1,1],[2,1],
                            [0,2],[1,2],[2,2]]
        ind_list = []
        for element in final_pattern:
            ind = unsolved_target_list.index(element)
            ind_list.append(ind)
        
        return ind_list 


    def save_final_path(self, optimised_path,blank_path_list_final):
        """ Save final_path_dofbot in final_path_dofbot.json file and return final_paht_dofbot
        """
        final_path_dofbot = []
        cord_dict = {1: [0, 0], 2: [1, 0], 3: [2, 0], 4: [3, 0], 5: [4, 0], 6: [0, 1], 7: [1, 1], 8: [2, 1], 9: [3, 1], 10: [4, 1], 
                     11: [0, 2], 12: [1, 2], 13: [2, 2], 14: [3, 2], 15: [4, 2], 16: [0, 3], 17: [1, 3], 18: [2, 3], 19: [3, 3], 
                     20: [4, 3], 21: [0, 4], 22: [1, 4], 23: [2, 4], 24: [3, 4], 25: [4, 4]}
        def find_key(cord_dict, target_val):
            for key,val in cord_dict.items():
                if val[0] == target_val[0] and val[1] == target_val[1]:
                    return key
        for ele in optimised_path:
            key1 = find_key(cord_dict, ele[0])    
            key2 = find_key(cord_dict, ele[1])
            final_path_dofbot.append((key1, key2))


        data = {
            "final_path_dofbot" : final_path_dofbot,
            "blank_path_list_final": blank_path_list_final
        }
        with open("src/database/final_path_dofbot.json","w") as json_file:
            print("loding data to final_path_dofbot")
            json.dump(data,json_file,indent=4)
            print("loded successfully")
        return final_path_dofbot

    def save_final_path_new(self, optimised_path,blank_path_list_final):
        """ Save final_path_dofbot in final_path_dofbot.json file and return final_paht_dofbot
        """
        final_path_dofbot = optimised_path
        data = {
            "final_path_dofbot" : final_path_dofbot,
            "blank_path_list_final": blank_path_list_final
        }
        with open("src/database/final_path_dofbot.json","w") as json_file:
            print("loding data to final_path_dofbot\n...")
            json.dump(data,json_file,indent=4)
            print("loded successfully")
        return final_path_dofbot
    

FUN = functions()


class solver:    
    def __init__(self):
        pass


    def generate_samples(self,itr):
        """ Run this function to generate random solving sequences.
        """
        iteration = itr
        # waitKey = 50
        RANDOM_SHUFFLE = random_unsolved_shuffle.random_unsolved()
        RANDOM_SHUFFLE.random_n_generate(iteration)
        print("\n\nwith {} radnom samples".format(iteration))


    def solve_final(self,itr):
        """
        USE next function solve_final_optimized....
        """
        """
        Solve puzzle and visualize the movements and save the movement co-ordinates to ffinal_path_dofbot.json
        """
        self.generate_samples(itr)
        start_time  = time.time()
        print("Start_solving\nwait...")
        unsolved_target_list_list_selected = FUN.read_unsolved_target_list_list()
        individual_no_of_steps = []
        grouped_no_of_steps = []
        indexes = []
        for i in range(itr):
            unsolved_target_list = unsolved_target_list_list_selected[i]
            lock_position_sequence = FUN.solving_lock_position_sequence(unsolved_target_list)
            try:
                blank_path_list = FUN.solve_by_target_list(unsolved_target_list)
                grouped_blank_path = ALGO.slicer(blank_path_list)
                individual_no_of_steps.append(len(blank_path_list))
                grouped_no_of_steps.append(len(grouped_blank_path))
                indexes.append(i)    
            except:
                if i == 0:
                    blank_path_list = [i for i in range(500)]
                    grouped_blank_path = [i for i in range(500)]
                pass
            
            if i > 0:
                current_len = len(grouped_blank_path)
                if current_len < previous_len:
                    index_stored = i
                    previous_len = current_len
                    final_LCP = lock_position_sequence
                    blank_path_list_final = blank_path_list
                    optimized_path = grouped_blank_path
            else:
                index_stored = i
                current_len = len(grouped_blank_path)   
                previous_len = current_len
                final_LCP = lock_position_sequence
                blank_path_list_final = blank_path_list
                optimized_path = grouped_blank_path
                

        total_search_time = time.time() - start_time
        if total_search_time > 60:
            minutes = total_search_time/60
            print("total searching time\t\t\t\t\t", round(minutes,2), "min")
        else:
            print("total searching time\t\t\t\t\t", round(total_search_time,2), "sec")
        
        
        # save final path in co-ordinate format to final_path_dofbot.json
        final_path_dofbot_cords = ALGO.movement_list_maker_for_dofbot(blank_path_list,optimized_path)
        print("\nsrc/puzzle_solver/final_main_method_random_samples")
        print("blank_path_list: ",blank_path_list,"\nlen ",len(blank_path_list))
        print("\noptimized_path_indexes", optimized_path)
        print("\nfinal_path_dofbot_cords: ",final_path_dofbot_cords)
        print()

        final_path_dofbot_json = FUN.save_final_path(final_path_dofbot_cords, blank_path_list_final)
        print("\nfinal_path_dofbot_json :",final_path_dofbot_json)

        print("total_combinations_checked {} ".format(itr))
        print("least number of steps at index {} are \t\t\t{}".format(index_stored ,previous_len-1))
        print("target_following_sequence",final_LCP)
        print("-"*50,"\nfinal_path_dofbot:\n", final_path_dofbot_json,"\n","-"*50,"\n\n")

        # FUN.visualize(WaitKey,blank_path_list_final)


    def solve_final_optimized(self,itr):
        progress_bar = tqdm(total = itr, desc="Searching Optimized way to: ")
        """
        Solve puzzle and visualize the movements and save the movement co-ordinates to ffinal_path_dofbot.json
        """
        self.generate_samples(itr)
        start_time  = time.time()
        print("Start_solving\nwait...")
        unsolved_target_list_list_selected = FUN.read_unsolved_target_list_list()
        individual_no_of_steps = []
        grouped_no_of_steps = []
        indexes = []
        for i in range(itr):
            unsolved_target_list = unsolved_target_list_list_selected[i]
            lock_position_sequence = FUN.solving_lock_position_sequence(unsolved_target_list)
            try:
                blank_path_list = FUN.solve_by_target_list(unsolved_target_list)
                grouped_blank_path = ALGO.NewSlicer(blank_path_list)
                individual_no_of_steps.append(len(blank_path_list))
                grouped_no_of_steps.append(len(grouped_blank_path))
                indexes.append(i)    
            except:
                if i == 0:
                    blank_path_list = [i for i in range(500)]
                    grouped_blank_path = [i for i in range(500)]
                pass
            
            if i > 0:
                current_len = len(grouped_blank_path)
                if current_len < previous_len:
                    index_stored = i
                    previous_len = current_len
                    final_LCP = lock_position_sequence
                    blank_path_list_final = blank_path_list
                    optimized_path = grouped_blank_path
            else:
                index_stored = i
                current_len = len(grouped_blank_path)   
                previous_len = current_len
                final_LCP = lock_position_sequence
                blank_path_list_final = blank_path_list
                optimized_path = grouped_blank_path
            progress_bar.update(1)
        progress_bar.close() 

        total_search_time = time.time() - start_time
        if total_search_time > 60:
            minutes = total_search_time/60
            print("total searching time\t\t\t\t\t", round(minutes,2), "min")
        else:
            print("total searching time\t\t\t\t\t", round(total_search_time,2), "sec")
        
        
        # save final path in co-ordinate format to final_path_dofbot.json
        final_path_dofbot_cords = optimized_path
        # print("\nsrc/puzzle_solver/final_main_method_random_samples")
        # print("blank_path_list: \n",blank_path_list,"\nlen ",len(blank_path_list))
        # # print("\noptimized_path_indexes", optimized_path)
        # # print("\nfinal_path_dofbot_cords: \n",final_path_dofbot_cords,"len\n",len(final_path_dofbot_cords))
        # print()
        
        final_path_dofbot_json = FUN.save_final_path_new(final_path_dofbot_cords, blank_path_list_final)
        # print("\nfinal_path_dofbot_json :\n",final_path_dofbot_json,"\n")

        # print("total_combinations_checked {} ".format(itr))
        # print("least number of steps at index {} are \t\t\t{}".format(index_stored ,previous_len))
        # print("target_following_sequence",final_LCP)
        print("-"*50,"\nfinal_path_dofbot:\n", final_path_dofbot_json,"\n\nlen",len(final_path_dofbot_json),"\n","-"*50,"\n")

        # FUN.visualize(WaitKey,blank_path_list_final)


    def visualize(self,WaitKey,pause):
        # print("visualizing...")
        
        with open("src/database/final_path_dofbot.json","r") as json_file:
            data = json.load(json_file)
        blank_path_list = data["blank_path_list_final"]
        final_path_dofbot = data["final_path_dofbot"]
        # print("\nBlank_path_list: ", blank_path_list)
        # print("\nfinal_path_dofbot: ",final_path_dofbot)

        with open("src/database/patterns.json","r") as json_file:
            data = json.load(json_file)
        raw_target_pattern = data["raw_target_pattern"]
        original_puzzle_pattern = data["puzzle_pattern"]
        target_canvas = CPIG.generate_image(raw_target_pattern, 3)
        cv2.imshow("target_canvas",target_canvas)
        ALGO.puzzle_solve_step_by_step(blank_path_list,original_puzzle_pattern,WaitKey,pause)
        # print("visualization_complete\n\n")




# SOLVE = solver()
# SOLVE.solve_final(50)
# FUN.visualize(50)


# blank_path_list =  [[2, 3], [2, 2], [1, 2], [1, 3], [2, 3], [2, 2], [1, 2], [0, 2], [0, 3], [1, 3], [1, 2], [0, 2], [0, 1], [1, 1], [2, 1], [2, 2], [1, 2], [1, 1], [2, 1], [3, 1], [3, 0], [4, 0], [4, 1], [4, 2], [3, 2], [3, 1], [2, 1], [1, 1], [1, 2], [1, 3], [0, 3], [0, 2], [0, 1], [0, 0], [1, 0], [2, 0], [2, 1], [1, 1], [1, 0], [2, 0], [3, 0], [4, 0], [4, 1], [3, 1], [3, 0], [2, 0], [1, 0], [1, 1], [1, 2], [0, 2], [0, 3], [0, 4], [1, 4], [2, 4], [3, 4], [3, 3], [4, 3], [4, 2], [4, 1], [4, 0], [3, 0], [2, 0], [1, 0], [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [4, 3], [4, 2], [4, 1], [4, 0], [3, 0], [2, 0], [1, 0], [1, 1], [1, 2], [0, 2]]

# print("blank_path_list: ",blank_path_list)
# print(len(blank_path_list))
# print("-"*100)
# print()
# print()

# # optimized_path = ALGO.NewSlicer(blank_path_list)
# optimized_path = ALGO.NewSlicer(blank_path_list)

# print("optimized_path: ",optimized_path)
# print(len(optimized_path))

# # print(FUN.save_final_path(optimized_path,blank_path_list))



