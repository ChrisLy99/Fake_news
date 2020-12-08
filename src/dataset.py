import os
import json
from collections import Counter
from datetime import datetime

class Tweet_Dataset:
    
    def __init__(self, filepath):
        '''params: config file path, path to folder containing data'''
        self.data = filepath
        
        # helper function to get the hashtags in a given tweet
        self.get_twt_hashtags = lambda twt: [tag['text'] for tag in twt['entities']['hashtags']]

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
        cnt = Counter()
        for twt in self.tweets():
            tags = self.get_twt_hashtags(twt)
            cnt.update({tag:1 for tag in tags})
        return cnt
    
    def user_id_counts(self):
        '''returns a collections.Counter object for a dict of user counts'''
        cnt = Counter()
        for twt in self.tweets():
            uid = twt['user']['id_str']
            cnt.update({uid:1})
        return cnt
    
    def user_name_counts(self):
        '''returns a collections.Counter object for a dict of user counts'''
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
        
        cnt = 0
        for twt in self.tweets():
            if twt['created_at'].date() == day.date():
                tags = self.get_twt_hashtags(twt)
                if hashtag in tags:
                    cnt += 1
        return cnt
    
    def get_daily_tag_counts(self):
        '''returns the counts of each hashtag by date'''
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
        with open(self.data) as f:
            num_twts = sum(1 for _ in f)
        return num_twts
    
    def clean_tweet(self, twt_dic):
        '''pre processing on the tweets'''
        twt_dic['created_at'] = datetime.strptime(twt_dic['created_at'], '%a %b %d %X %z %Y')
        for ht_ent in twt_dic['entities']['hashtags']:
            ht_ent.update({'text': str.lower(ht_ent['text'])})
        return twt_dic
