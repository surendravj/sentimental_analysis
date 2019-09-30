from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor

import pandas as pd
import numpy as np
import re
from textblob import TextBlob
import matplotlib.pyplot as plt


class Auth:
    def twitter_auth(self):
        auth = OAuthHandler(
            'BOT3NeMU5AGOx9QZNwtA6Nesd',
            'eVGNtdVv97sWsBJKkC6cUWYnGTjXyaWyARbYD6vly57psbsaLE')
        auth.set_access_token(
            '999548841228550144-xHCxhZBopA3uH0cb6UM4IdbFE2p3cwE',
            'QyUxmVInJXqliG4uKUcPQeTTwd8t5Ey1tQ1VGtzKCIVX1')
        return auth


class Twitter:
    def __init__(self, twitter_user):
        self.authicator = Auth().twitter_auth()
        self.twitterClient = API(self.authicator)
        self.twitter_user = twitter_user

    def get_tweets(self, no_of_tweets):
        tweets = []
        for tweet in Cursor(
                self.twitterClient.user_timeline,
                id=self.twitter_user).items(no_of_tweets):
            tweets.append(tweet)
        return tweets

    def get_home_timeline_tweets(self, no_of_tweets):
        homeline_tweets = []
        for tweet in Cursor(
                self.twitterClient.home_timeline,
                id=self.twitter_user).items(no_of_tweets):
            homeline_tweets.append(tweet)
        return homeline_tweets


class analyze:
    def structure_data(self, tweets):
        df = pd.DataFrame(
            data=[tweet.text for tweet in tweets], columns=['Tweets'])
        return df


class TweetAnalyzer:
    def clean_tweet(self, tweet):
        return ' '.join(
            re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ",
                   tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1


class plot_graph:
    def __init__(self):
        self.postive = 0
        self.nagative = 0
        self.neutral = 0

    def give_results(self, df):
        for i in df:
            if (i == 1):
                self.postive += 1
            elif (i == 0):
                self.neutral += 1
            else:
                self.nagative += 1

    def plot_pie(self):
        sentiment = [self.postive, self.nagative, self.neutral]
        colors = ['g', 'r', 'b']
        labels = ['postive', 'nagative', 'neutral']
        plt.pie(sentiment, labels=labels, colors=colors, autopct='%.1f%%')
        plt.title('Pie respresentaion of sentimental anaysis on Twitter')
        plt.show()

    def plot_gr(self, data):
        plt.plot(data)
        plt.xlabel('Tweets')
        plt.ylabel('Sentiment')
        plt.show()


t = Twitter('Cristiano')
t1=Twitter('Surendravj1')
a = analyze()
s = TweetAnalyzer()
df = a.structure_data(t.get_tweets(30))

df1 = a.structure_data(t1.get_home_timeline_tweets(30))

df1['sentiment'] = np.array(
    [s.analyze_sentiment(tweet) for tweet in df1['Tweets']])

df['sentiment'] = np.array(
    [s.analyze_sentiment(tweet) for tweet in df['Tweets']])



p = plot_graph()
p1=plot_graph()


print('Invidual Tweets of an user')
print(df)
p.give_results(df['sentiment'])
p.plot_pie()
p.plot_gr(df['sentiment'])


print('Analysis of Twitter home tweets of an individual person ')
print(df1)
p1.give_results(df1['sentiment'])
p1.plot_pie()
p1.plot_gr(df1['sentiment'])