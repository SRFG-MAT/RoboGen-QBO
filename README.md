# RoboGen-QBO
Holds all python projects of QBO One Robot (Documents-folder on Raspberry Pi 3)

Currently features:
- EmotionAnalysis of Faces in VideoStreams
- EmotionAnalysis of Sentences in Audio-Communications
- DecisionTrees imported from Alexa, but ran locally
- All functionality used on Q.Bo One to control Head, Mouth, Nose and Ears
- Bluetooth-Connection adapter to tablet android app
- Saved personal Settings
- Sample Python-Scripts from TheCorpora

Info: Autorun-Information on Q.Bo One can be found in main info.txt file (please keep this info file updated if you add any autostart scripts)

# SD Card Images
In addition to this repository: hardware-specific changes to Q.Bo and OS changes are stored in 16GB and 32GB SD-Card images on a local harddrive: in case you ever need these backups to restore an older Q.Bo-version please contact "SRFG-MAT"

## steps for first installation
- install Ubuntu and ROS
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

## start with
"rosrun TODO"

## access with
package_name = "TODO"
IP-Address: "TODO"
