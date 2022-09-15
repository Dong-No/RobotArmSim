#!/usr/bin/env python
#-*- coding:UTF-8 -*-

##real arm (Axis2 and Axis3 relationship is cared)

#from __future__ import print_function
import math
import sys
import time

import rospy
from rospy import timer 
from std_msgs.msg import Float64 , String
import serial
import threading
import struct

COM_Name1P = '/dev/ttyACM0'##STM attatched to motor1 and Pressure sensor
COM_Name23 = '/dev/ttyACM1'##STM attatched to motor2 and motor3
Stop_flag = 1
BAUTRATE = 230400#9600
# dt = 0.005#0.005

Cmd_1 = 0.0
Cmd_2 = 0.0
Cmd_3 = 0.0
Pressure_volt = 0.003#just initialize

#＃All lengh unit in mm
dis_num_board = 49.0	#distance between any two number boards is 0.049m
dis_ori_plate = (63.0+70.0) #distance between origin and the plate site
link0 = 60.0
link1 = 82.0
link2 = 131.0
link3 = 186.0#186 #take the center of ball as end of axis3

###need ro adjust in real arm
up_down_dis = 20.0 #20 #ball surface touch the plate
above_dis = 40.0 ##distance between ball center and ground
###need ro adjust in real arm

half_plate_lengh = 151.0/2.0

interval_i = 50 ##this is used for for_loop i,must be in type int
interval = 50.0 ##this is used for float division,must be in type float
time_interval = 0.01  #sec per interval





class coordinate:
    
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z

# now_position = coordinate(0.0 , dis_ori_plate + half_plate_lengh , up_down_dis)
# now_position = coordinate(0.0 , dis_ori_plate + half_plate_lengh + dis_num_board, up_down_dis)##assign initial position

##Note that coordinate is for ball center.


##11/28
R=[coordinate(0.0 , (link2+link3) , (link0+link1)) , coordinate( (link2+link3)*math.sin(28*math.pi/180.0),(link2+link3)*math.cos(28*math.pi/180.0) , link0+link1)]

# now_position = coordinate(0.0 , (link2+link3) , (link0+link1))
now_position = R[1]##11/28

A = [coordinate(-dis_num_board , dis_ori_plate + half_plate_lengh + dis_num_board , above_dis) , coordinate(-dis_num_board , dis_ori_plate + half_plate_lengh + dis_num_board , up_down_dis)]
B = [coordinate(0.0 , dis_ori_plate + half_plate_lengh + dis_num_board , above_dis) , coordinate(0.0 , dis_ori_plate + half_plate_lengh + dis_num_board, up_down_dis)]
C = [coordinate(dis_num_board , dis_ori_plate + half_plate_lengh + dis_num_board, above_dis) , coordinate(dis_num_board , dis_ori_plate + half_plate_lengh + dis_num_board, up_down_dis)]
D = [coordinate(-dis_num_board , dis_ori_plate + half_plate_lengh+4 , above_dis) , coordinate(-dis_num_board , dis_ori_plate + half_plate_lengh+4 , up_down_dis)]
E = [coordinate(0.0 , dis_ori_plate + half_plate_lengh+4 , above_dis) , coordinate(0.0 , dis_ori_plate + half_plate_lengh+4 , up_down_dis)]
F = [coordinate(dis_num_board , dis_ori_plate + half_plate_lengh+4 , above_dis) , coordinate(dis_num_board , dis_ori_plate + half_plate_lengh+4 , up_down_dis)]
G = [coordinate(-dis_num_board , dis_ori_plate + half_plate_lengh - dis_num_board , above_dis) , coordinate(-dis_num_board , dis_ori_plate + half_plate_lengh - dis_num_board , up_down_dis)]
H = [coordinate(0.0 , dis_ori_plate + half_plate_lengh - dis_num_board , above_dis) , coordinate(0.0 , dis_ori_plate + half_plate_lengh - dis_num_board , up_down_dis)]
I = [coordinate(dis_num_board , dis_ori_plate + half_plate_lengh - dis_num_board , above_dis) , coordinate(dis_num_board , dis_ori_plate + half_plate_lengh - dis_num_board , up_down_dis)]



def CmdtoByte(NUM):
    NUM_I = int(NUM*1000)
    return struct.pack("<i", NUM_I)
def Cmd_pub23(Serial):
    global Cmd_2
    global Cmd_3
    Command_String = 's'.encode() + CmdtoByte(Cmd_2) + CmdtoByte(Cmd_3) + 'e'.encode()  

    Serial.write(Command_String)
    
    return

