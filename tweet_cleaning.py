import pandas as pd
import numpy as np
import re
from textstat.textstat import textstat as ts

'''
Various simple functions created to perform textstat tests, to be later vectorized 
and used to enter in various test results onto dataframe
'''
def flesch_kincaid_grade(string):
    result = ts.flesch_kincaid_grade(string)
    return result


def automated_readability(string):
    result = ts.automated_readability_index(string)
    return result


def coleman_liau(string):
    result = ts.coleman_liau_index(string)
    return result


def linsear_write(string):
    result = ts.linsear_write_formula(string)
    return result


def dale_chall_readability(string):
    result = ts.dale_chall_readability_score(string)
    return result


def text_convert(text_string):

    '''
    Takes the raw utf-8 text string provided within result of twitter_pull.py,
    removes various unwanted details, removes URLs and emojis, and excludes retweets
    and tweets containing hashtags
    '''
    # Turn any retweets into None's to be later removed
    if text_string[2:4] == 'RT':
        return 'None'
    elif '@' in text_string:
        return 'None'
    elif '#' in text_string:
        return 'None'

    # Remove http(s) from text
    # Some assistance for regex found at:
    # https://stackoverflow.com/questions/11331982/how-to-remove-any-url-within-a-string-in-python

    text_string = re.sub(r'https?\S+', '', text_string)
    text_string = re.sub(r'(\\x..)+', '', text_string)
    # Remove the initial b and parentheses
    text_string = text_string[2:-1]

    # replacing shortenings for words with their words
    result_string = text_string.replace('&amp', 'and')
    result_string = result_string.replace('w/', 'with')
    result_string = result_string.replace('\\n\\n', ' ')
    result_string = result_string.replace(' u ', ' you ')
    result_string = result_string.replace('....', '')
    result_string = result_string.replace('...', '')
    result_string = result_string.replace('..', '')
    result_string = result_string.replace('\\n', ' ')
    result_string = result_string.replace('\\', '')
    result_string = result_string.replace('-H', '')
    '''
    Obama and Clinton tweets often ended with signature, below removes signature
    These steps were only run active when pertaining to the specific twitter user.
    ie. President Obama statement was active when cleaning Obama tweets, Hillary statement
    when cleaning Clinton tweets
    
    if result_string[-15:] == 'President Obama':
        result_string = result_string[:-15]
    if result_string[-7:] == 'Hillary':
    result_string = result_string[:-8]
    '''

    # Very short tweets were obfuscating textstat results, so anything less than 40 characters considered not a sentence
    if len(result_string) < 40:
        return None

    return result_string


def none_convert(text_string):
    if text_string == 'None':
        return float('NaN')
    else:
        return 0


text_convert = np.vectorize(text_convert, otypes=[np.str])
none_convert = np.vectorize(none_convert, otypes=[np.float])
flesch_kincaid_grade = np.vectorize(flesch_kincaid_grade, otypes=[np.float])
automated_readability = np.vectorize(automated_readability, otypes=[np.float])
coleman_liau = np.vectorize(coleman_liau, otypes=[np.float])
linsear_write = np.vectorize(linsear_write, otypes=[np.float])
dale_chall_readability = np.vectorize(dale_chall_readability, otypes=[np.float])


def main(screen_name):

    '''
    Requires raw csv file pulled from twitter_pull.py in same folder
    This script takes in the raw csv pulled from twitter, performs various clean-up strategies,
    and then performs and records the various textstat tests onto the dataframe, before pulling it
    back out as a csv file
    '''
    tweets = pd.read_csv('{}Tweets.csv'.format(screen_name))

    tweets['Text'] = text_convert(tweets['Text'])
    tweets['rating'] = none_convert(tweets['Text'])

    # Some assistance found from
    # https://stackoverflow.com/questions/13413590/how-to-drop-rows-of-pandas-dataframe-whose-value-in-certain-columns-is-nan
    tweets = tweets[pd.notnull(tweets['rating'])]
    tweets.drop(['rating'], axis=1, inplace=True)

    # Enter in name of tweet author here
    tweets['Author'] = screen_name

    tweets.reset_index(drop=True, inplace=True)

    # Taking converted text-strings, and running various textstat functions on them, setting them up

    tweets['Flesch_Grade'] = flesch_kincaid_grade(tweets['Text'])
    tweets['Automated_Readability_Index'] = automated_readability(tweets['Text'])
    tweets['Coleman_Liau_Index'] = coleman_liau(tweets['Text'])
    tweets['Linsear_Write_Score'] = linsear_write(tweets['Text'])
    tweets['Dale_Chall_Readability'] = dale_chall_readability(tweets['Text'])

    tweets.to_csv('Clean{}Tweets.csv'.format(screen_name), index=False)


if __name__ == '__main__':
    # input twitterhandle as input, and if twitter_pull step was successful the data will be cleaned
    main("SenSanders")
