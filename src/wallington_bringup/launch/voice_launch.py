from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    stt_node = Node(
        package="voice_interaction",
        executable="stt_node"
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

    return LaunchDescription([
        stt_node,
        voice_synth_node,
        audio_player_node,
        voice_command_processing_node
    ])