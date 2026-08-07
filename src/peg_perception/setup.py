from setuptools import find_packages, setup

package_name = 'peg_perception'

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
    maintainer='dvrk-team',
    maintainer_email='jacksherman29304@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'camera_interface = peg_perception.camera_interface:main',
            'pointcloud_test = peg_perception.pointcloud_test:main',
        ],
    },
)
