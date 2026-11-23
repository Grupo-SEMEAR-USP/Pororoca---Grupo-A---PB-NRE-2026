import rclpy
from rclpy.node import Node
import queue

from wallington_interfaces.msg import SpeechRecognition

from vosk import Model, KaldiRecognizer
import sounddevice as sd
import json
import threading

class stt_node(Node):
    def __init__(self):
        super().__init__("stt_node")

        self.command_pub = self.create_publisher(SpeechRecognition, "voice_commands", 10)

        self.q = queue.Queue()

        self.model = Model("/home/murilo/testes_stt/pt_model") #Modelo leve disponibilizado no site da vosk

        self.input_dev_num = sd.query_hostapis()[0]['default_input_device']
        device_info = sd.query_devices(self.input_dev_num, 'input')
        self.samplerate = int(device_info['default_samplerate'])

        self.recognition_thread = threading.Thread(target=self.speech_recognize, daemon=True)
        self.recognition_thread.start()

    def stream_callback(self, indata, frames, time, status):
        self.q.put(bytes(indata))

    def speech_recognize(self):
        with sd.RawInputStream(samplerate=self.samplerate, blocksize=16000, device=self.input_dev_num, dtype='int16', channels=1, callback=self.stream_callback):
            rec = KaldiRecognizer(self.model, self.samplerate)

            while rclpy.ok():
                data = self.q.get()

                isRecognized = False
                isRecognized_partially = False
                msg = SpeechRecognition()

                if rec.AcceptWaveform(data):
                    result = rec.FinalResult()

                    diction = json.loads(result)
                    lentext = len(diction["text"])

                    if lentext > 2:
                        result_text = diction["text"]
                        self.get_logger().info(result_text)
                        isRecognized = True
                    else:
                        isRecognized = False
                    
                    rec.Reset()
                else:
                    # In case of partial result
                    result_partial = rec.PartialResult()
                    if (len(result_partial) > 2):

                        isRecognized_partially = True
                        partial_dict = json.loads(result_partial)
                        partial = partial_dict["partial"]

                msg.is_recognized = isRecognized
                if isRecognized:
                    msg.final_result = result_text
                    msg.partial_result = ''
                    isRecognized = False
                    self.command_pub.publish(msg)
                elif isRecognized_partially:
                    msg.final_result = ''
                    msg.partial_result = partial
                    isRecognized_partially = False
                    self.command_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    myNode = stt_node()
    rclpy.spin(myNode)
    rclpy.shutdown()

if __name__=="__main__":
    main()