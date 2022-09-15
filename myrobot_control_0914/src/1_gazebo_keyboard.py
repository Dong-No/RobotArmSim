#!/usr/bin/env python

from getkey import getkey, keys
import rospy
import sys,math
from std_msgs.msg import Float64
from std_msgs.msg import Float64MultiArray

global joint_angle,del_theta
joint_angle = Float64MultiArray()
joint_angle.data = [0,0,0,0]
del_theta = 3.0 * math.pi / 180


def instructions():
    print '''
    keyboard control instructions:
    
    link1: w(+) e(-)
    link2: u(+) j(-)
    link3: i(+) j(-)
    link4: o(+) l(-)

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
    pub = rospy.Publisher('/myrobot/four_joints_position_controllers/command', Float64MultiArray, queue_size=10)
    rate = rospy.Rate(100) # 100hz

def read_keyboard(key_in):

    global joint_angle,del_theta

    if key_in == 'w':
        joint_angle.data[0]+=del_theta
    elif key_in == 'e':
        joint_angle.data[0]-=del_theta

    elif key_in == 'u':
        joint_angle.data[1]+=del_theta
    elif key_in == 'j':
        joint_angle.data[1]-=del_theta

    elif key_in == 'i':
        joint_angle.data[2]+=del_theta
    elif key_in == 'k':
        joint_angle.data[2]-=del_theta

    elif key_in == 'o':
        joint_angle.data[3]+=del_theta
    elif key_in == 'l':
        joint_angle.data[3]-=del_theta

    elif key_in == 'q':
        sys.exit("see you")

    else:
        print "read the instructions"

    for ele in joint_angle.data:
        angle_limit(ele)
    
    pub.publish(joint_angle)

if __name__ == '__main__':
    
    pub_cmd_to_joint()
    instructions()

    while not rospy.is_shutdown():
        key = getkey()
        read_keyboard(key)
        # rate.sleep()
    
        
    
