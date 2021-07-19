#!/bin/bash

set -e

export WORKSPACE_DIR=${ROS_HOME}/${1:-"action_ws"}
export PKG_NAME=${2:-"actionlib_tutorials_interfaces"}

source ${WORKSPACE_DIR}/devel/setup.bash

echo "starting fibonacci_action_client"
rosrun ${PKG_NAME} fibonacci_action_client.py