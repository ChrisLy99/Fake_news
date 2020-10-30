import yaml
import os
import subprocess
import numpy as np

def get_data_date(date, outdir, clean=False, N=None):
    """Retrieves data for the given day from the internet and places it in src/data.

    Args:
        date (str): format YYYY-MM-DD
        outdir (str): data directory path
        clean (bool): specifies whether to download the cleaned data (without retweets) or the raw data
        
    Todo:
        Retrieve data if it exists else download it
        
    """
#     try:
#         # read in data e.g.
#         np.genfromtxt('data/2020-10-02/tweet_ids.txt', dtype=np.int64)
#     except:
    if clean:
        file_name = date + '_clean-dataset.tsv.gz'
    else:
        file_name = date + '-dataset.tsv.gz'
        
    data_url_base_path = 'https://raw.githubusercontent.com/thepanacealab/covid19_twitter/master/dailies/' + date
    
    # https://raw.githubusercontent.com/thepanacealab/covid19_twitter/master/dailies/2020-03-27/2020-03-27-dataset.tsv.gz
    file_url = os.path.join(data_url_base_path, file_name)
    file_path = os.path.join(outdir, file_name) # ./data/raw/2020-03-27-dataset.tsv.gz
    file_tsv_path = os.path.splitext(file_path)[0] # removes ".gz" from the file path
    file_txt_path = os.path.splitext(file_tsv_path)[0] + '.txt' # replace ".tsv" from the file path with ".txt"
    file_jsonl_path = os.path.splitext(file_tsv_path)[0] + '.jsonl' # replace ".tsv" from the file path with ".jsonl"
    
    curl_command = "curl " + file_url + " --output " + file_path
    
    subprocess.run(curl_command, shell=True)
    subprocess.run("gunzip " + file_path, shell=True)
    
    twitter_ids = np.genfromtxt(file_tsv_path, dtype=np.int64, skip_header=1, usecols=(0,))
    np.savetxt(file_txt_path, twitter_ids, fmt='%i')
    # so now src/data should have a tsv file and a txt file for the data on the given date

    # hydration of tweet ids
    hydrate_command = "twarc hydrate " + file_txt_path + " > " + file_jsnol_path
    subprocess.run(hydrate_command, shell=True)

def load_config(path):
    """
    Load the configuration from config.yaml.
    """
    return yaml.load(open(path, 'r'), Loader=yaml.SafeLoader)
