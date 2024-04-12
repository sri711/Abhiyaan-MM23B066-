from glob import glob
from setuptools import find_packages, setup
package_name = 'new_pckg'  # Replace 'new_pckg' with your actual package name
setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=[
        'setuptools',
        'turtlesim',  # Add any other dependencies here
    ],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'turtle_control = new_pckg.node1:main',
            'nodes2 = new_pckg.node2:main',
        ],
    },
)

