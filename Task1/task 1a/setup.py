from glob import glob
from setuptools import find_packages, setup
package_name = 'capture_the_msg'
setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, glob('launch/*.launch.py')),
    ],

    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yash',
    maintainer_email='yashpurswani4@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ctm = capture_the_msg.ctm:main',
            'listener = capture_the_msg.subscriber_member_function:main',
            'Tanker = capture_the_msg.subscriber_member_function:main',
        ],
    }
)
