import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import matplotlib.pyplot as plt


columns = [ 'Flesch_Grade', 'Automated_Readability_Index', 'Coleman_Liau_Index',
           'Linsear_Write_Score', 'Dale_Chall_Readability']


def main():
    '''
    Concatenates the tweets from all the world leaders, then creates a machine-learning model. 
    Tests whether the model is accurate.
    '''
    sanders_text = pd.read_csv('CleanReducedSenSandersTweets.csv')
    obama_text = pd.read_csv('CleanReducedBarackObamaTweets.csv')
    clinton_text = pd.read_csv('CleanReducedHillaryClintonTweets.csv')
    trump_text = pd.read_csv('CleanReducedrealDonaldTrumpTweets.csv')
    corbyn_text = pd.read_csv('CleanReducedjeremycorbynTweets.csv')
    cameron_text = pd.read_csv('CleanReducedDavid_CameronTweets.csv')

    frame = [sanders_text, obama_text, clinton_text, trump_text, corbyn_text, cameron_text]

    concat_text = pd.concat(frame)
    concat_text.reset_index(inplace=True, drop=True)

    X = concat_text[columns].values
    y = concat_text['Author'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    # Multiple models using different strategies attempted
    # StandardScaler() and MinMaxScaler() both used, minutely preferable results found by using StandardScaler()
    tweet_classify_knn_model = make_pipeline(
        StandardScaler(),
        KNeighborsClassifier(n_neighbors=39)
    )

    tweet_classify_nb_model = make_pipeline(
        StandardScaler(),
        GaussianNB()
    )

    tweet_classify_svc_model = make_pipeline(
        StandardScaler(),
        SVC(kernel='rbf', C=10)
    )

    tweet_classify_knn_model.fit(X_train, y_train)
    tweet_classify_nb_model.fit(X_train, y_train)
    tweet_classify_svc_model.fit(X_train, y_train)

    print("Model results for:\nKNN: {}\nNB: {}\nSVC: {}\n".format(
        tweet_classify_knn_model.score(X_test, y_test),
        tweet_classify_nb_model.score(X_test, y_test),
        tweet_classify_svc_model.score(X_test, y_test)
    ))

    '''
    Below code used for data visualization. Some assistance for putting together image provided by Prof. Baker
    
    cmap = 'flag'
    scale = StandardScaler()
    pca = PCA(2)
    y_clr = LabelEncoder().fit_transform(y)
    X_pca = pca.fit_transform(scale.fit_transform(X))
    plt.scatter(X_pca[:,0], X_pca[:, 1], c=y_clr, edgecolor='k', cmap=cmap, alpha=0.75)
    plt.title('World Leader Tweet Data Under PCA')
    plt.savefig('World_Leader_Tweet_Classifier.png')
    '''


if __name__ == '__main__':
    main()
