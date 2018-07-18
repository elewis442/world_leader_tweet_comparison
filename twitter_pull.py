import tweepy
import pandas as pd

'''
Twitter API requires the use of personal key information provided upon request. 
For security purposes I've removed my personal twitter API codes
'''
consumer_key = 'REDACTED'
consumer_secret = 'REDACTED'
access_key = 'REDACTED'
access_secret = 'REDACTED'

# Code used to pull users twitter info and put into csv format modified from original code provided here:
# https://gist.github.com/yanofsky/5436496


def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets via the API, thus 3240 is limit of tweets pulled

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200, tweet_mode='extended')

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before {}".format(oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, tweet_mode='extended')

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...{} tweets downloaded so far".format(len(alltweets)))

    # transform the tweepy tweets into a 2D array that will populate the csv
    # outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

    id_list = []
    created_at_list = []
    text_list = []

    
    
    # Puts tweets into csv format (id, created_at, text)
    
    # Makes a list of ids, a list of created_at dates, and a list of tweet text
    
    for tweet in alltweets:
        id_list.append(tweet.id_str)
        created_at_list.append(tweet.created_at)
        return_string = tweet.full_text
        result_string = return_string.replace(';', '')
        final_string = result_string.encode("utf-8")
        text_list.append(final_string)

        
    # Assembles the lists into a 3-column DataFrame, then transforms that into csv
    
    tweets = {'ID': id_list,
             'Created_At': created_at_list,
             'Text': text_list}
    tweet_df = pd.DataFrame.from_dict(tweets)
    tweet_df = tweet_df[['ID', 'Created_At', 'Text']]

    tweet_df.to_csv('{}Tweets.csv'.format(screen_name), index=False)


if __name__ == '__main__':
    # pass in the username of the account you want to download
    get_all_tweets("SenSanders")
