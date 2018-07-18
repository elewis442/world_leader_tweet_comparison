import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd


def main():

    '''
    Takes the cleaned twitter data provided by tweet_cleaning.py for the various world leaders, evaluates the reading
    level of the tweets, and performs statistical tests comparing the results from world leaders to results from the 
    fifth grade corpus. Also compares the results from world leaders with each other.
    First runs a t-test with each world leader versus the fifth grade corpus, comparing on a specific test. Compared
    initially using Flesch Grade, as Flesch Readability test most universal text complexity test, but other tests can
    be checked as well.
    Also transforms data into proper format and performs two Tukey tests: the first Tukey test with all world leaders
    and fifth grade corpus, and the second Tukey test using just the world leader data
    '''

    # Pull in various required data
    fifthgrade = pd.read_csv('FifthGrade.csv')
    sanders_text = pd.read_csv('CleanReducedSenSandersTweets.csv')
    obama_text = pd.read_csv('CleanReducedBarackObamaTweets.csv')
    clinton_text = pd.read_csv('CleanReducedHillaryClintonTweets.csv')
    trump_text = pd.read_csv('CleanReducedrealDonaldTrumpTweets.csv')
    corbyn_text = pd.read_csv('CleanReducedjeremycorbynTweets.csv')
    cameron_text = pd.read_csv('CleanReducedDavid_CameronTweets.csv')

    '''
    Take data from the specific test to be compared
    Options for testing are: Flesch_Grade, Automated_Readability_Index, Coleman_Liau_Index,
    Linsear_Write_Score, Dale_Chall_Readability
    '''
    fifthgrade_fr = fifthgrade['Flesch_Grade'].values
    obama_fr = obama_text['Flesch_Grade'].values
    clinton_fr = clinton_text['Flesch_Grade'].values
    trump_fr = trump_text['Flesch_Grade'].values
    sanders_fr = sanders_text['Flesch_Grade'].values
    corbyn_fr = corbyn_text['Flesch_Grade'].values
    cameron_fr = cameron_text['Flesch_Grade'].values

    # Perform TT-test comparing world leader values to fifth grade corpus
    # Null Hypothesis states the averages for fifth grader and world leader data the same
    fifthgrade_to_obama_test = stats.ttest_ind(fifthgrade_fr, obama_fr)
    fifthgrade_to_clinton_test = stats.ttest_ind(fifthgrade_fr, clinton_fr)
    fifthgrade_to_trump_test = stats.ttest_ind(fifthgrade_fr, trump_fr)
    fifthgrade_to_sanders_test = stats.ttest_ind(fifthgrade_fr, sanders_fr)
    fifthgrade_to_corbyn_test = stats.ttest_ind(fifthgrade_fr, corbyn_fr)
    fifthgrade_to_cameron_test = stats.ttest_ind(fifthgrade_fr, cameron_fr)

    print("T-Test P-Value Comparing 5th Grade to:\nObama: {}\nClinton: {}\nTrump: {}\nSanders: {}\nCorbyn: {}\nCameron: {}\n".format(
        fifthgrade_to_obama_test.pvalue,
        fifthgrade_to_clinton_test.pvalue,
        fifthgrade_to_trump_test.pvalue,
        fifthgrade_to_sanders_test.pvalue,
        fifthgrade_to_corbyn_test.pvalue,
        fifthgrade_to_cameron_test.pvalue)
    )

    # Concatenate all world leaderdata together, to transform into proper form for Tukey test
    all_data = pd.DataFrame({'Obama': obama_fr, 'Clinton': clinton_fr,
                             'Trump': trump_fr, 'Sanders': sanders_fr,
                             'Corbyn': corbyn_fr, 'Cameron': cameron_fr})

    all_melt = pd.melt(all_data)

    all_posthoc = pairwise_tukeyhsd(
        all_melt['value'], all_melt['variable'],
        alpha=0.05)

    '''
    Code below used to visualize Tukey results between the six world leaders when compared on specific linguistic test
    '''
    fig = all_posthoc.plot_simultaneous()
    plt.title('Flesch Grade Scoring')
    plt.xlabel('Grade Level')
    plt.savefig("Flesch_Grade_Leaders.png")
    plt.show()


    '''
    Assembles fifth grade corpus data and data from each world leader into a single DataFrame, then performs Tukey test.
    Note that the Tukey test requires same-size datasets, so about half the data from each world leader is left out.
    '''
    reduced_obama_fr = obama_fr[:431]
    reduced_clinton_fr = clinton_fr[:431]
    reduced_trump_fr = trump_fr[:431]
    reduced_sanders_fr = sanders_fr[:431]
    reduced_corbyn_fr = corbyn_fr[:431]
    reduced_cameron_fr = cameron_fr[:431]

    all_v_fifthgrade_data = pd.DataFrame({'Obama': reduced_obama_fr, 'Clinton': reduced_clinton_fr,
                                          'Trump': reduced_trump_fr, 'Sanders': reduced_sanders_fr,
                                          'Corbyn': reduced_corbyn_fr, 'Cameron': reduced_cameron_fr,
                                          'FifthGraders': fifthgrade_fr})

    all_v_fifthgrade_melt = pd.melt(all_v_fifthgrade_data)

    all_v_fifthgrade_posthoc = pairwise_tukeyhsd(
        all_v_fifthgrade_melt['value'], all_v_fifthgrade_melt['variable'],
        alpha=0.05)

    '''
    Code below used to visualize Tukey results which include fifth grade data
    
    fig2 = all_v_fifthgrade_posthoc.plot_simultaneous()
    plt.title('Flesch Grade Scoring')
    plt.xlabel('Grade Level')
    plt.savefig("Flesch_Grade_5th_Graders_Leaders.png")
    # plt.show()
    '''


if __name__ == '__main__':
    main()
