#!/usr/bin/env python

from getkey import getkey, keys
import rospy
import sys,math
from std_msgs.msg import Float64MultiArray

global joint_angle,del_theta,ini_angle,goal_angle


joint_angle = [0,0,0,0]
# ini_angle = [0.0, 90-90, -90+90, 0.0]#in deg
ini_angle = [0, 0, 0, 0]#in rad

'''
-+ 90 is because of ST initial 0
but
arm initial state is [0, 90, -90, 0]
'''

# goal_angle = [10.774, -78.9715-90.0, -69.28+90.0, 56.2515]##in deg
goal_angle = [0.18804, -2.94911, 0.36163, 0.98177]
del_theta = [0,0,0,0]

for i in range(len(ini_angle)):
    del_theta[i] = (goal_angle[i] - ini_angle[i])/200##200*0.01 = 2sec (mission time)

def instructions():
    print '''
    precision test instructions:
    
    press s to start
   
    press q to quit
    '''
def angle_limit(theta):

    if theta > math.pi:
        theta = math.pi
    elif theta < -math.pi:
        theta = -math.pi

def pub_cmd_to_joint():
    global pub,rate
    rospy.init_node('joint_position_pub', anonymous=True)
    pub = rospy.Publisher('/real_robot_arm_joint', Float64MultiArray, queue_size=10)
    rate = rospy.Rate(100) # 100hz

def read_keyboard(key_in):

    global joint_angle,del_theta,goal_angle
    a=1
    if key_in =='s':
        while not rospy.is_shutdown():
            if a ==1:
                i=0
                while not abs(goal_angle[0]-joint_angle[0]) < 0.00001:
                    joint_angle[0]+=del_theta[0]
                    joint_angle[1]+=del_theta[1]
                    joint_angle[2]+=del_theta[2]+0.7*del_theta[1]
                    joint_angle[3]+=del_theta[3]


                    array = Float64MultiArray(data = joint_angle)
                    pub.publish(array)
                    # print i
                    # i+=1
                    rospy.sleep(0.01)#sec , dt of robot arm is 0.005
                print "ok" 
                a=2 
                rospy.sleep(1)#sec                 
            # elif key_in =='r':
            elif a == 2:
                while not abs(ini_angle[0]-joint_angle[0]) < 0.00001:
                    joint_angle[0]-=del_theta[0]
                    joint_angle[1]-=del_theta[1]
                    joint_angle[2]-=del_theta[2]+0.7*del_theta[1]
                    joint_angle[3]-=del_theta[3]

                    array = Float64MultiArray(data = joint_angle)
                    pub.publish(array)
                    rospy.sleep(0.01) 
                a=1
                rospy.sleep(1)#sec 
                print "ok"  
    elif key_in == 'q':
        sys.exit("see you")

    else:
        print "read the instructions"

    # for i in range(len(joint_angle)):
    #     angle_limit(joint_angle[i])




if __name__ == '__main__':
    
    pub_cmd_to_joint()
    instructions()

    while not rospy.is_shutdown():
        key = getkey()
        read_keyboard(key)
        # rate.sleep()
    
        
    