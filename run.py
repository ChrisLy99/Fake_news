import sys
import os
import subprocess

sys.path.insert(0, 'src')

from data.etl import load_config, get_data_date


def main(targets):
    """Runs the main project pipeline project, given targets.
    
    Currently only accepts 'data'
    
    Todo:
        basically the whole project
        
    """
    if 'data' in targets:
        # config file should be in root of the repository
        config = load_config("./config/config.yaml")
        get_data_date(**config)
    

if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
    