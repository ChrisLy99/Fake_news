import sys
import os

sys.path.insert(0, 'src')

from data.etl import load_config, get_data_date


def main(targets):
    """Runs the main project pipeline project, given targets.
    
    Currently only accepts 'data'
    
    Todo:
        basically the whole project
        
    """
    if 'data' in targets:
        config = load_config("config/data_params.yaml")
        data = get_data_date(**config)
    

if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
    