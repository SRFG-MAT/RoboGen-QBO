#!/bin/bash

set -e

export WORKSPACE_DIR=${ROS_HOME}/${1:-"action_ws"}
export PKG_NAME=${2:-"actionlib_tutorials_interfaces"}

echo "removing ${WORKSPACE_DIR} recursively!"
rm -rf ${WORKSPACE_DIR}

cd ${ROS_HOME}

./create_ws.sh ${WORKSPACE_DIR}
./create_pkg.sh ${WORKSPACE_DIR}

cd ${WORKSPACE_DIR}

catkin_make

source ${WORKSPACE_DIR}/devel/setup.bash

echo "starting roscore"
roscore &

echo "starting fibonacci_action_server"
rosrun ${PKG_NAME} fibonacci_action_server.py