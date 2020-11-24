# import yaml
import os
import json
from collections import Counter
from datetime import datetime

class Tweet_Dataset:
    
    def __init__(self, filepath):
        '''params: config file path, path to folder containing data'''
#         self.config = self.load_config(config_path)
#         self.start_date = self.config['start_date']
#         self.end_date = self.config['end_date']
#         data_file = self.start_date + '_' + self.end_date + '_ids.jsonl'
#         self.jsonl_path = data_folder + "/" + data_file
        self.data = filepath
        
        # helper function to get the hashtags in a given tweet
        self.get_twt_hashtags = lambda twt: [tag['text'] for tag in twt['entities']['hashtags']]
        
#     def get_start_date(self):
#         return datetime.strptime(self.start_date, '%Y-%m-%d')
    
#     def get_end_date(self):
#         return datetime.strptime(self.end_date, '%Y-%m-%d')
    
#     def load_config(self, config_path):
#         """Load the configuration from config."""
#         return yaml.load(open(config_path, 'r'), Loader=yaml.SafeLoader)

    def tweets(self):
        '''
        an iterator for the tweets
        
        use this by doing the following: 
            data_generator = tweet_dataset.tweets()
            tweet = next(data_generator)
        '''
        for line in open(self.data):
            dic = json.loads(line)
            dic = self.clean_tweet(dic)
            yield dic
    
    def hashtag_counts(self):
        '''returns a collections.Counter object for a dict of # counts'''
#         gen = self.tweets()
#         hashtag_counts = {}
#         while True:
#             try:
#                 twt = next(gen)
#                 for tag in twt['entities']['hashtags']:
#                     if tag['text'] not in hashtag_counts:
#                         hashtag_counts[tag['text']] = 1
#                     else:
#                         hashtag_counts[tag['text']] += 1
#             except StopIteration:
#                 break
#         return Counter(hashtag_counts)
        cnt = Counter()
        for twt in self.tweets():
            tags = self.get_twt_hashtags(twt)
            cnt.update({tag:1 for tag in tags})
        return cnt
    
    def user_id_counts(self):
        '''returns a collections.Counter object for a dict of user counts'''
#         gen = self.tweets()
#         user_counts = {}
#         while True:
#             try:
#                 twt = next(gen)
#                 usr_id = twt['user']['id_str']
#                 if usr_id not in user_counts:
#                     user_counts[usr_id] = 1
#                 else:
#                     user_counts[usr_id] += 1
#             except StopIteration:
#                 break
#         return Counter(user_counts)
        cnt = Counter()
        for twt in self.tweets():
            uid = twt['user']['id_str']
            cnt.update({uid:1})
        return cnt
    
    def user_name_counts(self):
        '''returns a collections.Counter object for a dict of user counts'''
#         gen = self.tweets()
#         user_counts = {}
#         while True:
#             try:
#                 twt = next(gen)
#                 usr_name = twt['user']['screen_name']
#                 if usr_name not in user_counts:
#                     user_counts[usr_name] = 1
#                 else:
#                     user_counts[usr_name] += 1
#             except StopIteration:
#                 break
#         return Counter(user_counts)
        cnt = Counter()
        for twt in self.tweets():
            u_name = twt['user']['screen_name']
            cnt.update({u_name:1})
        return cnt
    
    def get_day_tag_count(self, hashtag, day):
        '''returns the count of a hashtag on a given day
        params: hashtag, date, and Tweet_Dataset object
        date format: 10-31-2020, or datetime object
        '''
        if isinstance(day, str):
            day = datetime.strptime('03-22-2020', '%m-%d-%Y')
        
#         gen = self.tweets()
#         count = 0
#         while True:
#             try:
#                 twt = next(gen)
#                 hashtags = self.get_hashtags(twt) # using lambda function made in __init__
#                 if hashtag in hashtags:
#                     if twt['created_at'].date() == date.date():
#                         count += 1
#             except StopIteration:
#                 break
#         return count
        cnt = 0
        for twt in self.tweets():
            if twt['created_at'].date() == day.date():
                tags = self.get_twt_hashtags(twt)
                if hashtag in tags:
                    cnt += 1
        return cnt
#     lambda twt: [elem['text'] for elem in twt['entities']['hashtags']]
    
    def get_daily_tag_counts(self):
        '''returns the counts of each hashtag by date'''
#         gen = self.tweets()
#         daily_tag_occurrences = {} # {tag: {date: value}}
#         while True:
#             try:
#                 twt = next(gen)
#                 twt_date = twt['created_at'].date()
#                 hashtags = self.get_hashtags(twt)
#                 for tag in hashtags:
#                     if tag in daily_tag_occurrences:
#                         if twt_date in daily_tag_occurrences[tag]:
#                             daily_tag_occurrences[tag][twt_date] += 1
#                         else:
#                             daily_tag_occurrences[tag][twt_date] = 1
#                     else:
#                         daily_tag_occurrences[tag] = {twt_date: 1}
#             except StopIteration:
#                 break
#         return daily_tag_occurrences
        cnt = {}  # {tag: {date: value}}
        for twt in self.tweets():
            twt_date = twt['created_at'].date()
            tags = self.get_twt_hashtags(twt)
            for tag in tags:
                cnt_tag = cnt.setdefault(tag, {})
                tag_date = cnt[tag].setdefault(twt_date, 0)
                cnt_tag[twt_date] = cnt_tag[twt_date]+1 if tag_date else 1
        return cnt
    
    def __len__(self):
#         num_tweets = 0
#         gen = self.tweets()
#         while True:
#             try:
#                 twt = next(gen)
#                 num_tweets += 1
#             except StopIteration:
#                 break
#         return num_tweets
        with open(self.data) as f:
            num_twts = sum(1 for _ in f)
        return num_twts
    
    def clean_tweet(self, twt_dic):
        '''pre processing on the tweets'''
        twt_dic['created_at'] = datetime.strptime(twt_dic['created_at'], '%a %b %d %X %z %Y')
        return twt_dic
