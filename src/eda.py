import os
import numpy as np
import matplotlib.pyplot as plt
import pickle
# import warnings
# from datetime import datetime, timedelta #refactor
# warnings.filterwarnings('ignore')

# sys.path.insert(0,"../src")
# from dataset import Tweet_Dataset


def data_point(data, outdir):
    out = next(data.tweets())
    with open(os.path.join(outdir, 'data_point.pkl'), 'wb') as f:
        pickle.dump(out, f, pickle.HIGHEST_PROTOCOL)
    
def top_10_hashtags(data, outdir):
    tag_counts = data.hashtag_counts()

    most_common_tags = tag_counts.most_common(10)

    tag_labels = [elem[0] for elem in most_common_tags]
    tag_values = [elem[1] for elem in most_common_tags]
    indexes = np.arange(len(tag_labels))
    
    plt.figure()
    plt.bar(tag_labels, tag_values)
    plt.xticks(indexes, tag_labels, rotation='vertical', fontsize=10)
    plt.suptitle('Top 10 Hashtags')
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, 'top_hashtags.png'))
    plt.clf()
    
def top_10_users(data, outdir):
    usr_counts = data.user_name_counts()

    most_common_users = usr_counts.most_common(10)

    usr_labels = [elem[0] for elem in most_common_users]
    usr_values = [elem[1] for elem in most_common_users]
    indexes = np.arange(len(usr_labels))
    
    plt.figure()
    plt.bar(usr_labels, usr_values)
    plt.xticks(indexes, usr_labels, rotation='vertical', fontsize=10)
    plt.suptitle('Top 10 Most Posting Users')
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, 'top_users.png'))
    plt.clf()
    
def hashtag_time(data, outdir):
    daily_tag_occurrences = data.get_daily_tag_counts()
    
    for hashtag in ['Covid19', 'WearAMask', 'SocialDistancing', 'FakeNews', 'Hoax', 'ChinaVirus']:
        count = daily_tag_occurrences[hashtag]
        plot_hashtag_use(outdir, count, hashtag)
    
def plot_hashtag_use(outdir, counts, hashtag):
    dates, frequencies = zip(*sorted(counts.items()))
    
    plt.figure()
    plt.xticks(rotation='vertical')
    plt.suptitle(f'Occurrences of #{hashtag}')
    plt.plot(dates,frequencies)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, f'{hashtag}.png'))
    plt.clf()

def generate_stats(data, outdir, **kwargs):
    
    os.makedirs(outdir, exist_ok=True)
    data_point(data, outdir)
    top_10_hashtags(data, outdir)
    top_10_users(data, outdir)
    hashtag_time(data, outdir)
    
    return