import os
from utils import load_config, get_project_root


root = get_project_root()
cred_fp = os.path.join(root, '.env', 'twarc.yaml')

def auth():
    """Set-up secrets for authentication to tweepy."""
    creds = load_config(cred_fp)
    
    os.environ['consumer_key'] = creds['consumer_key']
    os.environ['consumer_secret'] = creds['consumer_secret']
    os.environ['access_token'] = creds['access_token']
    os.environ['access_token_secret'] = creds['access_token_secret']

    return

def make_datadir():
    """Set-up data directories."""

    data_loc = os.path.join(root, 'data')

    for d in ['raw', 'processed', 'report', 'tweets']:
        os.makedirs(os.path.join(data_loc, d), exist_ok=True)

    return