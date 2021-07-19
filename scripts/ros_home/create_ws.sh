#!/bin/bash

set -e

source /opt/ros/${ROS_DISTRO}/setup.bash
mkdir -p ${WORKSPACE_DIR}/src

cd ${WORKSPACE_DIR}/src

echo "initialise "`pwd`

catkin_init_workspace

cd ${WORKSPACE_DIR}/

catkin_make

