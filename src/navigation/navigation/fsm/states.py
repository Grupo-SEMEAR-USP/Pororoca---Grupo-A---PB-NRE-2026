from navigation.fsm.base_state import BaseState
from rclpy.time import Time
from rclpy.constants import S_TO_NS

class IdleState(BaseState):
    def on_enter(self, blackboard):
        node_logger = blackboard['logger']
        node_logger.info('Entering IDLE state: waiting for movement commands')
        blackboard['ang_vel'] = 0.0
        blackboard['lin_vel'] = 0.0

    def execute(self, blackboard):
        possible_objects = ['yellow', 'blue', 'red']
        if blackboard.get('object_searching') in possible_objects:
            return 'SEARCHING'
        return None

class SearchingState(BaseState):
    def on_enter(self, blackboard):
        node_logger = blackboard['logger']
        node_logger.info('Entering SEARCH state')
        blackboard['ang_vel'] = 0.5
        blackboard['lin_vel'] = 0.0

    def execute(self, blackboard):
        if(abs(blackboard['msg'].range-blackboard['last_range']) >= 0.5 and blackboard['msg'].range <= 5):
            blackboard['t0'] = Time.from_msg(blackboard['msg'].header.stamp).nanoseconds / S_TO_NS
            return 'IDENTIFYING'
        
        return None

    def on_exit(self, blackboard):
        node_logger = blackboard['logger']
        node_logger.info('Exiting SEARCH state')
        blackboard['ang_vel'] = 0.0
        blackboard['lin_vel'] = 0.0

class IdentifyingState(BaseState):
    def on_enter(self, blackboard):
        node_logger = blackboard['logger']
        node_logger.info('Entering ID state')
        blackboard['ang_vel'] = 0.5
        blackboard['lin_vel'] = 0.0
        blackboard['id_func'](blackboard.get('object_searching'))

    def execute(self, blackboard):
        if(abs(blackboard['msg'].range-blackboard['last_range']) >= 0.5 ):
            if(blackboard['found_object']):
                blackboard['tf'] = Time.from_msg(blackboard['msg'].header.stamp).nanoseconds / S_TO_NS
                return 'ALIGNING'
            else:
                return 'SEARCHING'
        return None

class AligningState(BaseState):
    def on_enter(self, blackboard):
        node_logger = blackboard['logger']
        node_logger.info('Entering ALIGNMENT state')
        blackboard['ang_vel'] = -0.5
        blackboard['lin_vel'] = 0.0
        blackboard['dt'] = blackboard['tf'] - blackboard['t0']

    def execute(self, blackboard):
        curr_time = Time.from_msg(blackboard['msg'].header.stamp).nanoseconds / S_TO_NS
        if(curr_time >= blackboard['tf']+blackboard['dt']):
            return 'APPROACHING'
        return None

class ApproachingState(BaseState):
    def on_enter(self, blackboard):
        node_logger = blackboard['logger']
        node_logger.info('Entering APPROACH state')
        blackboard['ang_vel'] = 0.0
        blackboard['lin_vel'] = 0.5

    def execute(self, blackboard):
        if(blackboard['msg'].range <= 0.5):
            blackboard['object_searching'] = ''
            return 'IDLE'
        if blackboard['last_range'] -  blackboard['msg'].range >= 1:
            blackboard['obstacle_distance'] = blackboard['last_range']
            return 'WAITING'
        if blackboard['msg'].range - blackboard['last_range']>= 1:
            blackboard['obstacle_distance'] = blackboard['last_range']
            return 'SEARCHING'
        return None

class WaitingObstacleState(BaseState):
    def on_enter(self, blackboard):
        node_logger = blackboard['logger']
        node_logger.info('Entering WAIT state')
        blackboard['ang_vel'] = 0.0
        blackboard['lin_vel'] = 0.0

    def execute(self, blackboard):
        if(abs(blackboard['msg'].range - blackboard['obstacle_distance']) <= 0.25):
            return 'APPROACHING'