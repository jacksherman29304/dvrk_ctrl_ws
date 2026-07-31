from ament_index_python.packages import get_package_share_directory
import os
import yaml

def load_config(filename='parameters.yaml'):
    path = os.path.join(get_package_share_directory('peg_task'), 'config', filename)
    with open(path) as file:
        # params = yaml.safe_load(file)

        # # Auto converts position offsets into Vector
        # # Auto converts rotation offsets in Rotation.RPY
        # for phase in ("entrance", "grasp", "lift", "relocate", "place"):
        #     if phase in params and "position_offset" in params[phase]:
        #         params[phase]["position_offset"] = Vector(*params[phase]["position_offset"])
        #     if phase in params and "rotation_offset" in params[phase]:
        #         params[phase]["rotation_offset"] = Rotation.RPY(*params[phase]["rotation_offset"])
 
        # return params
        return yaml.safe_load(file)

