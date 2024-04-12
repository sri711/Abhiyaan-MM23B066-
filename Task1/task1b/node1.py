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
        self.subscription_pose1 = self.create_subscription(Pose, 'turtle1/pose', self.pose1_callback, 10)
        self.subscription_pose2 = self.create_subscription(Pose, 'turtle2/pose', self.pose2_callback, 10)
        self.current_pose1 = None
        self.current_pose2 = None

    def pose1_callback(self, msg):
        self.current_pose1 = msg
        self.control_turtle()

    def pose2_callback(self, msg):
        self.current_pose2 = msg

    def control_turtle(self):
        if self.current_pose1 is not None and self.current_pose2 is not None:
            twist_msg = Twist()
            twist_msg.linear.x = 1.0  # Linear velocity
            twist_msg.angular.z = 0.0  # Ensure straight line motion
            # Check for collision with other turtle
            distance_to_other_turtle = sqrt((self.current_pose1.x - self.current_pose2.x)**2 + (self.current_pose1.y - self.current_pose2.y)**2)

            if distance_to_other_turtle <= 0.5:  # Adjust this threshold according to your needs
                twist_msg.angular.z = pi 
            # Bounce off the walls
            if self.current_pose1.x <= 0.1 or self.current_pose1.x >= 10.9:
                twist_msg.linear.x *= -1  # Reverse linear velocity
            if self.current_pose1.y <= 0.1 or self.current_pose1.y >= 10.9:
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