def Cmd_pub1P(Serial):
    global Cmd_1
    global Pressure_volt
    Command_String = 's'.encode() + CmdtoByte(Cmd_1) + CmdtoByte(Pressure_volt) + 'e'.encode()  

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
            
	    print data
        except Exception as e:
            print e, data           
    return

def move_on_surface(x,y): #地面上平移
    L = math.sqrt(x**2+y**2)
    L1 = link0+link1-up_down_dis
    L2 = link2
    L3 = link3
    L_diagonal = math.sqrt(L1**2+L**2)
    cosR = (L2**2+L3**2-L_diagonal**2)/(2*L2*L3)
    R = math.acos(cosR)
    angle3 = -(math.pi - R)
    a = math.acos(L1/L_diagonal)
    b = math.asin(L3/L_diagonal*math.sin(R))
    angle2 = -(math.pi - a - b) + math.pi/2
    angle1 = -math.asin(x/L)

    angle3 = angle3 + angle2*0.7##belt transmition of real arm

    # print angle1,angle2,angle3

    global Cmd_1,Cmd_2,Cmd_3
    Cmd_1 = angle1
    Cmd_2 = angle2 
    Cmd_3 = angle3
    # return(angle1,angle2,angle3)
    
    Cmd_pub23(STM_23)
    Cmd_pub1P(STM_1P)

def move_above_plate(x,y): #空中平移
    L = math.sqrt(x**2+y**2)
    L1 = link0+link1-above_dis
    L2 = link2
    L3 = link3
    L_diagonal = math.sqrt(L1**2+L**2)
    cosR = (L2**2+L3**2-L_diagonal**2)/(2*L2*L3)
    R = math.acos(cosR)
    angle3 = -(math.pi - R)
    a = math.acos(L1/L_diagonal)
    b = math.asin(L3/L_diagonal*math.sin(R))
    angle2 = -(math.pi - a - b) + math.pi/2
    angle1 = -math.asin(x/L)

    angle3 = angle3 + angle2*0.7##belt transmition of real arm

    # print angle1,angle2,angle3

    global Cmd_1,Cmd_2,Cmd_3
    Cmd_1 = angle1
    Cmd_2 = angle2 
    Cmd_3 = angle3

    # return(angle1,angle2,angle3)
    
    Cmd_pub23(STM_23)
    Cmd_pub1P(STM_1P)

def z_direction_move(x,y,z): #垂直地面上下移動
    L = math.sqrt(x**2+y**2)
    L1 = link0 + link1 - z###need to check
    L2 = link2
    L3 = link3
    L_diagonal = math.sqrt(L1**2+L**2)
    cosR = (L_diagonal**2-L2**2-L3**2)/(-2*L2*L3)
    R = math.acos(cosR)##
    angle3 = -(math.pi - R)
    a = math.acos(L1/L_diagonal)
    b = math.asin(L3/L_diagonal*math.sin(R))##law of sines
    angle2 = -(math.pi - a - b) + math.pi/2 ## +math.pi/2 is and offset in real arm , set arm start point
    angle1 = -math.asin(x/L)

    angle3 = angle3 + angle2*0.7##belt transmition of real arm
    
    # print angle1,angle2,angle3

    global Cmd_1,Cmd_2,Cmd_3
    Cmd_1 = angle1
    Cmd_2 = angle2 
    Cmd_3 = angle3
    # return(angle1,angle2,angle3)
    
    Cmd_pub23(STM_23)
    Cmd_pub1P(STM_1P)

##########################################
def move_on_R(x,y): #地面上平移
    L = math.sqrt(x**2+y**2)
    L1 = 0.0
    L2 = link2
    L3 = link3
    # L_diagonal = math.sqrt(L1**2+L**2)
    
    angle1 = -math.asin(x/L)
    angle2 = 0.0
    angle3 = 0.0##belt transmition of real arm

    # print angle1,angle2,angle3

    global Cmd_1,Cmd_2,Cmd_3
    Cmd_1 = angle1
    Cmd_2 = angle2 
    Cmd_3 = angle3
    # return(angle1,angle2,angle3)
    
    Cmd_pub23(STM_23)
    Cmd_pub1P(STM_1P)


