#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

def plot_belief(belief):
    
    plt.figure()
    
    ax = plt.subplot(2,1,1)
    ax.matshow(belief.reshape(1, belief.shape[0]))
    ax.set_xticks(np.arange(0, belief.shape[0],1))
    ax.xaxis.set_ticks_position("bottom")
    ax.set_yticks([])
    ax.title.set_text("Grid")
    
    ax = plt.subplot(2, 1, 2)
    ax.bar(np.arange(0, belief.shape[0]), belief)
    ax.set_xticks(np.arange(0, belief.shape[0], 1))
    ax.set_ylim([0, 1.05])
    ax.title.set_text("Histogram")


def motion_model(action, belief):
    
    p_ff = p_bb = 0.7
    p_bf = p_fb = 0.1
    p_stay = 0.2
    
    belief_out = np.zeros(len(belief))
        
    if action == "F":
        
        for i in range(len(belief)):

            if i < 14 and i > 0:

                belief_out[i] = (belief[i-1]*p_ff + belief[i+1]*p_fb + belief[i] * p_stay)

            elif i == 0:
                
                belief_out[i] = (belief[i+1] * p_fb + belief[i] * p_stay)

            else:

                belief_out[i] = (belief[i-1] * p_ff + belief[i] * p_stay)

    else:
        
        for i in range(len(belief)):

            if i < 14 and i > 0:

                belief_out[i] = (belief[i+1] * p_bb + belief[i-1] * p_fb + belief[i] * p_stay)

            elif i == 0:

                belief_out[i] = (belief[i+1] * p_bb + belief[i] * p_stay)

            else:

                belief_out[i] = (belief[i-1] * p_bf + belief[i] * p_stay)
                
    
    return belief_out

    
def sensor_model(observation, belief, world):
    
    p_white = 0.7
    p_black = 0.9
    belief_out = np.copy(belief)

    if observation == 0:
        
        for i,val in enumerate(world):
            
            if val == 0:
                
                belief_out[i] = p_black * belief[i]
            
            else:
                
                belief_out[i] = (1-p_white) * belief[i]
        
        
    else:
        
        for i,val in enumerate(world):
            
            if val == 1:
                
                belief_out[i] = p_white * belief[i]
            
            else:
                
                belief_out[i] = (1-p_black) * belief[i]
    
    
    return belief_out/sum(belief_out)

def recursive_bayes_filter(actions, observations, belief, world):
    
    
    belief_sensor = sensor_model(observations[0],belief,world)
    
    
    for i, action in enumerate(actions):
        
        mot_belief    = motion_model(action,belief_sensor)
        belief_sensor = sensor_model(observations[i+1],mot_belief,world)
    
    return belief_sensor