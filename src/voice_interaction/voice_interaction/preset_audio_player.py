import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import os
import sounddevice as sd
import soundfile as sf

from ament_index_python.packages import get_package_share_directory

class Preset_Player_Node(Node):
    def __init__(self):
        super().__init__("preset_audio_player")
        self.audio_dir = os.path.join(get_package_share_directory("voice_interaction", "audios"))
        self.subscriber_ = self.create_subscription(String, "audios", self.subscriber_callback, 10)
        self.get_logger().info("Audio player started!")

    def subscriber_callback(self, msg):
        data, fs = sf.read(str(os.path.join(self.audio_dir, 'audios', msg.data)))
        sd.play(data, fs)
        sd.wait()

def main(args=None):
    rclpy.init(args=args)
    myNode = Preset_Player_Node()
    rclpy.spin(myNode)
    rclpy.shutdown

if __name__=="__main__":
    main()
