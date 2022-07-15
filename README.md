# RobotArmSim

* **myNotes is some reference**------（optional)

* **block_for_arm is model (.stl) for gazebo**------(needed)


* **There are three ros packages**
  * 1.myrobot_control------(needed)
  * 2.myrobot_gazebo------(needed)
  * 3.my_robot_description------(needed)
  
  After downloded the needed files into your /catkin_ws/src,<br />
  ~/catkin_ws$ ```catkin_make```
  
  ```
  sudo apt-get install python-pip
  pip install --upgrade setuptools 
  ```
  (pip install --upgrade pip)(skip the WARNING) <br />
  
  `pip install getkey` <br />
  
  `sudo apt-get install ros-melodic-ros-control ros-melodic-ros-controllers`(gazebo_ros_plugins) <br />
  `sudo apt-get install ros-melodic-joint-state-publisher-gui` <br />
  (for roslaunch myrobot_description myrobot_rviz.launch) <br />
  
  `gedit ~/.ignition/fuel/config.yaml` <br />
  (change "api.ignitionfuel.org" with "fuel.ignitionrobotics.org") <br />
   ```
   mkdir ~/.gazebo/models
   cp -r ~/catkin_ws/src/block_for_arm ~/.gazebo/models
   ```

  
  
* **ERROR HANDLING** <br />
  
  
  * Gazebo:<br />
  [spawn_gazebo_model-4] process has died <br />
  
   (cause by rosdep permission)<br />
  
   (if you can't run $ `rosdep update` without sudo,<br />
   run $ `sudo rosdep fix-permissions`)<br />
  
