from textstat.textstat import textstat as ts
import pandas as pd
import numpy as np


# Below are formulas from TextStat that evaluate readability, formatted so they can be used with np.vectorize

def flesch_kincaid_grade(string):
    result = ts.flesch_kincaid_grade(string)
    return result


def flesch_kincaid_readability(string):
    result = ts.flesch_reading_ease(string)
    return result


def gunning_fog(string):
    result = ts.gunning_fog(string)
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


flesch_kincaid_grade = np.vectorize(flesch_kincaid_grade, otypes=[np.float])
flesch_kincaid_readability = np.vectorize(flesch_kincaid_readability, otypes=[np.float])
gunning_fog = np.vectorize(gunning_fog, otypes=[np.float])
automated_readability = np.vectorize(automated_readability, otypes=[np.float])
coleman_liau = np.vectorize(coleman_liau, otypes=[np.float])
linsear_write = np.vectorize(linsear_write, otypes=[np.float])
dale_chall_readability = np.vectorize(dale_chall_readability, otypes=[np.float])


def main():

    # A subscript used to enter in the scores onto the fifth grade corpus, without requiring any further clean-up
    # Requires untested Fifth Grade corpus in csv format in same folder

    tweets = pd.read_csv('FifthGradeText.csv')

    tweets['Flesch_Grade'] = flesch_kincaid_grade(tweets['Text'])
    tweets['Automated_Readability_Index'] = automated_readability(tweets['Text'])
    tweets['Coleman_Liau_Index'] = coleman_liau(tweets['Text'])
    tweets['Linsear_Write_Score'] = linsear_write(tweets['Text'])
    tweets['Dale_Chall_Readability'] = dale_chall_readability(tweets['Text'])
    
    tweets.to_csv('FifthGrade.csv', index=False)


if __name__ == '__main__':
    main()
