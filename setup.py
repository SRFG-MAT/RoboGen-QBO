# this file will reuse all information from your package.xml file
# and extend it with required dependencies for ROS python
# dont install this file directly, instead it will be found and
# installed automatically by adding the "catkin_python_setup()"-
# entry to your CMakeLists.txt project file
from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['robogenqbo'], #same as name in package.xml!!
    #install_requires=['rospy', 'actionlib'], #external packages as dependencies are already defined in package.xml
    scripts=[
        'scripts/python/QBO_action_server_py',
        'scripts/python/RoboGen_Projects'
    ] 
    #package_dir={'': 'src'}
)

setup(**d)