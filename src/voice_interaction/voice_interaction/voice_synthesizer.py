#!~/ros2_ws/.venv/bin/python

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from wallington_interfaces.action import AudioOutput

from piper import PiperVoice
import sounddevice as sd
import os
from ament_index_python.packages import get_package_share_directory

package_dir = get_package_share_directory('voice_interaction')
model_dir = os.path.join(package_dir, "voice_model", "wendel.onnx")

class Voice_Synth_Node(Node):
    def __init__(self):
        super().__init__("voice_synthesizer")

        self.action_server_ = ActionServer(self, AudioOutput, "audio_output", self.callback_voice_synth_)
        self.get_logger().info("Synth Started!")

        self.voice = PiperVoice.load(str(model_dir))
        self.voice.config.length_scale = 1
        self.stream = sd.OutputStream(samplerate=self.voice.config.sample_rate, channels=1, dtype= 'int16') #Garante que as sample rates coincidem na hora de produzir a voz e jogar pra stream
        self.stream.start()

    def callback_voice_synth_(self, goal_handle): #Note que, com ações, ele começa outra somente após acabar uma.
        msg = goal_handle.request.text

        self.get_logger().info(msg)

        for chunk in self.voice.synthesize(msg): #Escreve em chunks
            self.stream.write(chunk.audio_int16_array)

        goal_handle.succeed()
        result = AudioOutput.Result()
        result.success = True
        return result

def main(args=None):
    rclpy.init(args=args)
    myNode = Voice_Synth_Node()
    rclpy.spin(myNode)
    rclpy.shutdown()
    Voice_Synth_Node.stream.stop()
    Voice_Synth_Node.stream.close()


if __name__ == "__main__":
    main()