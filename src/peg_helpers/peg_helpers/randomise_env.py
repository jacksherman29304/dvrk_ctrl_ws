from ruamel.yaml import YAML as yml
from pathlib import Path
import random

### This script builds N-1 test environment configurations
### Randomly allocates target pegs using random seed and edits YAML file accordingly
### Run this file using python3 -m randomise_env in this directory - will create N-1 test config YAML files and save to target output path

N = 6
SEED = 51224
OUTPUT_PATH = '/home/dvrk-team/dvrk_ctrl_ws/src/peg_sim/ADF/Phantoms/Pegboards'

# fixed x,y,z offsets for blocks sitting on pegs
offsets = {
    'x': -0.0001,
    'y': 0.0,
    'z': 0.02009
}

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


# generate 2 random pegs from peg list
pegs = list(peg_pos)

# Random seed

random.seed(SEED)


# 5 tetst configurations
for test_no in range(1,N):
    sample = random.sample(pegs, k=2)
    # assign random peg to each of the blocks and update dictionary
    blocks = {
        'block2': {'peg': sample[0]},
        'block5': {'peg': sample[1]}
    }
    
    print(f"test_{test_no}: {sample}")

    # open pegboard_asymmetric.yaml file to alter environment
    doc = Path('/home/dvrk-team/dvrk_ctrl_ws/src/peg_sim/ADF/Phantoms/Pegboards/pegboard_asymmetric.yaml')

    yaml = yml(typ='rt') # round-trip - preserves comments etc.d
    with open(doc) as fp:
        data = yaml.load(fp)

    for block, block_pos in blocks.items():
        assigned_peg = block_pos['peg'] # grab new peg name
        new_pos = peg_pos[assigned_peg] # grab position of new peg

        existing_pos = data[f'BODY {block}']['location']['position'] # grab existing position x,y,z of block from yaml

        for coord in ('x', 'y', 'z'): # iterate through x,y,z updating new values + offset
            existing_pos[coord] = new_pos[coord] + offsets[coord]

    # append test number file name to end of output path
    output_path = Path(OUTPUT_PATH)
    output_path = output_path / f'test_{test_no}.yaml'

    # write new yaml file to output path
    with open(output_path, 'w') as fp:
        yaml.dump(data, fp)

    print(f"  Saved: {output_path}")
