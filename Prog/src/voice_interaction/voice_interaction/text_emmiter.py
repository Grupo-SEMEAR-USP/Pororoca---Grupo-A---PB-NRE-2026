#!~/ros2_ws/src/voice_interaction/.venv/bin/python

import rclpy
from rclpy.node import Node

from example_interfaces.msg import String # Importa tipo de dados das interfaces padrões do ROS. Tem como criar suas prórpias(tipo uma struct(eu acho)), mas n sei ainda

class text_emmiter(Node):
    def __init__(self):
        super().__init__("text_emmiter")

        self.publisher_ = self.create_publisher(String, "fala_wally", 10) # Cria um publisher, que joga as informações no topic "robot_news"
        self.timer_ = self.create_timer(0.5, self.publishLine_)
        self.get_logger().info("Started publisher!")

    def publishLine_(self):
        msg = String() # Cria uma mensagem do tipo string, que carrega a msg no atributo data
        msg.data = "Fala muito maneira para solicitar para o Wally" # Coloca mensagem na mensagem (senão fudeu)
        self.publisher_.publish(msg) # Publica


def main(args=None):
    rclpy.init(args=args)
    myNode = text_emmiter()
    rclpy.spin(myNode)
    rclpy.shutdown()

if __name__ == "__main__":
    main()