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
        self.intersect_x = None

    def pose1_callback(self, msg):
        self.current_pose1 = msg
        self.calculate_intersection()
        self.control_turtle()

    def pose2_callback(self, msg):
        self.current_pose2 = msg

    def calculate_intersection(self):
        # Calculate the intersection point between turtle1's trajectory and the line y=2
        if self.current_pose1 is not None:
            self.intersect_x = self.current_pose1.x

    def control_turtle(self):
        if self.current_pose2 is not None and self.intersect_x is not None:
            twist_msg = Twist()
            if self.current_pose2.x < self.intersect_x:
                twist_msg.linear.x = 2.0  # Move forward
            else:
                twist_msg.linear.x = 0.0  # Stop at intersection point
            self.publisher_.publish(twist_msg)

def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('spawn_turtle_node')
    def spawn_turtle():
        nonlocal node
        spawn_entity_client = node.create_client(Spawn, '/spawn')
        while not spawn_entity_client.wait_for_service(timeout_sec=1.0):
            node.get_logger().info('Service not available, waiting again...')
        req = Spawn.Request()
        req.name = 'turtle2'
        req.x = 5.0
        req.y = 2.0
        req.theta = 0.0
        future = spawn_entity_client.call_async(req)
        rclpy.spin_until_future_complete(node, future)
        if future.result() is not None:
            node.get_logger().info('Turtle spawned successfully')
        else:
            node.get_logger().error('Failed to spawn turtle')

    spawn_turtle()
    turtle_control = TurtleControl()
    rclpy.spin(turtle_control)
    turtle_control.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

