import utils.color_pallet_image_generator as cpig
import cv2
import numpy as np
from queue import PriorityQueue

CPIG = cpig.image_generator()
class Algorithm:
    # find color at location of point given co-ordinates (x,y)
    def find_color_at_location(self,location:list, puzzle_pattern:list):
        row_num = location[1]
        column_num = location[0]
        return(puzzle_pattern[row_num][column_num])
    
    # find the location of blank sapce in puzzle --> return x,y co-ordinates
    def find_blank_space(self, puzzle_pattern:list):
        row_index = 0
        column_index = 0 
        for row_index in range(5):
            for column_index in range(5):
                element = puzzle_pattern[row_index][column_index]
                if element == '0':
                    # return [row_index,column_index]
                    x = column_index
                    y = row_index
                    return[x, y]

    # find the neighbour elements near to given (x,y) location
    def neighbor_elements(self, center_location:list):
        neighbor = []
        row_num = center_location[0]
        column_num = center_location[1]
        
        if column_num > 0 and column_num<4:
            neighbor.append([row_num,column_num-1])
            neighbor.append([row_num,column_num+1])
        elif column_num == 0:
            neighbor.append([row_num,column_num+1])
        elif column_num == 4:
            neighbor.append([row_num,column_num-1])
        
        if row_num > 0 and row_num<4:
            neighbor.append([row_num-1, column_num])
            neighbor.append([row_num+1,column_num])
        elif row_num == 0:
            neighbor.append([row_num+1, column_num])
        elif row_num == 4:
            neighbor.append([row_num-1, column_num])
        
        return neighbor
        
    # find already achieved positions in puzzle comparing with target. and return the position which matched. 
    def first_check_matched(self,puzzle_pattern:list,target_pattern:list): 
        match_list = []
        unsolved_target_list = []
        for y in range(3):
            for x in range(3):
                if target_pattern[y][x] == puzzle_pattern[y+1][x+1]:
                    match_list.append([x+1,y+1])
                else:
                    unsolved_target_list.append([x,y])    
                
        return match_list,unsolved_target_list
                
