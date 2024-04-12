#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Spawn

class TurtleControl(Node):
    def __init__(self):
        super().__init__('turtle_control')
        self.publisher_ = self.create_publisher(Twist, 'turtle2/cmd_vel', 10)
        self.subscription_pose1 = self.create_subscription(Pose, 'turtle1/pose', self.pose1_callback, 10)
        self.subscription_pose2 = self.create_subscription(Pose, 'turtle2/pose', self.pose2_callback, 10)
        self.current_pose1 = None
        self.current_pose2 = None

    def pose1_callback(self, msg):
        self.current_pose1 = msg
        self.move_turtle2_along_x()

    def move_turtle2_along_x(self):
        if self.current_pose2 is not None:
            twist_msg = Twist()
            twist_msg.linear.x = self.current_pose1.x - self.current_pose2.x  # Move to align x-coordinate with turtle1
            twist_msg.linear.y = 0.0  # Ensure no motion in y-direction
            twist_msg.angular.z = 0.0  # Ensure straight line motion
            self.publisher_.publish(twist_msg)

    def pose2_callback(self, msg):
        self.current_pose2 = msg

def spawn_turtle(node):
    spawn_entity_client = node.create_client(Spawn, '/spawn')
    while not spawn_entity_client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('Service not available, waiting again...')
    req = Spawn.Request()
    req.name = 'turtle2'
    req.x = 5.0
    req.y = 2.0  # Spawning turtle2 on the y=2 line
    req.theta = 0.0
    future = spawn_entity_client.call_async(req)
    rclpy.spin_until_future_complete(node, future)

    if future.result() is not None:
        node.get_logger().info('Turtle spawned successfully')
    else:
        node.get_logger().error('Failed to spawn turtle')

def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('spawn_turtle_node')
    spawn_turtle(node)  # Automatically spawn turtle2
    turtle_control = TurtleControl()
    rclpy.spin(turtle_control)
    turtle_control.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

