from ament_index_python.packages import get_package_share_directory
import os
import yaml

def load_config(filename='parameters.yaml'):
    path = os.path.join(get_package_share_directory('peg_task'), 'config', filename)
    with open(path) as file:
        return yaml.safe_load(file)

