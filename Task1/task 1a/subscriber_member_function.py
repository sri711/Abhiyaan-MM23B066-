import rclpy
from rclpy.node import Node
from std_msgs.msg import String
class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            '/start_here',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.subscription2 = self.create_subscription(
            String,
            '/You_are_welcome',
            self.welcome_callback,
            10)
        self.subscription2  # prevent unused variable warning

        self.subscription3 = self.create_subscription(
            String,
            '/Pasta_way',
            self.welcome3_callback,
            10)
        self.subscription3  # prevent unused variable warning

        self.subscription4 = self.create_subscription(
            String,
            '/Bison',
            self.welcome4_callback,
            10)
        self.subscription4  # prevent unused variable warning

        self.subscription5 = self.create_subscription(
            String,
            '/Oops',
            self.welcome5_callback,
            10)
        self.subscription5  # prevent unused variable warning

        self.subscription6 = self.create_subscription(
            String,
            '/Rebooted',
            self.welcome6_callback,
            10)
        self.subscription6  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard in start here: "%s"' % msg.data)

    def welcome_callback(self, msg):

        self.get_logger().info('I heard in you r welcome: "%s"' % msg.data)

    def welcome3_callback(self, msg):

        self.get_logger().info('I heard in Pasta_way: "%s"' % msg.data)

    def welcome4_callback(self, msg):

        self.get_logger().info('I heard in Bison: "%s"' % msg.data)

    def welcome5_callback(self, msg):

        self.get_logger().info('I heard in Oops "%s"' % msg.data)

    def welcome6_callback(self, msg):

        self.get_logger().info('I heard in Rebooted: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':

    main()