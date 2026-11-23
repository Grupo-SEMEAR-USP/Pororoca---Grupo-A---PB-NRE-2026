import rclpy
import datetime
from rclpy.node import Node
from rclpy.action import ActionClient

from std_msgs.msg import String
from wallington_interfaces.msg import SpeechRecognition
from wallington_interfaces.action import AudioOutput

class voice_command_processing_node(Node):
    def __init__(self):
        super().__init__("voice_command_processing")
        self.voice_sub = self.create_subscription(SpeechRecognition, "voice_commands", self.pick_voice_callback,10)
        self.tts_client = ActionClient(self, AudioOutput, 'audio_output')
        self.audio_pub = self.create_publisher(String, "audios", 10)
        self.movement_pub = self.create_publisher(String, "movement_action", 10)
        self.id_state = 0

    def call_tts_server(self, msg):
        while not self.tts_client.wait_for_server(1.0):
            self.get_logger().warn('Waiting for audio output server')

        goal = AudioOutput.Goal()
        goal.text = msg

        future = self.tts_client.send_goal_async(goal)
        future.add_done_callback(self.process_tts_response)

    def process_tts_response(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('TTS goal rejected...')
            return
        self.get_logger().info('TTS goal accepted!')

    def pick_voice_callback(self, msg):
        if self.id_state == 0:
            self.identify_callback(self, msg)
        else:
            self.command_callback(self, msg)

    def identify_callback(self, msg):
        data = ''
        if not msg.is_recognized:
            data = msg.partial_result
        else:
            data = msg.final_result

        if(data == 'wally'):
            self.get_logger().info('Call identified')
            self.call_tts_server('Olá! Em que posso ajudar?')
            self.id_state = 1

    def command_callback(self, msg):
        data = ''
        if not msg.is_recognized:
            data = msg.partial_result
        else:
            data = msg.final_result
        match(data):
            case 'horas' | 'oração':
                time = datetime.datetime.now()
                self.get_logger().info('Time request identified')
                if(time.hour == 1):
                    self.call_tts_server(f'São {time.hour} hora e {time.minute} minutos')
                elif(time.minute == 1):
                    self.call_tts_server(f'São {time.hour} horas e {time.minute} minuto')
                else:   
                    self.call_tts_server(f'São {time.hour} horas e {time.minute} minutos')
                self.id_state = 0

            case 'você':
                self.get_logger().info('Description request identified')
                self.call_tts_server(f'Eu sou o Wallington, um robô ambiental interativo! Eu fui criado no grupo Semear em 2026, e posso te ajudar a identificar plantas e solos')
                self.id_state = 0

            case 'goku':
                audio = String()
                audio.data = 'goku.wav'
                self.audio_pub.publish(audio)
                self.id_state = 0

            case 'esponja':
                audio = String()
                audio.data = 'bob_esponja.wav'
                self.audio_pub.publish(audio)
                self.id_state = 0

            case 'amarelo':
                color = String()
                color.data = 'yellow'
                self.movement_pub.publish(color)
                self.id_state = 0

            case 'vermelho':
                color = String()
                color.data = 'red'
                self.movement_pub.publish(color)
                self.id_state = 0

            case 'azul':
                color = String()
                color.data = 'blue'
                self.movement_pub.publish(color)
                self.id_state = 0

def main(args=None):
    rclpy.init(args=args)
    myNode = voice_command_processing_node()
    rclpy.spin(myNode)
    rclpy.shutdown()

if __name__ == "__main__":
    main()