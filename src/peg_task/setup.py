from setuptools import find_packages, setup

package_name = 'peg_task'

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
    description='Sequential task routines for the peg transfer challenge.',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'pick_and_place = peg_task.pick_and_place:main'
        ],
    },
)
