import yaml
import os
import json
from collections import Counter
from datetime import datetime

class Tweet_Dataset:
    
    def __init__(self, config_path, data_folder):
        '''params: config file path, path to folder containing data'''
        self.config = self.load_config(config_path)
        self.start_date = self.config['start_date']
        self.end_date = self.config['end_date']
        data_file = self.start_date + '_' + self.end_date + '_ids.jsonl'
        self.jsonl_path = data_folder + data_file
    
    def load_config(self, config_path):
        """Load the configuration from config."""
        return yaml.load(open(config_path, 'r'), Loader=yaml.SafeLoader)

    def tweets(self):
        '''
        an iterator for the tweets
        
        use this by doing the following: 
            data_generator = tweet_dataset.tweets()
            tweet = next(data_generator)
        '''
        for line in open(self.jsonl_path):
            dic = json.loads(line)
            dic = self.clean_tweet(dic)
            yield dic
    
    def hashtag_counts(self):
        '''returns a collections.Counter object for a dict of # counts'''
        gen = self.tweets()
        hashtag_counts = {}
        while True:
            try:
                twt = next(gen)
                for tag in twt['entities']['hashtags']:
                    if tag['text'] not in hashtag_counts:
                        hashtag_counts[tag['text']] = 1
                    else:
                        hashtag_counts[tag['text']] += 1
            except StopIteration:
                break
        return Counter(hashtag_counts)
    
    def __len__(self):
        num_tweets = 0
        gen = self.tweets()
        while True:
            try:
                twt = next(gen)
                num_tweets += 1
            except StopIteration:
                break
        return num_tweets
    
    def clean_tweet(self, twt_dic):
        '''pre processing on the tweets'''
        twt_dic['created_at'] = datetime.strptime(twt_dic['created_at'], '%a %b %d %X %z %Y')
        return twt_dic