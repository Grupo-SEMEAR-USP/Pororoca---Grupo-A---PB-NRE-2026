from launch import LaunchDescription

from launch_ros.actions import Node


def generate_launch_description():

    voice_synth_node = Node(
        package="voice_interaction",
        executable="voice_synthesizer"
    )

    return LaunchDescription(
        voice_synth_node,
    )