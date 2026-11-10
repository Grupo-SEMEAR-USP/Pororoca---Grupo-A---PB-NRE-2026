from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory("wallington_description"), "launch"), "/gazebo.launch.py"]),
    )

    voice_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory("wallington_bringup"), "launch"), "/voice_launch.py"]),
    )

    identification_node = Node(
        package="poggers_id_test",
        executable="color_match"
    )

    navigation_node = Node(
        package="navigation",
        executable="movement_state_machine"
    )

    return LaunchDescription([
        gazebo_launch,
        voice_launch,
        identification_node,
        navigation_node
    ])