process_time = 0##how many times did the program run
    
    
if __name__ == '__main__' :
 
    rospy.init_node('Com_STM32_INTERFACE',anonymous= True)
    rate=rospy.Rate(100) # 100hz
        
    try:
        
        STM_1P = Connect_STM(COM_Name1P, BAUTRATE)
        STM_23 = Connect_STM(COM_Name23, BAUTRATE)
        
        if  (STM_1P != 'Error' and STM_23 != 'Error'):
            
            t_1P = threading.Thread(target=Read_data, args=(STM_1P,))
            t_1P.start()
            t_23 = threading.Thread(target=Read_data, args=(STM_23,))
            t_23.start()
            while not rospy.is_shutdown():
                # Cmd_pub23(STM)

                # Y = input("繼續=1，否=0:\n")
                # if Y == 1 :             
                    
                    read_in = ['a','a']
                    position = [coordinate(0,0,0),coordinate(0,0,0),coordinate(0,0,0),coordinate(0,0,0)]
                    ##meaningless,just initialize,tell the computer there are 2 and 4 index

                    n=0
                    while n < 2 :
                        read_in[n] = raw_input("position A~I: ")
                        n+=1

                    if read_in[0] == 'A' :
                        position[0] = A[0]
                        position[1] = A[1]

                    elif read_in[0] == 'B' :
                        position[0] = B[0]
                        position[1] = B[1]

                    elif read_in[0] == 'C' :
                        position[0] = C[0]
                        position[1] = C[1]

                    elif read_in[0] == 'D' :
                        position[0] = D[0]
                        position[1] = D[1]

                    elif read_in[0] == 'E' :
                        position[0] = E[0]
                        position[1] = E[1]

                    elif read_in[0] == 'F' :
                        position[0] = F[0]
                        position[1] = F[1]

                    elif read_in[0] == 'G' :
                        position[0] = G[0]
                        position[1] = G[1]

                    elif read_in[0] == 'H' :
                        position[0] = H[0]
                        position[1] = H[1]

                    elif read_in[0] == 'I' :
                        position[0] = I[0]
                        position[1] = I[1]

                    elif read_in[0] == 'R' :
                        position[0] = R[0]
                        position[1] = R[1]
                        
                    else: 
                        sys.exit("improper input")

                    ###

                    if read_in[1] == 'A' :
                        position[2] = A[1]
                        position[3] = A[0]

                    elif read_in[1] == 'B' :
                        position[2] = B[1]
                        position[3] = B[0]

                    elif read_in[1] == 'C' :
                        position[2] = C[1]
                        position[3] = C[0]

                    elif read_in[1] == 'D' :
                        position[2] = D[1]
                        position[3] = D[0]

                    elif read_in[1] == 'E' :
                        position[2] = E[1]
                        position[3] = E[0]

                    elif read_in[1] == 'F' :
                        position[2] = F[1]
                        position[3] = F[0]
                    elif read_in[1] == 'G' :
                        position[2] = G[1]
                        position[3] = G[0]

                    elif read_in[1] == 'H' :
                        position[2] = H[1]
                        position[3] = H[0]

                    elif read_in[1] == 'I' :
                        position[2] = I[1]
                        position[3] = I[0]

                    elif read_in[1] == 'R' :
                        position[2] = R[1]##11/28
                        position[3] = R[1]##11/28
                        
                    else: 
                        sys.exit("improper input")


                        #print(x_difference,y_difference,z_difference) 

                    
                    xi = now_position.x
                    yi = now_position.y
                    zi = now_position.z
                    xf = position[0].x
                    yf = position[0].y
                    zf = position[0].z
                    # print 'debug'
                    if  now_position.z != position[0].z :##R[1] to A[0] or A[0] to R[1]
                        ##############11/28###############
                        if   now_position.x == R[1].x:
                            x_difference = (R[0].x - R[1].x)
                            y_difference = (R[0].y - R[1].y)
                            #z_difference = (R[0].z - R[1].z)
                            i=1
                            for i in range(interval_i)  :
                                move_on_R(xi,yi)                                           
                                
                                xi+= x_difference / (interval) #兩點之間切成100格
                                yi+= y_difference / (interval)
                                # print(xi,yi,zi)
                                i+=1
                                time.sleep(time_interval)

                            xi = R[0].x ## let xi totally match xf
                            yi = R[0].y
                            move_on_R(xi,yi)
                            time.sleep(time_interval*3)
                            now_position = R[0]
                        ##############11/28###############
                        x_difference = (position[0].x - now_position.x)
                        y_difference = (position[0].y - now_position.y)
                        z_difference = (position[0].z - now_position.z)
                        # print 'debug'
                        i=1
                        for i in range(interval_i*2)  :
                            z_direction_move(xi,yi,zi)                                           
                            
                            xi+= x_difference / (interval*2) #R[0] point is far away from normal work area
                            yi+= y_difference / (interval*2) #so we set double interval numbers between R and A~I
                            zi+= z_difference / (interval*2) #to avoid motor_input_volt from saturation
                            # print(xi,yi,zi)
                            i+=1
                            time.sleep(time_interval)

                        xi = xf ## let xi totally match xf
                        yi = yf
                        zi = zf
                        z_direction_move(xi,yi,zi)
                        time.sleep(time_interval*3)

                    else :
                        if  now_position.z == above_dis :##== position[0].z
                        # print('haha')
                            x_difference = (position[0].x - now_position.x)
                            y_difference = (position[0].y - now_position.y)
                            # z_difference = (position[0].z - now_position.z)

                            i=1
                            for i in range(interval_i)  :
                                move_above_plate(xi,yi)                                           
                                
                                xi+= x_difference / interval #兩點之間切成100格
                                yi+= y_difference / interval
                                # print(xi,yi,zi)
                                i+=1
                                time.sleep(time_interval)

                            xi = xf ## let xi totally match xf
                            yi = yf
                            move_above_plate(xi,yi)
                            time.sleep(time_interval*3)

                        elif now_position.z == (link0+link1) :##== position[0].z
                            x_difference = (position[0].x - now_position.x)
                            y_difference = (position[0].y - now_position.y)
                            # z_difference = (position[0].z - now_position.z)

                            i=1
                            for i in range(interval_i)  :
                                move_on_R(xi,yi)                                           
                                
                                xi+= x_difference / (interval) #兩點之間切成100格
                                yi+= y_difference / (interval)
                                # print(xi,yi,zi)
                                i+=1
                                time.sleep(time_interval)

                            xi = xf ## let xi totally match xf
                            yi = yf
                            move_on_R(xi,yi)
                            time.sleep(time_interval*3)
            #######################################################

                    j = 0
                    while j < 3 :
                        xi = position[j].x
                        xf = position[j+1].x
                        yi = position[j].y
                        yf = position[j+1].y
                        zi = position[j].z
                        zf = position[j+1].z
                        x_difference = (position[j+1].x - position[j].x)
                        y_difference = (position[j+1].y - position[j].y)
                        z_difference = (position[j+1].z - position[j].z)

                        if zi == zf == up_down_dis:##moving on the surface of the plate
                            i=1
                            for i in range(interval_i)  :##
                                move_on_surface(xi,yi)

                                xi+= x_difference / interval
                                yi+= y_difference / interval
                                # print(xi,yi,zi)
                                i+=1
                                time.sleep(time_interval)

                            xi = xf ## let xi totally match xf
                            yi = yf
                            move_on_surface(xi,yi)
                            time.sleep(time_interval*3)
                               
                        elif zi != zf :
                            i=1
                            for i in range(interval_i)  :
                                z_direction_move(xi,yi,zi)
                                
                                xi+= x_difference / interval #兩點之間切成100格
                                yi+= y_difference / interval
                                zi+= z_difference / interval
                                # print(xi,yi,zi)
                                i+=1
                                time.sleep(time_interval)
                            xi = xf ## let xi totally match xf
                            yi = yf
                            zi = zf
                            z_direction_move(xi,yi,zi)
                            time.sleep(time_interval*3)

                        elif zi == zf == R[0].z :
                            i=1
                            for i in range(interval_i*2)  :
                                move_on_R(xi,yi)
                                
                                xi+= x_difference / (interval*2) #兩點之間切成100格
                                yi+= y_difference / (interval*2)
                                # print(xi,yi)
                                i+=1
                                time.sleep(time_interval)
                            xi = xf ## let xi totally match xf
                            yi = yf
                        
                            move_on_R(xi,yi)
                            time.sleep(time_interval*3)
                            print 'go to reset'
                        else :
                            sys.exit("error")

                        # print j 
                        j+=1
                        
                    
                    now_position = position[3]
                    print 'now position:',read_in[1]
                    process_time+=1
                    print 'the program has run ',process_time,' times'
                    
                
                # else:
                #     sys.exit("see you")

            rate.sleep()
        
            Stop_flag = 0
            STM_1P.close()
            STM_23.close()
            print 'ROS bye!' 
            sys.exit()   
            
    except: 
        print('Some error!bye!')
        sys.exit()

    


##2021.11.20.17:54
##reset: insert R twice
##axis 3 controller can be improved
##

 
