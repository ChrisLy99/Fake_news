import os
import json
from collections import Counter
from datetime import datetime
import utils
import logging


root = utils.get_project_root()
start_date = '2020-03-01'
start_period = datetime.strptime(f"{start_date}-+0000", '%Y-%m-%d-%z')
end_date = '2020-10-01'
end_period = datetime.strptime(f"{end_date}-+0000", '%Y-%m-%d-%z')


class Tweet_Dataset:
    
    def __init__(self, filepath):
        '''params: config file path, path to folder containing data'''
        self.data_ = filepath
        
#         config = utils.load_config('.env/tweepy.yaml')
#         consumer_key, consumer_secret = config['consumer_key'], config['consumer_secret']
#         access_token, access_token_secret = config['access_token'], config['access_token_secret']
        
#         auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#         auth.set_access_token(access_token, access_token_secret)

#         self.api = tweepy.API(auth, wait_on_rate_limit=True)
        
        # helper function to get the hashtags in a given tweet
        self.get_twt_hashtags = lambda twt: [tag['text'] for tag in twt['entities']['hashtags']]
        self.get_lower_hashtags = lambda twt: [str.lower(tag['text']) for tag in twt['entities']['hashtags']]

    def tweets(self):
        '''
        an iterator for the tweets
        
        use this by doing the following: 
            data_generator = tweet_dataset.tweets()
            tweet = next(data_generator)
        '''
        for line in open(self.data_):
            dic = json.loads(line)
            dic = self.clean_tweet(dic)
            yield dic
            
    def tweets_period(self):
        '''
        an iterator for the tweets
        
        use this by doing the following: 
            data_generator = tweet_dataset.tweets()
            tweet = next(data_generator)
        '''
        for line in open(self.data_):
            dic = json.loads(line)
            dic = self.clean_tweet(dic)
            if dic['created_at'] < end_period and dic['created_at'] > start_period:
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
    
    def hashtag_polarity(self, top=200, marker_hts=['wuhanvirus', 'fakenews', 'maga']):
        """Returns the polarities of the top hashtags"""
        ht_cnt = self.hashtag_counts()
        baseline = [(ht,cnt/len(self)) for ht,cnt in ht_cnt.most_common(top)]
        base_hts = [ht for ht,_ in baseline]
        marker_set = [x for x in self.tweets() if self.shares_hashtag(marker_hts, self.get_twt_hashtags(x))]
        ht_cnt_marker = Counter()
        for twt in marker_set:
            tags = self.get_twt_hashtags(twt)
            ht_cnt_marker.update({tag:1 for tag in tags})
        
        ht_polarity = self.polarity(ht_cnt_marker, len(marker_set), baseline)
        return ht_polarity, base_hts
    
    def shares_hashtag(self, x_hts, y_hts):
        return not set(x_hts).isdisjoint(set(y_hts))
    
    def polarity(self, counter, num, baseline):
        return Counter({ht: ((counter.get(ht, 0)/num)-roc)/roc for ht,roc in baseline})
    
    def user_pol(self, ht_polarity, base_hts):
        ht_used = []
        num_contain = 0
        for tweet in self.tweets_period():
            hts = self.get_lower_hashtags(tweet)
            ht_used += hts
            if self.shares_hashtag(hts, base_hts):
                num_contain += 1

        tot = 0
        for ht in list(set(ht_used).intersection(set(base_hts))):
            tot += ht_polarity.get(ht)
        out = 0 if num_contain == 0 else tot / num_contain
        return tot, out

#     # Uses tweepy, old code
#     def user_polarity(screenname, ht_pol, base_hts):
#         startDate = datetime(2020, 3, 1, 0, 0, 0)
#         endDate =   datetime(2020, 10, 1, 0, 0, 0)
#         tweets = []
#         tmpTweets = tweepy.Cursor(self.api.user_timeline, screen_name=screenname, tweet_mode="extended").items()
#         for tweet in tmpTweets:
#             if tweet.created_at < endDate and tweet.created_at > startDate:
#                 tweets.append(tweet)

#         ht_used = []
#         num_contain = 0
#         for tweet in tweets:
#             hts = self.get_twt_hashtags(tweet)
#             ht_used += hts
#             if self.shares_hashtag(hts, base_hts):
#                 num_contain += 1

#         tot = 0
#         for ht in list(set(ht_used).intersection(set(base_hts))):
#             tot += ht_polarity.get(ht)
#         out = 0 if num_contain == 0 else tot / num_contain
#         return out
    
#     def echo_tweet(tid, ht_pol, base_hts):
#         users = []
#         tmpTweets = self.api.retweets(id=tid, count=100)
#         for tweet in tmpTweets:
#             users.append(tweet.user.screen_name)
#         pol = []
#         try:
#             for name in users:
#                 pol.append(self.user_polarity(f'@{name}', ht_pol, base_hts))
#         except:
#             save = np.array([p for p in pol if p!=0])
#             np.savetxt(f'{tid}_save.txt', save)
#         return pol
#         return [self.user_polarity(f'@{name}', ht_pol, base_hts) for name in users]

    def __len__(self):
        with open(self.data_) as f:
            num_twts = sum(1 for _ in f)
        return num_twts
    
    def clean_tweet(self, twt_dic):
        '''pre processing on the tweets'''
        twt_dic['created_at'] = datetime.strptime(twt_dic['created_at'], '%a %b %d %X %z %Y')
        for ht_ent in twt_dic['entities']['hashtags']:
            ht_ent.update({'text': str.lower(ht_ent['text'])})
        return twt_dic
