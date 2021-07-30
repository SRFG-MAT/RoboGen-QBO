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

# SD Card Images
In addition to this repository: hardware-specific changes to Q.Bo and OS changes are stored in 16GB and 32GB SD-Card images on a local harddrive: in case you ever need these backups to restore an older Q.Bo-version please contact "SRFG-MAT"

## steps for first installation
- install Ubuntu/Debian and ROS (Ubuntu 18 with ROS Melodic OR Ubuntu 16 with ROS Kinetic; for Raspbian use alternative install guide below)
- create a catkin workspace (see the steps below)
- clone this repository into the workspace's src directory
- clone other, required repositories into the src directory
- [OPTIONAL] execute "rosdep install -i --from-paths src" from the workspace to install ROS dependencies
- [OPTIONAL] execute "rosdep install -y --from-paths src --ignore-src --rosdistro kinetic -r --os=debian:stretch"
- execute "catkin_make" from the workspace to build all packages in the workspace

## steps to create the catkin workspace with ROS
1) mkdir –p ~/catkin_ws/src
2) cd ~/catkin_ws/src
3) catkin_init_workspace
4) cd ~/catkin_ws/
5) catkin_make
6) source ~/catkin_ws/devel/setup.bash
7) echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
8) catkin_create_pkg beginner_tutorials std_msgs rospy roscpp
9) HINT: If you want to also use a python based action server follow the instructions here: http://docs.ros.org/en/hydro/api/catkin/html/user_guide/setup_dot_py.html

## alternative install guide
if the above steps did not work try the following tutorial instead:
http://wiki.ros.org/ROSberryPi/Installing%20ROS%20Kinetic%20on%20the%20Raspberry%20Pi

## start with
"rosrun robogenqbo [name_of_python_file.py]"

## access with
- package_name = "robogenqbo"
- IP-Address: "192.168.48.177"
- to check for connectivity try steps: http://wiki.ros.org/ROS/NetworkSetup
