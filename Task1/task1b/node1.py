#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import atan2, pi, sqrt
import random

class TurtleControl(Node):
    def __init__(self):
        super().__init__('turtle_control')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.subscription_pose = self.create_subscription(Pose, 'turtle1/pose', self.pose_callback, 10)
        self.subscription_pose  # prevent unused variable warning
        self.current_pose = None
        self.target_pose = Pose()
        self.set_random_target_pose()  # Set initial random target pose

    def pose_callback(self, msg):
        self.current_pose = msg
        self.control_turtle()

    def set_random_target_pose(self):
        self.target_pose.x = random.uniform(0.0, 11.0)
        self.target_pose.y = random.uniform(0.0, 11.0)
        if self.current_pose is not None:
            self.target_pose.theta = atan2(self.target_pose.y - self.current_pose.y, self.target_pose.x - self.current_pose.x)

    def control_turtle(self):
        if self.current_pose is not None:
            twist_msg = Twist()
            distance = sqrt((self.target_pose.x - self.current_pose.x) ** 2 +
                            (self.target_pose.y - self.current_pose.y) ** 2)
            if distance > 0.1:  # Threshold for stopping
                twist_msg.linear.x = 1.0  # Linear velocity
                twist_msg.angular.z = 0.0  # Ensure straight line motion
            else:
                twist_msg.linear.x = 0.0
                twist_msg.angular.z = 0.0
                # Change target pose after reaching the current target
                self.set_random_target_pose()
            # Bounce off the walls
            if self.current_pose.x <= 0.1 or self.current_pose.x >= 10.9:
                twist_msg.linear.x *= -1  # Reverse linear velocity
            if self.current_pose.y <= 0.1 or self.current_pose.y >= 10.9:
                twist_msg.angular.z = pi  # Reverse direction if hitting a wall
            self.publisher_.publish(twist_msg)

def main(args=None):
    rclpy.init(args=args)
    turtle_control = TurtleControl()
    rclpy.spin(turtle_control)
    turtle_control.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

