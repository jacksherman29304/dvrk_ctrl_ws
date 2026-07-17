from setuptools import find_packages, setup

import os
from glob import glob

package_name = 'utilities'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dvrk-team',
    maintainer_email='jacksherman29304@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'object_loc = utilities.object_loc:main',
            'tool_cmd = utilities.tool_cmd:main',
            'psm1_cmd = utilities.psm1_cmd:main',
            'psm2_cmd = utilities.psm2_cmd:main'
        ],
    },
)
