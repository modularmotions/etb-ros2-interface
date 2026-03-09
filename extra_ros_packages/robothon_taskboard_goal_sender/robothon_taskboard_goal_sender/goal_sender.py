import argparse
import random

from action_msgs.msg import GoalStatus
from robothon_taskboard_msgs.action import ExecuteTask
from robothon_taskboard_msgs.msg import Task
from robothon_taskboard_msgs.msg import TaskStep
from robothon_taskboard_msgs.msg import SensorMeasurement
from robothon_taskboard_msgs.msg import ActuatorStep

import rclpy
from rclpy.action import ActionClient
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class RobothonTaskBoardGoalSender(Node):

    def __init__(self, random_order=False):
        super().__init__('minimal_action_client')
        self._action_client = ActionClient(self, ExecuteTask, 'taskboard_execute_task')
        self.random_order = random_order

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback):
        message = 'Feedback: {0}: '.format(feedback.feedback.elapsed_time)
        self.get_logger().info('Received feedback: {0}'.format(message))
        # self.get_logger().info(f'[DEBUG] Test')

    def get_result_callback(self, future):
        result = future.result().result
        status = future.result().status
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Goal succeeded! Result: {0}'.format(result.finish_time))
        else:
            self.get_logger().info('Goal failed with status: {0}'.format(status))

        # Shutdown after receiving a result
        rclpy.shutdown()

    def send_goal(self):
        self.get_logger().info('Waiting for action server...')
        self._action_client.wait_for_server()

        goal_msg = ExecuteTask.Goal()
        goal_msg.human_task = False

        task = Task()
        # task.name = "Test task"
        task.name = "Speed test"

        # Define task steps
        steps = []

        # Press Blue Button
        task_step = TaskStep()
        task_step.sensor_name = "BLUE_BUTTON_LEFT"
        task_step.type = TaskStep.TASK_STEP_TYPE_EQUAL
        task_step.target.type = SensorMeasurement.SENSOR_MEASUREMENT_TYPE_BOOL
        task_step.target.bool_value.append(True)
        print("DEBUG: task step: %s", task_step)
        steps.append(task_step)

        # Turn on Blue Button LED
        task_step = TaskStep()
        task_step.type = TaskStep.TASK_STEP_TYPE_ACTUATOR
        task_step.actuator_name = "blue button led"
        task_step.sensor_name = "Blue Button LED"

        task_step.target.type = ActuatorStep.ACTUATOR_VALUE_TYPE_BOOL
        task_step.state = True
        task_step.target.bool_value.append(True)
        print("DEBUG: task step: %s", task_step)
        steps.append(task_step)

        # # Move fader to 0.5
        # task_step = TaskStep()
        # task_step.sensor_name = "FADER"
        # task_step.type = TaskStep.TASK_STEP_TYPE_EQUAL
        # task_step.target.type = SensorMeasurement.SENSOR_MEASUREMENT_TYPE_ANALOG
        # task_step.target.analog_value.append(0.5)
        # task_step.tolerance = 0.1
        # steps.append(task_step)

        # Press Red Button
        task_step = TaskStep()
        task_step.sensor_name = "RED_BUTTON_RIGHT"
        task_step.type = TaskStep.TASK_STEP_TYPE_EQUAL
        task_step.target.type = SensorMeasurement.SENSOR_MEASUREMENT_TYPE_BOOL
        task_step.target.bool_value.append(True)
        steps.append(task_step)

        # Press Red Button
        task_step = TaskStep()
        task_step.sensor_name = "BLUE_BUTTON_LEFT"
        task_step.type = TaskStep.TASK_STEP_TYPE_EQUAL
        task_step.target.type = SensorMeasurement.SENSOR_MEASUREMENT_TYPE_BOOL
        task_step.target.bool_value.append(True)
        steps.append(task_step)

        # # Press Red Button
        # task_step = TaskStep()
        # task_step.sensor_name = "RED_BUTTON_RIGHT"
        # task_step.type = TaskStep.TASK_STEP_TYPE_WAIT_RANDOM
        # # task_step.target.type = SensorMeasurement.SENSOR_MEASUREMENT_TYPE_BOOL
        # # task_step.target.bool_value.append(True)
        # steps.append(task_step)

        # Shuffle steps if random_order is True
        if self.random_order:
            random.shuffle(steps)

        # Add steps to task
        task.steps.extend(steps)
        goal_msg.task = task

        self.get_logger().info('Sending goal request...')

        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def cancel_goal(self):
        self.get_logger().info('Cancelling goal')
        self._send_goal_future.result().cancel_goal_async()


def main(args=None):
    try:
        parser = argparse.ArgumentParser(description="Send taskboard goals")
        parser.add_argument('--random-order', action='store_true', help="Shuffle the task steps before sending.")
        cli_args = parser.parse_args()

        rclpy.init(args=args)

        goal_sender = RobothonTaskBoardGoalSender(random_order=cli_args.random_order)
        goal_sender.get_logger().info(f'[DEBUG] cli_args.random_order: {cli_args.random_order}')

        goal_sender.send_goal()

        rclpy.spin(goal_sender)
    except (KeyboardInterrupt, ExternalShutdownException):
        goal_sender.cancel_goal()


if __name__ == '__main__':
    main()
