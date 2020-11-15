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
        
        # helper function to get the hashtags in a given tweet
        self.get_hashtags = lambda twt: [elem['text'] for elem in twt['entities']['hashtags']]
        
    def get_start_date(self):
        return datetime.strptime(self.start_date, '%Y-%m-%d')
    
    def get_end_date(self):
        return datetime.strptime(self.end_date, '%Y-%m-%d')
    
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
    
    def user_id_counts(self):
        '''returns a collections.Counter object for a dict of user counts'''
        gen = self.tweets()
        user_counts = {}
        while True:
            try:
                twt = next(gen)
                usr_id = twt['user']['id_str']
                if usr_id not in user_counts:
                    user_counts[usr_id] = 1
                else:
                    user_counts[usr_id] += 1
            except StopIteration:
                break
        return Counter(user_counts)
    
    def user_name_counts(self):
        '''returns a collections.Counter object for a dict of user counts'''
        gen = self.tweets()
        user_counts = {}
        while True:
            try:
                twt = next(gen)
                usr_name = twt['user']['screen_name']
                if usr_name not in user_counts:
                    user_counts[usr_name] = 1
                else:
                    user_counts[usr_name] += 1
            except StopIteration:
                break
        return Counter(user_counts)
    
    def get_day_tag_count(self, hashtag, date):
        '''returns the count of a hashtag on a given day
        params: hashtag, date, and Tweet_Dataset object
        date format: 10-31-2020, or datetime object
        '''
        if isinstance(date, str):
            date = datetime.strptime('03-22-2020', '%m-%d-%Y')
        
        gen = self.tweets()
        count = 0
        while True:
            try:
                twt = next(gen)
                hashtags = self.get_hashtags(twt) # using lambda function made in __init__
                if hashtag in hashtags:
                    if twt['created_at'].date() == date.date():
                        count += 1
            except StopIteration:
                break
        return count
    
    def get_daily_tag_counts(self):
        '''returns the counts of each hashtag by date'''
        gen = self.tweets()
        daily_tag_occurrences = {} # {tag: {date: value}}
        while True:
            try:
                twt = next(gen)
                twt_date = twt['created_at'].date()
                hashtags = self.get_hashtags(twt)
                for tag in hashtags:
                    if tag in daily_tag_occurrences:
                        if twt_date in daily_tag_occurrences[tag]:
                            daily_tag_occurrences[tag][twt_date] += 1
                        else:
                            daily_tag_occurrences[tag][twt_date] = 1
                    else:
                        daily_tag_occurrences[tag] = {twt_date: 1}
            except StopIteration:
                break
        return daily_tag_occurrences
    
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