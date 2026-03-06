import copy

import torch

from utils.data import *
import numpy as np
import random
from utils.objection_function import *
from utils.data import read_data,cal_distance,extract_data,extract_data1


def _travel_time(distance_value, speed):
    if speed <= 0:
        return 0.0
    return (float(distance_value) * DISTANCE_UNIT_METERS) / float(speed) / TIME_UNIT_SECONDS
class UAV(object):
    def __init__(self, args=None, speed=60, endurance_time=0.5, max_weight=7, qu=1.0, p0=95.0, emax=475000.0, gamma=0.35):
        if args is not None:
            speed = getattr(args, "drone_speed", speed)
            max_weight = getattr(args, "drone_max_load", max_weight)
            qu = getattr(args, "drone_qu", qu)
            p0 = getattr(args, "drone_p0", p0)
            emax = getattr(args, "drone_emax", emax)
            gamma = getattr(args, "drone_gamma", gamma)
            time_unit_seconds = getattr(args, "time_unit_seconds", 3600.0)
            power_max = p0 * (1 + gamma * max_weight / qu)
            endurance_time = emax / power_max / time_unit_seconds
        else:
            time_unit_seconds = 3600.0
       
        self.speed = float(speed)
        self.endurance_time = float(endurance_time)
        self.max_weight = float(max_weight)
        self.qu = float(qu)
        self.p0 = float(p0)
        self.emax = float(emax)
        self.gamma = float(gamma)
        self.time_unit_seconds = float(time_unit_seconds)
        self.Gmd = self.max_weight
        self.Emd = self.emax
        self.uav_route_list = []



    def UAV_Route_Feasible(self,lauch_node,recycle_node,path_sequence,truck_sequence,distance):
        if self.uav_route_list:
            lauch_node_index,recycle_node_index = truck_sequence.index(lauch_node),truck_sequence.index(recycle_node)
            for uav_route in self.uav_route_list:
                if uav_route[0][-1] == truck_sequence[0][-1]:
                    
                    index_launch,index_recycle= truck_sequence.index(uav_route[0]),truck_sequence.index(uav_route[1])
                    if (lauch_node_index >= index_launch and lauch_node_index < index_recycle) or (recycle_node_index > index_launch and recycle_node_index <= index_recycle):
                        return False 

class truck(object):
    def __init__(self,speed = 30)
        self.speed = float(speed)
        self.truck_route = []
        self.available_UAV = []

class Solution():
    def __init__(self,truck_route,uav_fleet):
        self.truck_route = truck_route
        self.uav_fleet = uav_fleet

    def cal_time(self,distance):
        time = 0
        recycle_node = dict()
        print("-------self.truck_route-----")
        print(self.truck_route)
        for i in range(0,len(self.truck_route) - 1):

            
            if uav_recycle(recycle_node,self.truck_route[i]) and time < max(recycle_node[self.truck_route[i][0]]):
                if max(recycle_node[self.truck_route[i][0]]) - time >= 0.05: 
                    time = max(recycle_node[self.truck_route[i][0]]) 
                    uav_launch(time, self.uav_fleet, self.truck_route[i], recycle_node, distance) 
                else:
                    time1 = max(recycle_node[self.truck_route[i][0]])
                    uav_launch(time1, self.uav_fleet, self.truck_route[i], recycle_node, distance)  
                    time += 0.05
            else:
                uav_launch(time, self.uav_fleet, self.truck_route[i], recycle_node, distance)  
                if i != 0:
                    time += 0.05  
            time += _travel_time(distance[int(self.truck_route[i][0])][int(self.truck_route[i + 1][0])], truck_speed)
        return time
# The code is being updated...
