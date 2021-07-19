#!/bin/bash

set -e

source ${WORKSPACE_DIR}/devel/setup.bash

cd ${WORKSPACE_DIR}/src

catkin_create_pkg ${PKG_NAME} actionlib message_generation roscpp rospy std_msgs actionlib_msgs

#sed '/add_action_files/s/# //g' 


# create / insert code like here: https://wiki.ros.org/actionlib_tutorials/Tutorials/SimpleActionServer%28ExecuteCallbackMethod%29
cp ${WORKSPACE_DIR}/src/${PKG_NAME}/CMakeLists.txt ${WORKSPACE_DIR}/src/${PKG_NAME}/CMakeLists.txt.bak
cp ${ROS_HOME}/CMakeLists.src.txt ${WORKSPACE_DIR}/src/${PKG_NAME}/CMakeLists.txt

sed -i 's/\(  <exec_depend>actionlib<\/exec_depend>\)/ \
  <exec_depend>message_generation<\/exec_depend>\
\1/g' ${PKG_NAME}/package.xml

cp -r ${ROS_HOME}/action ${WORKSPACE_DIR}/src/${PKG_NAME}

cp -r ${ROS_HOME}/python/actionlib_tutorials_py ${WORKSPACE_DIR}/src/${PKG_NAME}