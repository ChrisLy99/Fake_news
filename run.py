import sys
import os

sys.path.insert(0, 'src')

import env_setup
from etl import get_data_range, download_retweets
from utils import get_project_root, load_config, convert_notebook
from eda import generate_stats, generate_polarity
from dataset import Tweet_Dataset


def main(targets):
    """Runs the main project pipeline project, given targets.
    
    Todo:
        test target, needs 2 tweets for users
        
    """
    root = get_project_root()
    env_setup.make_datadir()
    
    # set up symbolic link to data on dsmlp
    env = load_config("config/env_dsmlp.yaml")
    if os.path.exists(env["dst"]):
        pass
    else:
        os.symlink(**env) # data_path -> "data/temp/2020-03-22_2020-08-01_ids.jsonl"
    
    if 'all' in targets:
        targets = ['data', 'eda']
        
    if 'data' in targets:
        config = load_config("config/data_params.yaml")
        fp = get_data_range(**config)
        data = Tweet_Dataset(fp)
        
    if 'eda' in targets:
        config = load_config('config/eda_params.yaml')
        
        try:
            data
        except NameError:
            data = Tweet_Dataset("data/processed/2020-03-22_2020-08-01_ids.jsonl")

        generate_stats(data, **config)
        
        ht_polarity, base_hts = data.hashtag_polarity()
        for tid,path in config["tids"]:
            download_retweets(tid, path)
            tmp_data = Tweet_Dataset(path)
            generate_polarity(tmp_data, ht_polarity, base_hts, **config)
            
        # execute notebook / convert to html
        convert_notebook(**config)
            
    if 'test' in targets:
        config = load_config("config/test.yaml")
        data = Tweet_Dataset(**config['data'])
        
        generate_stats(data, **config['eda'])
        ht_polarity, base_hts = data.hashtag_polarity()
        for tid,path in config['eda']["tids"]:
            print(path)
            tmp_data = Tweet_Dataset(path)
            generate_polarity(tmp_data, ht_polarity, base_hts, **config['eda'])
            
        convert_notebook(**config['eda'])

if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
    
