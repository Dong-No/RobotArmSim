# RobotArmSim

**myNotes is some reference------（optional)

**block_for_arm is model (.stl) for gazebo------(needed)


**There are three ros packages**
  * 1.myrobot_control------(needed)
  * 2.myrobot_gazebo------(needed)
  * 3.my_robot_description------(needed)
  
  After downloded the needed files into your /catkin_ws/src,<br />
  '''~/catkin_ws$ catkin_make'''
  
  
  sudo apt-get install python-pip <br />
  pip install --upgrade setuptools <br />
  (pip install --upgrade pip)(skip the WARNING) <br />
  
  pip install getkey <br />
  
  sudo apt-get install ros-melodic-ros-control ros-melodic-ros-controllers <br />
  (for roslaunch myrobot_gazebo myrobot.launch) <br />
  sudo apt-get install ros-melodic-joint-state-publisher-gui <br />
  (for roslaunch myrobot_description myrobot_rviz.launch) <br />
  
  gedit ~/.ignition/fuel/config.yaml <br />
  (change "api.ignitionfuel.org" with "fuel.ignitionrobotics.org") <br />
  
