import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from navigation.fsm.states import *

from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import Range
from wallington_interfaces.srv import VisionRequest
from wallington_interfaces.action import AudioOutput
from std_msgs.msg import String

class StateMachineNode(Node):
    def __init__(self):
        super().__init__('movement_state_machine')

        self.blackboard = {
            'logger': self.get_logger(),
            'msg': Range(),
            'ang_vel': 0.0,
            'lin_vel': 0.0,
            'object_searching': '',
            'last_range': 0.0,
            't0': 0.0,
            'tf': 0.0,
            'dt': 0.0,
            'id_func': self.call_identification_server,
            'tts_func': self.call_tts_server,
            'found_object': False,
            'obstacle_distance': 0,
        }

        self.states = {
            'IDLE': IdleState(),
            'SEARCHING': SearchingState(),
            'IDENTIFYING': IdentifyingState(),
            'ALIGNING': AligningState(),
            'APPROACHING': ApproachingState(),
            'WAITING': WaitingObstacleState(),
        }

        self.current_state_key = 'IDLE'
        self.states[self.current_state_key].on_enter(self.blackboard)

        self.velocity_pub = self.create_publisher(TwistStamped, "wallington_controller/cmd_vel", 10)
        self.action_sub = self.create_subscription(String, "movement_action", self.action_callback, 10)
        self.ultrasonic_sub = self.create_subscription(Range, "ultrasonic", self.ultrasonic_callback, 10)

        self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        movement_cmd = TwistStamped()
        movement_cmd.header.stamp = self.get_clock().now().to_msg()
        movement_cmd.twist.linear.x = self.blackboard['lin_vel']
        movement_cmd.twist.angular.z = self.blackboard['ang_vel']
        self.velocity_pub.publish(movement_cmd)

    def ultrasonic_callback(self, msg):
        self.blackboard['last_range'] = self.blackboard['msg'].range
        self.blackboard['msg'] = msg
        self.fsm_tick()

    def action_callback(self, msg):
        self.blackboard['object_searching'] = msg.data

    def call_identification_server(self, color):
        client = self.create_client(VisionRequest, "tag_identification")
        while not client.wait_for_service(1.0):
            self.get_logger().warn('Waiting for identification server')

        request = VisionRequest.Request()
        request.color = color

        future = client.call_async(request=request)
        future.add_done_callback(lambda f: self.process_id_result(f))

    def process_id_result(self, future):
        try:
            response = future.result()
            found = response.answer  
            self.get_logger().info(f"Server returned: {found}")

            self.blackboard['found_object'] = found
            
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")

    def call_tts_server(self, msg):
        client = ActionClient(self, AudioOutput, 'audio_output')

        while not client.wait_for_server(1.0):
            self.get_logger().warn('Waiting for audio output server')

        goal = AudioOutput.Goal()
        goal.text = msg

        future = client.send_goal_async(goal)
        future.add_done_callback(self.process_tts_response)

    def process_tts_response(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('TTS goal rejected...')
            return
        self.get_logger().info('TTS goal accepted!')

    def fsm_tick(self):
        current_state_obj = self.states[self.current_state_key]
        next_state_key = current_state_obj.execute(self.blackboard)

        if next_state_key is not None and next_state_key != self.current_state_key:
            if next_state_key in self.states:
                current_state_obj.on_exit(self.blackboard)

                self.current_state_key = next_state_key

                self.states[self.current_state_key].on_enter(self.blackboard)
            else:
                self.get_logger().error('Attempted to enter unexisting state!')

def main(args=None):
    rclpy.init(args=args)
    node_object = StateMachineNode()
    rclpy.spin(node_object)
    rclpy.shutdown

if __name__=="__main__":
    main()