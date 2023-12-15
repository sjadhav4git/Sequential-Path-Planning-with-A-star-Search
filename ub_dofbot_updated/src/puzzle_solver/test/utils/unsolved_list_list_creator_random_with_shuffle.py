import json
from itertools import permutations
import random
import time

class random_unsolved:
    def random_n_generate(self,length):
        start_time = time.time()
        unsolved_target_list = [[0,0],[1,0],[2,0],
                                [0,1],[1,1],[2,1],
                                [0,2],[1,2],[2,2]]


        index_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        
        random_unsolved_target_list_lists =[unsolved_target_list]
        
        for i in range(length-1):
            random.shuffle(index_list)
            unsolved_target_list_temp = []
            for j in index_list:
                unsolved_target_list_temp.append(unsolved_target_list[j])
            random_unsolved_target_list_lists.append(unsolved_target_list_temp)
        
        data = {
            "unsolved_target_list_lists": random_unsolved_target_list_lists
            # "unsolved_target_list_lists": unsolved_target_list_lists
        }
        
        with open("unsolved_target_lists_random_shuffle.json", "w") as json_file:
            json.dump(data,json_file,indent=4)

        print("\ndata saved to unsolved_target_lists.json")
        end_time = time.time()
        print("time taken to save n samples: ", end_time-start_time, "sec")
        
    