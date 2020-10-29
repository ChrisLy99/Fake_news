from src.data.etl import load_config, get_data_date
import yaml
import os
import subprocess
def main():
    # config file should be in root of the repository
    config = load_config("./config/config.yaml")
    get_data_date(config['date'], out_dir='./src/data')
    

if __name__ == '__main__':
    main()