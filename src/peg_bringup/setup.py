from setuptools import find_packages, setup

import os 
from glob import glob

package_name = 'peg_bringup'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dvrk-team',
    maintainer_email='jacksherman29304@gmail.com',
    description='Launch files, parameters and startup checks for the full system.',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'ambf_live = peg_bringup.ambf_live:main',
            'crtk_live = peg_bringup.crtk_live:main'
        ],
    },
)
