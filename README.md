# world_leader_tweet_comparison
*Comparing The Social Media Writing Complexity of Political Leaders, or, Does a World Leader Write Better than a Fifth Grader?*

***Abstract***

With the ubiquity of social media, and the near-requirement of every public figure to make use of it, it seems like every major world leader now has an active Twitter account. With the current United States president often making headlines based on his use of the Twitter platform, parsing complex geopolitical topics into 140 (or now 280) characters, it feels like today’s general political discourse has been simplified. Hence the core idea to this data science project: is the Twitter output of major world leaders more or less complex than the average writing of a fifth grader?

This project intends to find an answer to this question. As well, with the data gathered in order to answer this first question, it will also attempt to try and answer two further questions: whom amongst the current important political figures of the United States and the UK (specifically Hillary Clinton, Donald Trump, Barack Obama, Bernie Sanders, Jeremy Corbyn, and David Cameron)  write tweets with the most linguistic complexity, and is it possible to develop a machine learning model that can accurately guess a tweet’s author, based on the sentence’s linguistic complexity?


***Required Files and Setup***

Attached in the git repository are five files, and accompanying folder containing the pulled data in various formats. In addition it will be required to install the textstat python library, which contains the linguistic complexity tests performed on the pulled Twitter data, and the tweepy python library, which provides assistance in connecting with Twitter’s API. 

The five python files contained in the git repository are:

*twitter_pull.py*

Prerequisite Files Needed: None (Twitter API access keys required)

A script which makes a call to the Twitter API, and extracts up to the most recent 3,240 tweets of a provided Twitter user, specifically their tweet ID, the date of the tweet’s creation, and the raw text in UTF-8 format, which is returned in a csv format. Original script was found from a git repository online (source can be found in file itself), with some changes made to utilize the pandas library as opposed to the csv library. 

*tweet_cleaning.py*

Prerequisite Files Needed: Raw output csv file extracted from twitter_pull.py

A script which takes the raw UTF-8 strings provided from the results of twitter_pull.py, and cleans up the data to make them as approximate to regular sentences as possible. After which, it also runs through the five chosen textstat linguistic tests on each tweet, determining and saving the various test results, appending a column containing the author of the tweet to be later used in the machine learning classifier, and returning the results in a csv file.

*tweet_textstat.py*

Prerequisite Files Needed: A csv file containing the corpus of text from fifth-grade writing samples

This script takes a csv file that’s the listing of samples of fifth grade writing, upon which the five chosen textstat linguistic complexity tests are run against, with the results for each sample saved, and the final results returned in a csv file

*tweet_stat_finder.py*

Prerequisite Files Needed: The cleaned up csv data files of each world leader, as well as the tested data file of fifth grade samples

This file will run the various statistical tests on the provided data, first running a t-test comparing the fifth grade corpus to each individual political leader, then transforming the data into the necessary form to run two Tukey tests, one for the group just containing all world leaders, and one of the group containing all world leaders and the fifth grade sample results

*tweet_classifier.py*

Prerequisite Files Needed: The cleaned-up csv data files of each world leader

This file will take in the data for each provided political figure, and attempt to create a machine learning classifier that will attempt to discern a tweet’s author based on a tweet’s linguistic complexity.

In addition to the above five python files, the git repository also contains a file folder containing all the necessary extracted data, including the original raw data csv files for each world leader extracted from the Twitter API, the cleaned-up data csv files for each leader, as well as cleaned-up files for each leader that’s been normalized to have the same number of rows (specifically 800), as Tukey statistical tests require datasets of equivalent size. 

Lastly, the data folder also contains the original text file of fifth grade sample writing, as well as the csv file containing that same data, the data samples found by extracting samples from the internet, totaling 431 samples.

