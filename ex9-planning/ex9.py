#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

thr_free = 0.9

def plot_path(path, x_start, x_goal, M):
    plt.matshow(M, cmap="gray")
    if path.shape[0] > 2:
        plt.plot(path[:, 1], path[:, 0], 'b')
    plt.plot(x_start[1], x_start[0], 'or')
    plt.plot(x_goal[1], x_goal[0], 'xg')
    plt.show()


def is_valid(v):
    if v > thr_free:
        return True
    return False

def plan_path_uninformed(x_start, x_goal, M):
    
    cost = 1
    count = 0
    goal = False
    no_expansion =  False
    checked = np.zeros_like(M)
    action_save = np.ones_like(M) * (-1)

    g = 0 
    x = int(x_start[1])
    y = int(x_start[0])
    checked[y][x] = 1
    actions = [[0 , 1],
               [0 ,-1],
               [-1, 0],
               [1 , 0],
               [-1, -1],
               [-1, 1],
               [1, -1],
               [1, 1]]
    open_list = [[g,y,x]]

    
    while goal is False and no_expansion is False:
       
        
        if len(open_list)==0:
            print(open_list)
            no_expansion = True
            print("-------Path not found----------")
        
        else:
            open_list.sort(reverse=True)
            new_node = open_list.pop()

            g = new_node[0]
            x = new_node[2]
            y = new_node[1]
            count+=1
            if x == x_goal[1] and y == x_goal[0] :
                goal =True
              
                print("At goal point")
            else:
                
                for i in range(len(actions)):

                    x_updated = int(x + actions[i][1])
                    y_updated = int(y + actions[i][0])
                    
                    if 0<=x_updated<=(M.shape[1]-1) and 0<=y_updated<=(M.shape[0]-1):

                        if is_valid(M[y_updated][x_updated]) is True and checked[y_updated][x_updated] == 0:
                            
                            
                            g_updated = g + cost
                            open_list.append([g_updated,y_updated,x_updated])
                            checked[y_updated][x_updated] = 1
                            action_save[y_updated][x_updated] = i
                            
    
    if no_expansion is False and goal is True:

        path = np.array([int(x_goal[0]),int(x_goal[1])])
        x_new = int(x_goal[1])
        y_new = int(x_goal[0])
        
        while x_new != x_start[1] or y_new != x_start[0]:
            
            x_prev = x_new - actions[int(action_save[y_new][x_new])][1]
            y_prev = y_new - actions[int(action_save[y_new][x_new])][0] 
            
            path = np.vstack((path,[y_new,x_new]))

            x_new = x_prev
            y_new = y_prev
    print("Number of nodes explored are: ",count)
    print("Length of the path: ",path.shape[0])
    return path

def h_cost(x,y,x_goal):
    
    x_f = int(x_goal[1])
    y_f = int(x_goal[0])

    return int(np.sqrt(((x_f-x)**2) + ((y_f-y)**2)))

def plan_path_astar(x_start, x_goal, M):

    cost = 1
    count =0
    goal = False
    no_expansion =  False
    checked = np.zeros_like(M)
    action_save = np.ones_like(M) * (-1)

    g = 0 
    x = int(x_start[1])
    y = int(x_start[0])
    checked[y][x] = 1
    actions = [[0 , 1],
               [0 ,-1],
               [-1, 0],
               [1 , 0],
               [-1, -1],
               [-1, 1],
               [1, -1],
               [1, 1]]

    f = g + h_cost(x,y,x_goal)
    open_list = [[f,g,h_cost(x,y,x_goal),y,x]]

    
    while goal is False and no_expansion is False:
       
        
        if len(open_list)==0:
            print(open_list)
            no_expansion = True
            print("-------Path not found----------")
        
        else:
            open_list.sort(reverse=True)
            new_node = open_list.pop()
          
            f = new_node[0]
            g = new_node[1]
            h = new_node[2]
            x = new_node[4]
            y = new_node[3]
            count += 1
            if x == x_goal[1] and y == x_goal[0] :
                goal =True
        
                print("At goal point")
            else:
                
                for i in range(len(actions)):

                    x_updated = int(x + actions[i][1])
                    y_updated = int(y + actions[i][0])
                    
                    if 0<=x_updated<=(M.shape[1]-1) and 0<=y_updated<=(M.shape[0]-1):

                        if is_valid(M[y_updated][x_updated]) is True and checked[y_updated][x_updated] == 0:
                           
                            h_updated = h_cost(x_updated,y_updated,x_goal)
                            g_updated = g + cost
                            f_updated = g_updated + h_updated
                            open_list.append([f_updated,g_updated,h_updated,y_updated,x_updated])
                            checked[y_updated][x_updated] = 1
                        
                            action_save[y_updated][x_updated] = i
                            
    if no_expansion is False and goal is True:

        path = np.array([int(x_goal[0]),int(x_goal[1])])
        x_new = int(x_goal[1])
        y_new = int(x_goal[0])
        
        while x_new != x_start[1] or y_new != x_start[0]:
            
        
            
            x_prev = x_new - actions[int(action_save[y_new][x_new])][1]
            y_prev = y_new - actions[int(action_save[y_new][x_new])][0] 
            
            path = np.vstack((path,[y_new,x_new]))

            x_new = x_prev
            y_new = y_prev
 
    print("Number of nodes explored are: ",count)
    print("Length of the path: ",path.shape[0])
    return path
