# add your fancy code here

import math
import numpy as np


def inv_motion_model(u_t):

    trans = math.sqrt((u_t[1][0]-u_t[0][0])**2 + (u_t[1][1]-u_t[0][1])**2)
    rot1  = math.atan2((u_t[1][1]-u_t[0][1]),(u_t[1][0]-u_t[0][0])) - u_t[0][2]
    rot2  = u_t[1][2] - u_t[0][2] - rot1


    return rot1, trans, rot2

def prob(query, std):

    return max(0,(1/(math.sqrt(6)*std)- (abs(query)/(6 * (std**2)))))

def motion_model_odometry(x_init,x_query,u_t,alpha):

    rot1,trans, rot2 = inv_motion_model(u_t)

    rot1_hat, trans_hat , rot2_hat = inv_motion_model([x_init,x_query])

    p1 = prob(rot1 - rot1_hat,alpha[0]* abs(rot1)+ alpha[1]*trans)
    p2 = prob(trans - trans_hat,alpha[2]*trans + alpha[3] * (abs(rot1)+ abs(rot2)))
    p3 = prob(rot2-rot2_hat, alpha[0] * abs(rot2)  + alpha[1] * trans)


    return p1*p2*p3
