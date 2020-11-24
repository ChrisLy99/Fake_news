import os
import subprocess
import numpy as np

import json
from datetime import timedelta


# TODO: add twarc authentification

def get_data(start_date, end_date, outdir, clean=False, p=360):
    """Downloads tweets for the days between start and end dates.
    
    Dates range from start_date inclusive to end_date exclusive. Attempts
    downloading data if data file doesn't already exist.
       
    Args:
        start_date (str): start of data range. Format YYYY-MM-DD.
        end_date (str): end of data range. Format YYYY-MM-DD.
        outdir (str): data directory path.
        clean (bool): specifies whether to download the cleaned data 
          (without retweets) or the raw data.
        
    """
    parent_dir = os.path.dirname(outdir)
    file_txt_path = os.path.join(parent_dir, 'temp', start_date) + f'_{end_date}_ids.txt'  # ./data/temp/2020-03-27_2020-03-30_ids.txt
    file_jsonl_path = os.path.splitext(file_txt_path)[0] + '.jsonl'
    
    if os.path.isfile(file_jsonl_path):
        pass
    else:
        get_data_range_p(start_date, end_date, outdir, clean)
        hydrate_data_range(start_date, end_date, outdir, clean)
    return file_jsonl_path

def get_data_range_p(start_date, end_date, outdir, clean=False, p=360):
    """Downloads tweets for the days between start and end dates.
    
    Dates range from start_date inclusive to end_date exclusive. Attempts
    downloading data if data file doesn't already exist.
       
    Args:
        start_date (str): start of data range. Format YYYY-MM-DD.
        end_date (str): end of data range. Format YYYY-MM-DD.
        outdir (str): data directory path.
        clean (bool): specifies whether to download the cleaned data 
          (without retweets) or the raw data.
        
    """
    parent_dir = os.path.dirname(outdir)
    file_txt_path = os.path.join(parent_dir, 'temp', start_date) + f'_{end_date}_ids.txt'  # ./data/temp/2020-03-27_2020-03-30_ids.txt
    
    if os.path.isfile(file_txt_path):
        return
    else:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
        out = []
        for day in daterange(start, end):
            date_ = day.isoformat()
            try:
                download_data_date(date_, outdir, clean)
                tmp = read_data_date(date_, outdir, clean)
                out = out + list(tmp[::p].copy())  # running list of every p tweet IDs
            except:
                pass
        out = np.array(out)

        np.savetxt(file_txt_path, out, fmt='%i')
    return

def download_data_date(date, outdir, clean=False):
    """Downloads tweets for the given day.
    
    First checks if tweets have already been downloaded. If they haven't,
    then download them and save the tweet IDs to a txt file.
       
    Args:
        date (str): date of data. Format YYYY-MM-DD.
        outdir (str): data directory path.
        clean (bool): specifies whether to download the cleaned data 
          (without retweets) or the raw data.
        
    """
    data_path = os.path.join(outdir, date) + '_all_ids.txt' # ./data/raw/2020-03-27_all_ids.txt
    if os.path.isfile(data_path):
        return
    else:  # full data doesn't exist
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
        try:
            # np.genfromtxt decompresses .gz by default
            twitter_ids = np.genfromtxt(gz_path, dtype=np.int64, skip_header=1, usecols=(0,))
            np.savetxt(data_path, twitter_ids, fmt='%i')
        except:
            pass
        os.remove(gz_path)
    return

def read_data_date(date, outdir, clean=False):
    return np.genfromtxt(f'data/raw/{date}_all_ids.txt', dtype=np.int64)

def hydrate_data_range(start_date, end_date, outdir, clean=False):
    """Sample 1 tweet for every p tweets on the given day.
    
    Hydrates tweets in date range sampling 1 tweet for every p tweets.
    This function should only be run after get_data_range() is called. It
    will save the sampled tweet IDs in another file.
       
    Args:
        start_date (str): start of data range. Format YYYY-MM-DD.
        end_date (str): end of data range. Format YYYY-MM-DD.
        outdir (str): data directory path.
        clean (bool): specifies whether to download the cleaned data 
          (without retweets) or the raw data.
        p (int): rate of tweets to hydrate.
        
    """
    parent_dir = os.path.dirname(outdir)
    file_txt_path = os.path.join(parent_dir, 'temp', start_date) + f'_{end_date}_ids.txt'  # ./data/temp/2020-03-27_2020-03-30_ids.txt
    file_jsonl_path = os.path.splitext(file_txt_path)[0] + '.jsonl'                        # replace ".txt" from the file path with ".jsonl"
    
    hydrate_ids(file_txt_path, file_jsonl_path)

def get_N_data_date(date, outdir, clean=False, N=500):
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
    """Retrieves tweets given IDs in txt_path using twarc"""
    hydrate_command = "twarc hydrate " + txt_path + " > " + jsonl_path
    subprocess.run(hydrate_command, shell=True)

def daterange(start, end):
    """Generator for dates between start and end dates.
    
    ref: https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
    
    Args:
        start (date): start of range inclusive.
        end (date): end of range exclusive.
    
    Yields:
        Next date in range.
        
    """
    for n in range(int((end - start).days)):
        yield start + timedelta(n)
