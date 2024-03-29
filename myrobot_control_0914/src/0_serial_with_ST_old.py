#!/usr/bin/env python
#-*- coding:UTF-8 -*-

##real arm (Axis2 and Axis3 relationship is cared)
import math
import sys
import time

import rospy
from rospy import timer 
from std_msgs.msg import Float64MultiArray
import serial
import threading
import struct

'''
Belt transmition of real arm:

    joint3 is influenced by joint2 by 0.7 
    delta(j3)= delta(j3) +0.7*delta(j2)
    line80 deals with this as if j2 j3 is independent

'''

global cmd 
cmd = []

global Stop_flag
Stop_flag = 1

COM_Name12 = '/dev/ttyACM0'##STM attatched to motor1 and Pressure sensor
COM_Name34 = '/dev/ttyACM1'##STM attatched to motor2 and motor3

BAUTRATE = 230400

def CmdtoByte(NUM):
    NUM_I = int(NUM*1000)
    return struct.pack("<i", NUM_I)

def Cmd_pub12(Serial):
    global cmd
    Command_String = 's'.encode() + CmdtoByte(cmd[0]) + CmdtoByte(cmd[1]) + 'e'.encode()  

    Serial.write(Command_String)
    return

def Cmd_pub34(Serial):
    global cmd
    Command_String = 's'.encode() + CmdtoByte(cmd[2]) + CmdtoByte(cmd[3]) + 'e'.encode()  
    Serial.write(Command_String)
    return

def Connect_STM(COM, baudrate):
    try:
        ser = serial.Serial(COM, baudrate)
    except:
        print('Connect Error! 0')
        return 'Error'
    print('Connect OK! 0')
    return ser
    
def Read_data(Serial):
    global Stop_flag
    while(Stop_flag):
        try:
            data = Serial.readline()
            print data
        except Exception as e:
            print e, data           
    return



def sub_cmd():
    rospy.Subscriber('/real_robot_arm_joint', Float64MultiArray, callback_sub_cmd)

def callback_sub_cmd(msg):
    global cmd
    cmd = list(msg.data)##.data is tuple

    print cmd
    cmd[2]=cmd[2] + cmd[1] * 0.7##belt transmition of real arm
    Cmd_pub12(STM_12)
    Cmd_pub34(STM_34)
    
    
    
    
if __name__ == '__main__' :
 
    STM_12 = Connect_STM(COM_Name12, BAUTRATE)
    STM_34 = Connect_STM(COM_Name34, BAUTRATE)
    
    if  (STM_12 != 'Error' and STM_34 != 'Error'):

        try:
            t_12 = threading.Thread(target=Read_data, args=(STM_12,))
            t_12.start()
            t_34 = threading.Thread(target=Read_data, args=(STM_34,))
            t_34.start()

            rospy.init_node('Com_STM32_INTERFACE',anonymous= True)
            sub_cmd()
            rospy.spin()
        except:
            Stop_flag = 0
            STM_12.close()
            STM_34.close()
            sys.exit('ROS bye!')  
        
    else:
        Stop_flag = 0
        STM_12.close()
        STM_34.close()
        sys.exit('Some error!bye!')
    

 
