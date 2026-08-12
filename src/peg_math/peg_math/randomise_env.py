from ruamel.yaml import YAML as yml
from pathlib import Path
import random

# # fixed x,y,z offsets for blocks sitting on pegs
# offsets = {
#     'x': -0.0001,
#     'y': 0.0,
#     'z': 0.02009
# }

# # fixed peg positions
# peg_pos = {
#     'peg1': {'x': 0.03352, 'y': 0.23481, 'z': 0.7089},
#     'peg2': {'x': 0.07571, 'y': 0.24574, 'z': 0.70891},
#     'peg3': {'x': 0.07577, 'y': 0.22395, 'z': 0.70891},
#     'peg4': {'x': 0.04203, 'y': 0.24581, 'z': 0.70891},
#     'peg5': {'x': 0.0589, 'y': 0.26063, 'z': 0.70891},
#     'peg6': {'x': 0.05889, 'y': 0.20927, 'z': 0.70891},
#     'peg7': {'x': 0.02455, 'y': 0.25263, 'z': 0.70891},
#     'peg8': {'x': 0.02458, 'y': 0.23483, 'z': 0.70891},
#     'peg9': {'x': 0.02456, 'y': 0.21708, 'z': 0.70891},
#     'peg10': {'x': 0.04203, 'y': 0.22389, 'z': 0.70891},
#     'peg12': {'x': -0.00473, 'y': 0.2527, 'z': 0.70891},
#     'peg13': {'x': -0.00466, 'y': 0.23481, 'z': 0.70891},
#     'peg14': {'x': -0.0047, 'y': 0.21708, 'z': 0.70891}
# }

# # active blocks assigned peg
# blocks = {
#     'block2': {'peg': 'peg2'},
#     'block5': {'peg': 'peg7'}
# }

# # generate 2 random pegs from peg list
# pegs = list(peg_pos)
# sample = random.sample(pegs, k=2)

# # assign random peg to each of the blocks and update dictionary
# blocks['block2']['peg'] = sample[0]
# blocks['block5']['peg'] = sample[1]

# # open pegboard_asymmetric.yaml file to alter environment
# doc = Path('/home/dvrk-team/dvrk_ctrl_ws/src/peg_sim/ADF/Phantoms/Pegboards/pegboard_asymmetric.yaml')
# yaml = yml(typ='rt') # round-trip - preserves comments etc.d
# with open(doc) as fp:
#     data = yaml.load(fp)


# for block, block_pos in blocks.items():
#     assigned_peg = block_pos['peg'] # grab new peg name
#     new_pos = peg_pos[assigned_peg] # grab position of new peg

#     existing_pos = data[f'BODY {block}']['location']['position'] # grab existing position x,y,z of block from yaml

#     for coord in ('x', 'y', 'z'): # iterate through x,y,z updating new values + offset
#         existing_pos[coord] = new_pos[coord] + offsets[coord]

# out_path = Path('/home/dvrk-team/dvrk_ctrl_ws/src/peg_sim/ADF/Phantoms/Pegboards/pegboard_asymmetric_out.yaml')
# with open(out_path, 'w') as fp: # write back to yaml
#     yaml.dump(data, fp)


# input_path = yaml to edit
# output_path = save to new location or make the same as input to overwrite

def randomise_env(input_path, output_path, chosen_blocks = ['block2', 'block5'], x_off=None, y_off=None, z_off=None, seed=None):

    i = Path(input_path)
    o = Path(output_path)

    if x_off is not None and y_off is not None and z_off is not None:
        offsets = {
        'x': x_off,
        'y': y_off,
        'z': z_off
        }

    else:
        # fixed x,y,z offsets for blocks sitting on pegs
        offsets = {
            'x': -0.0001,
            'y': 0.0,
            'z': 0.02009
        }

    if seed is not None:
        random.seed(seed)

    # fixed peg positions
    peg_pos = {
        'peg1': {'x': 0.03352, 'y': 0.23481, 'z': 0.7089},
        'peg2': {'x': 0.07571, 'y': 0.24574, 'z': 0.70891},
        'peg3': {'x': 0.07577, 'y': 0.22395, 'z': 0.70891},
        'peg4': {'x': 0.04203, 'y': 0.24581, 'z': 0.70891},
        'peg5': {'x': 0.0589, 'y': 0.26063, 'z': 0.70891},
        'peg6': {'x': 0.05889, 'y': 0.20927, 'z': 0.70891},
        'peg7': {'x': 0.02455, 'y': 0.25263, 'z': 0.70891},
        'peg8': {'x': 0.02458, 'y': 0.23483, 'z': 0.70891},
        'peg9': {'x': 0.02456, 'y': 0.21708, 'z': 0.70891},
        'peg10': {'x': 0.04203, 'y': 0.22389, 'z': 0.70891},
        'peg12': {'x': -0.00473, 'y': 0.2527, 'z': 0.70891},
        'peg13': {'x': -0.00466, 'y': 0.23481, 'z': 0.70891},
        'peg14': {'x': -0.0047, 'y': 0.21708, 'z': 0.70891}
    }


    # dictionary of blocks with associated peg
    blocks = {block: {'peg': None} for block in chosen_blocks}
    
    # generate 2 random pegs from peg list
    pegs = list(peg_pos)
    sample = random.sample(pegs, k=2)

    # assign random peg to each of the blocks and update dictionary
    blocks['block2']['peg'] = sample[0]
    blocks['block5']['peg'] = sample[1]

    # open pegboard_asymmetric.yaml file to alter environment
    doc = Path(i)
    yaml = yml(typ='rt') # round-trip - preserves comments etc.d
    with open(doc) as fp:
        data = yaml.load(fp)


    for block, block_pos in blocks.items():
        assigned_peg = block_pos['peg'] # grab new peg name
        new_pos = peg_pos[assigned_peg] # grab position of new peg

        existing_pos = data[f'BODY {block}']['location']['position'] # grab existing position x,y,z of block from yaml

        for coord in ('x', 'y', 'z'): # iterate through x,y,z updating new values + offset
            existing_pos[coord] = new_pos[coord] + offsets[coord]

    out_path = Path(o)
    with open(out_path, 'w') as fp: # write back to yaml
        yaml.dump(data, fp)