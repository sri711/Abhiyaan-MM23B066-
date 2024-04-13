from setuptools import find_packages, setup

package_name = 'pygm'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sriprakash',
    maintainer_email='sriprakash@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	'pygame_node = pygm.race_car:main',
            	'obstacle_publisher = pygm.obstaclesros2:main',
        ],
    },
)
