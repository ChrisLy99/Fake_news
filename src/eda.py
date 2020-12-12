import os
import numpy as np
import matplotlib.pyplot as plt
import pickle


from etl import extract_users, download_retweets


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
    
    for hashtag in ['covid19', 'wearamask', 'socialdistancing', 'wuhanvirus', 'fakenews', 'maga']:
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

# # uses tweepy, old code
# def echo_chambers(data, outdir):
#     ht_polarity, base_hts = data.hashtag_polarity()
    
#     for tid in [1241517991843581953, 1241430375496212481]:
#         user_polarities = self.echo_tweet(tid, ht_polarity, base_hts)
#         plot_echo_chambers(outdir, tid, polarity)
        
# def plot_echo_chambers(outdir, tid, polarity):
#     clean = [pol for pol in polarity if pol!=0]
    
#     plt.figure()
#     plt.suptitle(f'Distribution of user polarities retweeting #{tid} (tweet id)')
#     plt.hist(clean)
#     plt.tight_layout()
#     plt.savefig(os.path.join(outdir, f'{tid}.png'))
#     plt.clf()

def echo_chamber(data, outdir, ht_polarity, base_hts, test=False):
    users = extract_users(None, data.data_, test)
    polarities = []
    polarities_n = []
    for user in users:
        pol, pol_norm = user.user_pol(ht_polarity, base_hts)
        if pol != 0:
            polarities.append(pol)
        if pol_norm != 0:
            polarities_n.append(pol_norm)
    base = os.path.splitext(os.path.basename(data.data_))[0]
    path = os.path.join(outdir, base)
    np.savetxt(f'{path}.txt', np.array(polarities))
    np.savetxt(f'{path}_norm.txt', np.array(polarities_n))
    
    plot_echo_chambers(outdir, polarities, base)
    plot_echo_chambers(outdir, polarities_n, base, True)
    
def plot_echo_chambers(outdir, pol, base, norm=False):
    
    plt.figure()
    title = f'Distribution of user polarities from {base} retweets'
    title = f'{title} (normalized)' if norm else title
    plt.suptitle(title)
    plt.hist(pol)
    plt.xlabel("User polarity")
    plt.ylabel("Number of users")
    plt.tight_layout()
    path = f'{base}_norm.png' if norm else f'{base}.png'
    plt.savefig(os.path.join(outdir, path))
    plt.clf()
    
# def user_pol(user_data):
#     ht_used = []
#     num_contain = 0
#     for tweet in user_data.tweets_period():
#         hts = user_data.get_lower_hashtags()
#         ht_used += hts
#         if not set(hts).isdisjoint(set(base_ht)):
#             num_contain += 1

#     tot = 0
#     for ht in list(set(ht_used).intersection(set(base_ht))):
#         tot += ht_polarity.get(ht)
#     out = 0 if num_contain == 0 else tot / num_contain
#     return tot, out

def generate_stats(data, outdir, **kwargs):
    
    os.makedirs(outdir, exist_ok=True)
    data_point(data, outdir)
    top_10_hashtags(data, outdir)
    top_10_users(data, outdir)
    hashtag_time(data, outdir)
#     echo_chamber(data, outdir)
    
    return
    
def generate_polarity(data, ht_polarity, base_hts, outdir, test, **kwargs):
    
    os.makedirs(outdir, exist_ok=True)
    echo_chamber(data, outdir, ht_polarity, base_hts, test)
    
    return
