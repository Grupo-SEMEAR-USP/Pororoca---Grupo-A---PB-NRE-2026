#!~/ros2_ws/.venv/bin/python

import rclpy
from rclpy.node import Node

from piper import PiperVoice
import sounddevice as sd
import os
from ament_index_python.packages import get_package_share_directory

from wallington_interfaces.msg import AudioOutput

package_dir = get_package_share_directory('voice_interaction')
model_dir = os.path.join(package_dir, "voice_model", "wendel.onnx")

voice = PiperVoice.load(str(model_dir)) #Rodando em um modelo de peso médio. Se travar na rasp, da até pra puxar um modelo mais leve
voice.config.length_scale = 1


class Voice_Synth_Node(Node):
    def __init__(self):
        super().__init__("voice_synthesizer")

        self.subscriber_ = self.create_subscription(AudioOutput, "voice_output", self.callback_voice_synth_, 10)
        self.get_logger().info("Synth Started!")

    def callback_voice_synth_(self, msg):
        stream = sd.OutputStream(samplerate=voice.config.sample_rate, channels=1, dtype= 'int16') #Garante que as sample rates coincidem na hora de produzir a voz e jogar pra stream
        stream.start()

        if(msg.text_to_speech != ""):
            text = msg.text_to_speech

            self.get_logger().info(msg.text_to_speech)

            for chunk in voice.synthesize(text): #Escreve em chunks
                stream.write(chunk.audio_int16_array)

        stream.stop()
        stream.close()

def main(args=None):
    rclpy.init(args=args)
    myNode = Voice_Synth_Node()
    rclpy.spin(myNode)
    rclpy.shutdown()


if __name__ == "__main__":
    main()