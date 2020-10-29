import yaml
import os
import subprocess
import pandas as pd


def get_data_date(date, out_dir, clean=False):
    '''
    Retrieves data for the given day from the internet and places it in src/data.

    'clean' specifies whether to download the cleaned data (without retweets) or the raw data
    '''

    dailies_path = 'https://raw.githubusercontent.com/thepanacealab/covid19_twitter/master/dailies/'
    day_path = dailies_path + date + '/'
    if clean:
        file_name = date + '_clean-dataset.tsv.gz'
    else:
        file_name = date + '-dataset.tsv.gz'
    # https://raw.githubusercontent.com/thepanacealab/covid19_twitter/master/dailies/2020-03-27/2020-03-27-dataset.tsv.gz
    file_url = day_path + file_name

    curl_command = "curl " + file_url + " --output " + out_dir + '/' + file_name
    file_path = out_dir + '/' + file_name
    subprocess.run(curl_command, shell=True)
    subprocess.run("gunzip " + file_path, shell=True)
    data_table = pd.read_csv(file_path[:-3], sep='\t') # [:-3] removes ".gz" from the file path since its been unzipped
    data_table = data_table['tweet_id'] # getting only the tweet ids
    # saving to txt
    data_table.to_csv(file_path[:-7] + '.txt', header=None, index=None, sep=' ', mode='a') # [:-7] removes .tsv.gz
    # so now src/data should have a tsv file and a txt file for the data on the given date

    # hydration of tweet ids
    hydrate_command = "twarc hydrate " + file_path[:-7] + '.txt' + " > " + file_path[:-7] + ".jsonl"
    subprocess.run(hydrate_command, shell=True)

def load_config(path):
    """
    Load the configuration from config.yaml.
    """
    return yaml.load(open(path, 'r'), Loader=yaml.SafeLoader)