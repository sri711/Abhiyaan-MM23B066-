from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='capture_the_msg',
            executable='ctm.py',
            name='ctm'
        )
    ])

