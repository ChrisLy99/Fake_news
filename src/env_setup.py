import os
import utils


basedir = os.path.dirname(__file__)
cred_fp = os.path.join(basedir, '..', '.env', 'tweepy.yaml')


def auth():
    '''
    set-up secrets for authentication to tweepy
    '''
    creds = load_config(cred_fp)
    
    os.environ['consumer_key'] = creds['consumer_key']
    os.environ['consumer_secret'] = creds['consumer_secret']
    os.environ['access_token'] = creds['access_token']
    os.environ['access_token_secret'] = creds['access_token_secret']

    return

def make_datadir():

    data_loc = os.path.join(basedir, '..', 'data')

    for d in ['raw', 'temp', 'out']:
        os.makedirs(os.path.join(data_loc, d), exist_ok=True)

    return