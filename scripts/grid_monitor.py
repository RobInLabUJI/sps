#!/usr/bin/env python
import rospy
import math
from nav_msgs.msg import Odometry
from gazebo_msgs.srv import SpawnModel, DeleteModel
from geometry_msgs.msg import Pose

cell_x = 27
cell_y = 46
grid_size = 50.0

previous_cell = None

pose = Pose()
pose.position.x = 0
pose.position.y = 0
pose.position.z = 0
pose.orientation.x = 0
pose.orientation.y = 0
pose.orientation.z = 0
pose.orientation.w = 1

grid = []  # List to store the tuples

with open('/home/ecervera/Escritorio/CERN/catkin_ws/src/sps/sdf/keys.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        values = line.split()
        a, b = map(int, values)
        tuple_data = (a, b)
        grid.append(tuple_data)
        
def grid_cell(x,y):
    xg = math.floor(x/grid_size) + cell_x
    yg = math.floor(y/grid_size) + cell_y
    return xg, yg

def spawn_cell(cx, cy):
    global spawn_sdf_model
    if (cx, cy) in grid:
        pose.position.x = (cx-cell_x) * grid_size
        pose.position.y = (cy-cell_y) * grid_size
        model_name = 'sps_' + str(cx).zfill(2) + str(cy).zfill(2)
        with open("/home/ecervera/Escritorio/CERN/catkin_ws/src/sps/sdf/"+model_name+"/model.sdf", "r") as f:
            model_xml = f.read()
        spawn_sdf_model(model_name, model_xml, "", pose, "world")

def delete_cell(cx,cy):
    global delete_model
    if (cx, cy) in grid:
        model_name = 'sps_' + str(cx).zfill(2) + str(cy).zfill(2)
        delete_model(model_name)
            
def callback(data):
    global previous_cell
    global spawn_sdf_model
    global delete_model

    x = data.pose.pose.position.x
    y = data.pose.pose.position.y
    if previous_cell is None:
        init_cx, init_cy = grid_cell(x, y)
        for dx in range(-1,2):
            for dy in range(-1,2):
                cx = init_cx + dx
                cy = init_cy + dy
                if (cx, cy) in grid:
                    spawn_cell(cx, cy)
        previous_cell = grid_cell(x, y)
        
    current_cell = grid_cell(x,y)
    pcx, pcy = previous_cell
    ccx, ccy = current_cell
    if ccx > pcx:
        spawn_cell(ccx+1, ccy-1)
        spawn_cell(ccx+1, ccy)
        spawn_cell(ccx+1, ccy+1)
        delete_cell(ccx-2, ccy-1)
        delete_cell(ccx-2, ccy)
        delete_cell(ccx-2, ccy+1)
    if ccx < pcx:
        spawn_cell(ccx-1, ccy-1)
        spawn_cell(ccx-1, ccy)
        spawn_cell(ccx-1, ccy+1)
        delete_cell(ccx+2, ccy-1)
        delete_cell(ccx+2, ccy)
        delete_cell(ccx+2, ccy+1)
    if ccy > pcy:
        spawn_cell(ccx-1, ccy+1)
        spawn_cell(ccx,   ccy+1)
        spawn_cell(ccx+1, ccy+1)
        delete_cell(ccx-1, ccy-2)
        delete_cell(ccx,   ccy-2)
        delete_cell(ccx+1, ccy-2)
    if ccy < pcy:
        spawn_cell(ccx-1, ccy-1)
        spawn_cell(ccx,   ccy-1)
        spawn_cell(ccx+1, ccy-1)
        delete_cell(ccx-1, ccy+2)
        delete_cell(ccx,   ccy+2)
        delete_cell(ccx+1, ccy+2)
            
    previous_cell = current_cell
    
def listener():
    global spawn_sdf_model
    global delete_model
        
    rospy.init_node('grid_monitor', anonymous=True)

    rospy.Subscriber("/ground_truth/odom", Odometry, callback)
    rospy.wait_for_service('/gazebo/spawn_sdf_model')
    spawn_sdf_model = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
    rospy.wait_for_service('/gazebo/delete_model')
    delete_model = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
        
    rospy.spin()

if __name__ == '__main__':
    listener()
