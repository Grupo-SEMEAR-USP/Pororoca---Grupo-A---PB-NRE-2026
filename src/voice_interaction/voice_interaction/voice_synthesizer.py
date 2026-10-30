#!~/Pororoca---Grupo-A---PB-NRE-2026/.venv/bin/python

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse
from rclpy.executors import MultiThreadedExecutor
from wallington_interfaces.action import AudioOutput

from piper import PiperVoice
import sounddevice as sd
import os
from ament_index_python.packages import get_package_share_directory
import time

package_dir = get_package_share_directory('voice_interaction')
model_dir = os.path.join(package_dir, "voice_model", "wendel.onnx")

class Voice_Synth_Node(Node):
    def __init__(self):
        super().__init__("voice_synthesizer")

        self.action_server_ = ActionServer(self, AudioOutput, "audio_output", 
                                           execute_callback=self.execute_callback_voice_synth_,
                                           goal_callback=self.goal_callback_,
                                           handle_accepted_callback=self.handle_accepted_callback_)
        self.get_logger().info("Synth Started!")

        self.goal_queue_ = []
        self.feedback_frequency_ = 0.5

        self.voice = PiperVoice.load(str(model_dir))
        self.voice.config.length_scale = 1

        self.stream = sd.OutputStream(samplerate=self.voice.config.sample_rate, channels=1, dtype= 'int16') #Garante que as sample rates coincidem na hora de produzir a voz e jogar pra stream
        self.stream.start()

    def goal_callback_(self, goal_request):
        return GoalResponse.ACCEPT

    def handle_accepted_callback_(self, goal_handle):
        self.goal_queue_.append(goal_handle)
        goal_handle.execute()

    def execute_callback_voice_synth_(self, goal_handle): #Note que, com ações, ele começa outra somente após acabar uma.
        msg = goal_handle.request.text
        feedback_msg = AudioOutput.Feedback()

        while goal_handle in self.goal_queue_:
            feedback_msg.position_in_queue = self.goal_queue_.index(goal_handle)
            goal_handle.publish_feedback(feedback_msg)

            if(feedback_msg.position_in_queue == 0):
                break

            time.sleep(1/self.feedback_frequency_)

        self.get_logger().info(msg)

        for chunk in self.voice.synthesize(msg): #Escreve em chunks
            self.stream.write(chunk.audio_int16_array)

        goal_handle.succeed()
        result = AudioOutput.Result()
        result.success = True
        self.goal_queue_.remove(goal_handle)
        return result

def main(args=None):
    rclpy.init(args=args)
    voice_synth_node = Voice_Synth_Node()

    executor = MultiThreadedExecutor()
    executor.add_node(voice_synth_node)
    executor.spin()

    Voice_Synth_Node.stream.stop()
    Voice_Synth_Node.stream.close()
    voice_synth_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()