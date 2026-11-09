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

    voice_synth_node = Node(
        package="voice_interaction",
        executable="voice_synthesizer"
    )

    audio_player_node = Node(
        package="voice_interaction",
        executable="preset_audio_player"
    )

    voice_command_processing_node = Node(
        package="voice_interaction",
        executable="voice_command_processing"
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
        voice_synth_node,
        audio_player_node,
        voice_command_processing_node,
        identification_node,
        navigation_node
    ])