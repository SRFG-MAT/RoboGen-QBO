#!/bin/sh
export ROS_IP="192.168.48.117"
export ROS_MASTER_URI="http://192.168.48.41:11311/"
export ROS_PYTHON_LOG_CONFIG_FILE="/opt/QBO/catkin_ws/src/RoboGen-QBO/logging/logging.conf"
echo "[createEnvVars.sh] Succesfully exported ROS env variables for this terminal"

# Either do every time you open a console:
# ". createEnvVariables.sh"
# Or add this line to home/pi/.bashrc file:
# "source /opt/QBO/catkin_ws/src/RoboGen-QBO/launch/createEnvVars.sh"