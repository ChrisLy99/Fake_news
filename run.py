import sys
import os

sys.path.insert(0, 'src')

from data.etl import load_config, get_data_range_p, hydrate_data_range


def main(targets):
    """Runs the main project pipeline project, given targets.
    
    Currently only accepts 'data'
    
    Todo:
        basically the whole project
        
    """
    if 'data' and 'model' in targets:
        config = load_config("config/data_params.yaml")
        get_data_range_p(**config)
        hydrate_data_range(**config)
    

if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
    