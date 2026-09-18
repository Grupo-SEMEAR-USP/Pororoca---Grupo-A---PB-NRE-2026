from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    voice_synth_node = Node(
        package="voice_interaction",
        executable="voice_synthesizer"
    )

    ld.add_action(voice_synth_node)
    return ld