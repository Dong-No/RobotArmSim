#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import threading
import rospy
import struct
import sys
from std_msgs.msg import Float64 , String
COM_Name = '/dev/ttyACM0'
Stop_flag = 1
BAUTRATE = 230400#9600
dt = 0.005#0.005

Cmd_2 = 0.01
Cmd_3 = 0.02

def callback2(data):
    global Cmd_2 
    Cmd_2 = data.data
def callback3(data):
    global Cmd_3     
    Cmd_3 = data.data  

def CmdtoByte(NUM):
    NUM_I = int(NUM*1000)
    return struct.pack("<i", NUM_I)#some needed transformation for passing data from python to c++ 


def Cmd_pub(Serial):
    
    Command_String = 's'.encode() + CmdtoByte(Cmd_2) + CmdtoByte(Cmd_3) + 'e'.encode()  

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
    #ser = serial.Serial(COM, baudrate)
    
def Read_data(Serial):
    
    while(Stop_flag):
        try:
            data = Serial.readline()
            
	    print(data)
        except Exception as e:
            print(e, data)            
    return
    
###


if __name__ == '__main__':
    
    rospy.init_node('Com_STM32_INTERFACE', anonymous= True)
    # rospy.Subscriber("joint2",Float64,callback2) 
    # rospy.Subscriber("joint3",Float64,callback3)
    rate = rospy.Rate(100)
    #  Cmd_3 = rospy.Subscriber("/myrobot/joint3_position_controller/command", Float64 , callback)   
    
    try:
        STM = Connect_STM(COM_Name, BAUTRATE)
        if STM != 'Error':
            t = threading.Thread(target=Read_data, args=(STM,))
            t.start()
            while not rospy.is_shutdown():
                Cmd_pub(STM)
                rate.sleep()


            Stop_flag = 0
            STM.close()   
            print('ROS bye!')        
            sys.exit()
    except: 
        print('Some error!bye!')
        sys.exit()
    


        
        
    
    

    
