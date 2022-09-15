#!/usr/bin/env python

import rospy
import sys,math
from std_msgs.msg import Float64
from std_msgs.msg import Float64MultiArray
from moveit_msgs.msg import DisplayTrajectory
from trajectory_msgs.msg import JointTrajectory,JointTrajectoryPoint

global joint_angle,del_theta
joint_angle = Float64MultiArray()
joint_angle.data = [0,math.pi/2,-math.pi/2,-math.pi/2]


initial_offset = [0,math.pi/2,-math.pi/2,0]#difference btw ST-zero-point and Moveit-zero-point
def real_arm_issue(cmd_list):
    for i in range(len(cmd_list)):
        cmd_list[i] = cmd_list[i] - initial_offset[i]
    return cmd_list
    '''
    The same initial pose of real arm  btw ST and Moveit
            |
            |    
        ____|
        |
    =========

    but  their data differ  :
    
        ST          Moveit_plan
        j1:0        j1:0
        j2:0        j2:1.5708       ---> j2(ST) = j2(Moveit) -1.5708
        j3:0        j3:-1.5708      ---> j3(ST) = j3(Moveit) +1.5708
        j4:0        j4:0
    '''
    


def angle_limit(theta):

    if theta > math.pi:
        theta = math.pi
    elif theta < -math.pi:
        theta = -math.pi
    return theta

def pub_cmd_to_joint():
    global pub,rate,joint_angle
    rospy.init_node('joint_position_pub', anonymous=True)
    pub = rospy.Publisher('/real_robot_arm_joint', Float64MultiArray, queue_size=10)
    # rate = rospy.Rate(100) # 100hz
    

def sub_to_moveit():
	rospy.Subscriber("/move_group/display_planned_path",DisplayTrajectory,callback)

def callback(msg_get):
    # msg_get = DisplayTrajectory
    global joint_angle
    for ele in  msg_get.trajectory:

        a_list = ele.joint_trajectory.points
        for e in  a_list:
            joint_angle.data = e.positions
            # print "line 41",joint_angle.data
            joint_angle.data = list(joint_angle.data)

            # for angle in joint_angle.data:
            #     angle = angle_limit(angle)

            joint_angle.data = real_arm_issue(joint_angle.data)

            pub.publish(joint_angle)
            rospy.sleep(0.03)##check if moveit_plan has time stamp to set this

if __name__ == '__main__':


    print "moveit_real_arm_interface ok!"   
    pub_cmd_to_joint()

    sub_to_moveit()
    rospy.spin()

   
   
    
        
    
