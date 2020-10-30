import os
import subprocess
import numpy as np
import yaml
import json
# import pandas as pd

# TODO: add twarc authentification

def get_data_date(date, outdir, clean=False, N=500):
    """Retrieves N tweets for the given day.
    
    Retrieves N tweets from existing file. If it doesn't exist then sample
    N tweets from file containing all tweet IDs for the given day. And if
    that file also doesn't exist, fetch it from the github and create them.
       
    Args:
        date (str): date of data. Format YYYY-MM-DD.
        outdir (str): data directory path.
        clean (bool): specifies whether to download the cleaned data 
          (without retweets) or the raw data.
        N (int): number of tweets to hydrate, if None hydrate all.
        
    Returns:
        A list containing N tweet json objects.
        
    """
    file_txt_path = os.path.join(outdir, date) + f'_{N}_ids.txt'     # ./data/raw/2020-03-27_500_ids.txt
    file_jsonl_path = os.path.splitext(file_txt_path)[0] + '.jsonl'  # replace ".txt" from the file path with ".jsonl"
    
    try:
        return read_jsonl(file_jsonl_path)
    except FileNotFoundError:  # jsonl file doesn't exist for N sample
        pass
    try:
        # read in full data to sample from
        full_data_path = os.path.join(outdir, date) + '_all_ids.txt' # ./data/raw/2020-03-27_all_ids.txt
        twitter_ids = np.genfromtxt(full_data_path, dtype=np.int64)  
        
        sample_idx = np.random.uniform(high=len(twitter_ids), size=N).astype(np.int64)
        sample = twitter_ids[sample_idx]
        np.savetxt(file_txt_path, sample, fmt='%i')
        
        hydrate_ids(file_txt_path, file_jsonl_path)
        return read_jsonl(file_jsonl_path)
    except:  # full data doesn't exist
        if clean:
            file_name = date + '_clean-dataset.tsv.gz'
        else:
            file_name = date + '-dataset.tsv.gz'

        url_base = 'https://raw.githubusercontent.com/thepanacealab/covid19_twitter/master/dailies/' + date

        # https://raw.githubusercontent.com/thepanacealab/covid19_twitter/master/dailies/2020-03-27/2020-03-27-dataset.tsv.gz
        url = os.path.join(url_base, file_name)
        gz_path = os.path.join(outdir, file_name) # ./data/raw/2020-03-27-dataset.tsv.gz
        
        curl_command = "curl " + url + " --output " + gz_path

        subprocess.run(curl_command, shell=True)
        # subprocess.run("gunzip " + gz_path, shell=True)
        
        # np.genfromtxt decompresses .gz by default
        twitter_ids = np.genfromtxt(gz_path, dtype=np.int64, skip_header=1, usecols=(0,))
        np.savetxt(full_data_path, twitter_ids, fmt='%i')
        
        os.remove(gz_path)

        sample_idx = np.random.uniform(high=len(twitter_ids), size=N).astype(np.int64)
        sample = twitter_ids[sample_idx]
        np.savetxt(file_txt_path, sample, fmt='%i')
        
        hydrate_ids(file_txt_path, file_jsonl_path)
        return read_jsonl(file_jsonl_path)

def read_jsonl(jsonl_path):
    """Returns a list of tweet json objects."""
    data = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data
                
def hydrate_ids(txt_path, jsonl_path):
    """Hydrate the tweet IDs in txt_path using twarc"""
    hydrate_command = "twarc hydrate " + txt_path + " > " + jsonl_path
    subprocess.run(hydrate_command, shell=True)

def load_config(path):
    """Load the configuration from config.yaml."""
    return yaml.load(open(path, 'r'), Loader=yaml.SafeLoader)
