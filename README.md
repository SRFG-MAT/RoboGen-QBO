# RoboGen-QBO
Holds all python projects of QBO One Robot ("opt/qbo"-folder on Raspberry Pi 3)

Currently features:
- EmotionAnalysis of Faces in VideoStreams
- EmotionAnalysis of Sentences in Audio-Communications
- DecisionTrees imported from Alexa, but ran locally
- All functionality used on Q.Bo One to control Head, Mouth, Nose and Ears
- Bluetooth-Connection adapter to tablet android app
- Saved personal Settings
- Sample Python-Scripts from TheCorpora
- ROS Action Server implementation with self-registry feature

Info: Autorun-Information on Q.Bo One can be found in main info.txt file (please keep this info file updated if you add any autostart scripts)

## SD Card Images
In addition to this repository: hardware-specific changes to Q.Bo and OS changes are stored in 16GB and 32GB SD-Card images on a local harddrive: in case you ever need these backups to restore an older Q.Bo-version please contact "SRFG-MAT"

## preconditions for first installation
- installed OS on QBO: Debian/Stretch 
- installed ROS on QBO: ROS Kinetic
- for Raspbian install, try to use alternative install guide: http://wiki.ros.org/ROSberryPi/Installing%20ROS%20Kinetic%20on%20the%20Raspberry%20Pi
- this project uses a python based action server following the instructions here: http://docs.ros.org/en/hydro/api/catkin/html/user_guide/setup_dot_py.html
- this project requires as a dependency: actionlib git-repo (https://github.com/ros/actionlib / branch: indigo-devel)
- this project requires rosdep installation following: https://wiki.ros.org/rosdep

## steps to create the catkin workspace with ROS
1) "mkdir –p /opt/QBO/catkin_ws/src"
2) "cd /opt/QBO/catkin_ws/src"
3) "catkin_init_workspace"
4) checkout this git repo in the src-dir
5) checkout the actionlib git repo (https://github.com/ros/actionlib / branch: indigo-devel) in the src-dir
6) "cd ~/catkin_ws/"
7) "catkin_make" (first build of actionlib will take some time)
8) "source /opt/QBO/catkin_ws/devel/setup.bash"
9) "echo "source /opt/QBO/catkin_ws/devel/setup.bash" >> ~/.bashrc"
10) "catkin_create_pkg beginner_tutorials std_msgs rospy roscpp"
11) [OPTIONAL] "rosdep install -i --from-paths /opt/QBO/catkin_ws" (from workspace)
12) [OPTIONAL] "rosdep install -y --from-paths /opt/QBO/catkin_ws --ignore-src --rosdistro kinetic -r --os=debian:stretch" (from workspace)

## start with
1) "roscore"
2) "rosrun robogenqbo [name_of_python_file.py]"

## access with
- package_name = "robogenqbo"
- IP-Address: "192.168.48.177"
- to check for connectivity try steps: http://wiki.ros.org/ROS/NetworkSetup