#------------------------------------------------------------------------------------------------------------             
    
    def find_location_of_color(self, puzzle_pattern:list,target_color:str):
        match_color_location = []
        for x in range(5):
            for y in range(5):
                location = [x,y]
                puzzle_color = Algorithm.find_color_at_location(self,location, puzzle_pattern)
                if puzzle_color == target_color:
                    match_color_location.append(location)
        return match_color_location
    
    
    def A_star(self,start_point,goal_point,lock_positions:list):
        # create_grid
        def grid_creator(lock_positions):
            grid=[]
            for y in range(5):
                row = []
                for x in range(5):
                    if [x,y] not in lock_positions:
                        row.append(0)
                    else:
                        row.append(1)
                grid.append(row)
            return grid
            
        grid = grid_creator(lock_positions)
        start = (start_point[1],start_point[0])
        goal = (goal_point[1],goal_point[0])
        
        # Define the possible movements (up, down, left, right)
        movements = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # Create a dictionary to store the cost of each position
        costs = {}
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                costs[(row, col)] = float('inf')

        # Create a priority queue for the open set
        open_set = PriorityQueue()
        open_set.put((0, start))  # Start position with cost 0

        # Create a dictionary to store the parent of each position
        parents = {}
        parents[start] = None

        # Create a function to calculate the heuristic (Manhattan distance)
        def heuristic(a, b):
            return abs(b[0] - a[0]) + abs(b[1] - a[1])

        # A* algorithm
        while not open_set.empty():
            current_cost, current = open_set.get()
            if current == goal:
                break

            for movement in movements:
                dx, dy = movement
                next_position = (current[0] + dx, current[1] + dy)

                if next_position[0] >= 0 and next_position[0] < len(grid) and next_position[1] >= 0 and next_position[1] < len(grid[0]):
                    if grid[next_position[0]][next_position[1]] == 1:
                        continue
                    
                    new_cost = current_cost + 1

                    if new_cost < costs[next_position]:
                        costs[next_position] = new_cost
                        priority = new_cost + heuristic(next_position, goal)
                        open_set.put((priority, next_position))
                        parents[next_position] = current

        # Retrieve the path by backtracking from the goal to the start
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = parents[current]
        path.append(start)
        path.reverse()
        
        
        # convert into [x,y] array
        def convert(path):
            Path = []
            for loc in path:
                x = loc[1]
                y = loc[0]
                Path.append([x,y])
            return Path
        path = convert(path)
        
        return path
       
    
    def A_star_for_blank_path(self,start_point,goal_point,lock_positions:list,temp_lock_position):
        # create_grid
        lock_positions_with_temp_lock = lock_positions
        lock_positions_with_temp_lock.append(temp_lock_position)
        def grid_creator(lock_positions_with_temp_lock):
            grid=[]
            for y in range(5):
                row = []
                for x in range(5):
                    if [x,y] not in lock_positions_with_temp_lock:
                        row.append(0)
                    else:
                        row.append(1)
                grid.append(row)
            return grid
            
        grid = grid_creator(lock_positions_with_temp_lock)
        start = (start_point[1],start_point[0])
        goal = (goal_point[1],goal_point[0])
        
        # Define the possible movements (up, down, left, right)
        movements = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # Create a dictionary to store the cost of each position
        costs = {}
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                costs[(row, col)] = float('inf')

        # Create a priority queue for the open set
        open_set = PriorityQueue()
        open_set.put((0, start))  # Start position with cost 0

        # Create a dictionary to store the parent of each position
        parents = {}
        parents[start] = None

        # Create a function to calculate the heuristic (Manhattan distance)
        def heuristic(a, b):
            return abs(b[0] - a[0]) + abs(b[1] - a[1])

        # A* algorithm
        while not open_set.empty():
            current_cost, current = open_set.get()
            if current == goal:
                break

            for movement in movements:
                dx, dy = movement
                next_position = (current[0] + dx, current[1] + dy)

                if next_position[0] >= 0 and next_position[0] < len(grid) and next_position[1] >= 0 and next_position[1] < len(grid[0]):
                    if grid[next_position[0]][next_position[1]] == 1:
                        continue
                    
                    new_cost = current_cost + 1

                    if new_cost < costs[next_position]:
                        costs[next_position] = new_cost
                        priority = new_cost + heuristic(next_position, goal)
                        open_set.put((priority, next_position))
                        parents[next_position] = current

        # Retrieve the path by backtracking from the goal to the start
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = parents[current]
        path.append(start)
        path.reverse()
        
        
        # convert into [x,y] array
        def convert(path):
            Path = []
            for loc in path:
                x = loc[1]
                y = loc[0]
                Path.append([x,y])
            return Path
        path = convert(path)
        
        return path
    
    
    
    def tile_move_A_star_path_list(self,available_color_locations,target_color_location,lock_positions):
        selected_tile_path_lists = []
        for color_location in available_color_locations:
            start = color_location
            goal = [target_color_location[0]+1,target_color_location[1]+1]
            selected_path = self.A_star(start,goal,lock_positions)
            selected_tile_path_lists.append(selected_path)
        return selected_tile_path_lists
    
    
    
    def update_puzzle(self,puzzle_pattern,blank_path):
        # print("\nblank_path: ",blank_path)
        # print("un-puzzlePattern: ", puzzle_pattern)
        clrs = []
        for i in range (len(blank_path)-1):
            row= blank_path[i+1][1]
            col =blank_path[i+1][0]            
            clrs.append(puzzle_pattern[row][col])
            
        for i in range (len(blank_path)-1):
            row= blank_path[i][1]
            col =blank_path[i][0]
            puzzle_pattern [row][col]=clrs[i]
        
        row= blank_path[-1][1]
        col =blank_path[-1][0]
        puzzle_pattern[row][col] = '0'
        
        # print("updated-puzzle_pattern",puzzle_pattern)
        # print("clrs",clrs)
        return puzzle_pattern
        
        
        
    def list_flattener(self,List):
        flat_list = []
        for sublist in List:
            for subelement in sublist:
                flat_list.append(subelement)
            # print(sublist)      
        flat_list_unique_elements = []
        for i in range(len(flat_list)-1):
            if flat_list[i] != flat_list[i+1]:
                flat_list_unique_elements.append(flat_list[i])
                
        flat_list_unique_elements.append(flat_list[-1])
            
        return flat_list_unique_elements
        
    
    def slicer(self,blank_path_list):
        slice_index_list = []
        # slice_index_list.append(blank_path_list[0])
        
        for i in range(len(blank_path_list)-1):
            ele1 = blank_path_list[i]
            ele2 = blank_path_list[i+1]
            if ele1[1] == ele2[1]: #movement in x direction
                # slice_index_list_x.append(i)
                slice_index_list.append('x')
                
            if ele1[0] == ele2[0]: #movement in y direction
                # slice_index_list_x.append(i)
                slice_index_list.append('y')
        
        # for i,dir in enumerate(slice_index_list):
        ind_list = []
        ind_list.append(0)
        for j in range(len(slice_index_list)-1):
            if slice_index_list[j] != slice_index_list[j+1]:
                ind_list.append(j+1)
        ind_list.append(len(blank_path_list)-1)
        sliced_ind_list = ind_list
        return sliced_ind_list

    
    def movement_list_maker(self,blank_path_list):
        sliced_ind_list = self.slicer(blank_path_list)
        movement_groups = []
        for i in range(len(sliced_ind_list)-1):
            ind1 = sliced_ind_list[i]
            ind2 = sliced_ind_list[i+1]
            movement_groups.append(blank_path_list[ind1:ind2+1])
            
        return movement_groups
    
    # ++++++++++++++++++++++++++++++++++++++++++++++ ONgoing

    def movement_list_maker_for_dofbot(self,blank_path_list,grouped_blank_path_indexes):
        movement_groups = []
        for i in grouped_blank_path_indexes[1:]:
            movement_groups.append([blank_path_list[i],blank_path_list[i-1]])    
        return movement_groups
    
    # ++++++++++++++++++++++++++++++++++++++++++++++ ONgoing

    
    def puzzle_solve_step_by_step(self,blank_path_list,original_puzzle_pattern,waitKey):
        # print(original_puzzle_pattern)
        
        
        sliced_ind_list= self.slicer(blank_path_list)
        for i in range(len(blank_path_list)-1):
            step_puzzle_canvas = CPIG.generate_image_puzzle_pattern(original_puzzle_pattern,5)  
            if i in sliced_ind_list:          
                cv2.imshow('Step_puzzle_solver',step_puzzle_canvas)
            if i == 0:
                cv2.waitKey(waitKey*10)
            else:
                cv2.waitKey(waitKey)
            
            loc1 = blank_path_list[i]
            loc2 = blank_path_list[i+1]
            # find color at loc2
            clr = self.find_color_at_location(loc2,original_puzzle_pattern)
            
            original_puzzle_pattern[loc1[1]][loc1[0]] = clr
            original_puzzle_pattern[loc2[1]][loc2[0]] = '0'
            
            # step_puzzle_canvas = CPIG.generate_image_puzzle_pattern(original_puzzle_pattern,5)            
            # cv2.imshow('Step_puzzle_solver',step_puzzle_canvas)
            # cv2.waitKey(50)
            # visualize original puzzle pattern
        
        step_puzzle_canvas = CPIG.generate_image_puzzle_pattern(original_puzzle_pattern,5)            
        cv2.imshow('Step_puzzle_solver',step_puzzle_canvas)
        cv2.waitKey(0)
      
      
        
    def solve_puzzle(self,puzzle_pattern,target_pattern,unsolved_target_list,lock_positions):
        
        # lock_positions = []
        total_path= []
        
        while True:
            
            # for center in lock_positions:
            #     clr = (40,40,40)
            #     loc = ((center[0]*100 + 50),(center[1]*100 + 50))
            
            if len(unsolved_target_list) == 0:
                # print("puzzle solved...")
                break 
            # peak first element color of unsolved target list and start solving it
            # unsolved target list updating each time hence we pick first element every time until there are no elements left.
            target_color_location = unsolved_target_list[0]
            
            target_color = self.find_color_at_location(target_color_location,target_pattern)
            
            #
            # __________________________________________________________________
            # find target color in puzzle_pattern
            #-> note: shouldn't be color at lock_positions
            
            available_color_locations = self.find_location_of_color(puzzle_pattern,target_color)  
            available_color_locations_temp = []
            for valid_loc in available_color_locations:
                if valid_loc not in lock_positions:
                    available_color_locations_temp.append(valid_loc)
            available_color_locations = available_color_locations_temp
            # print("---------------------------------------------------------------")
            # print("\n\n\navailable_color_locations: ",available_color_locations, "target_color:",target_color,"at",target_color_location)
            
            # find paths from each available color locations to destination location using A_star --tile_move_A_star_path_list
            selected_tile_path_lists = self.tile_move_A_star_path_list(available_color_locations,target_color_location,lock_positions)
            
            # find shortest path:
            lengths = []
            for selected_path in selected_tile_path_lists:
                length = len(selected_path)
                lengths.append(length)
            
            index = lengths.index(min(lengths))
            shortest_path = selected_tile_path_lists[index]
            selected_path = shortest_path
            
            # print("selected_avl_clr_loc:",selected_path[0])
            
            # find blank path from blank location to index 1 location in selected path
            # and add index 0 location in blank path
            
            # print("\nselected_path-103",selected_path)
            for i in range(len(selected_path)-1):
                temp_lock_position  = selected_path[i]
                # print("temp_lock_position-106",temp_lock_position)
                blank_space_location = self.find_blank_space(puzzle_pattern)
                goal_point = selected_path[i+1]
                # print("lock_positions", lock_positions)
                lock_positions.append(temp_lock_position)
                # print("lock_positions_append", lock_positions)
                blank_path = self.A_star(blank_space_location,goal_point,lock_positions)
                lock_positions.pop()
                
                blank_path.append(selected_path[i])
                total_path.append(blank_path)
                # print("i:",i,"\nBlank_path:",blank_path)
                # print("lock_positions_pop", lock_positions)
                
                # update_puzzle_pattern
                self.update_puzzle(puzzle_pattern,blank_path)
                updated_puzzle_canvas = CPIG.generate_image_puzzle_pattern(puzzle_pattern,5)   
                #cv2.imshow("updated_puzzle",updated_puzzle_canvas)
                #cv2.waitKey(20)
                #cv2.imshow("prev_updated_puzzle",updated_puzzle_canvas)
                        
            #_____________________________________________________________________
            # update lock_pose.json
            new_lock_pose = [unsolved_target_list[0][0] +1 ,unsolved_target_list[0][1] +1 ]
            lock_positions.append(new_lock_pose)
            # locked_loc = unsolved_target_list.pop(0) 
            unsolved_target_list.pop(0) 
            # print("unsolved_target_list-210:",unsolved_target_list)
                
            # lock_positions.append(locked_loc)
            
            
        #cv2.imshow('puzzle',canvas)
        #cv2.imshow('target',target_canvas)
        #cv2.imshow('solved_puzzle',updated_puzzle_canvas)
        # self.list_flattener(total_path)

        #cv2.waitKey(20)
        # print("total_path",total_path)
        # print(len(total_path))
        # print(np.shape(total_path))

        blank_path_list = self.list_flattener(total_path)
        return blank_path_list      
