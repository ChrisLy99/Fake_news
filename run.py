import sys
import os

sys.path.insert(0, 'src')

import env_setup
from etl import get_data
from utils import load_config, convert_notebook
from eda import generate_stats
from dataset import Tweet_Dataset # TODO change Tweet_Dataset params


def main(targets):
    """Runs the main project pipeline project, given targets.
    
    Currently only accepts 'data'
    
    Todo:
        basically the whole project
        
    """
    env_setup.make_datadir()
    
    # set up symbolic link to data on dsmlp
    env = load_config("config/env_dsmlp.yaml")
    if os.path.exists(env["dst"]):
        pass
    else:
        os.symlink(**env) # data_path -> "data/temp/2020-03-22_2020-08-01_ids.jsonl"
        
    config_path, data_folder = "config/data_params.yaml", "data/temp"
    
    if 'data' and 'model' in targets:
        config = load_config("config/data_params.yaml")
        get_data(**config)
        data = Tweet_Dataset(config_path, data_folder)
        
    if 'eda' in targets:
        config = load_config('config/eda_params.yaml')
        
        try:
            data
        except NameError:
            data = Tweet_Dataset(config_path, data_folder)

        generate_stats(data, **config)
        
        # execute notebook / convert to html
        convert_notebook(**config)
    

if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
    