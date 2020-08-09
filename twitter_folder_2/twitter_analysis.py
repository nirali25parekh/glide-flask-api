import tweepy
import config
import re
import pickle
import string
import json
from textblob import TextBlob

# twitter api
auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
auth.set_access_token(config.TWITTER_ACCESS_TOKEN,config.TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# test authentication
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

def clean_tweet(tweet): 
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 

def get_tweet_sentiment(tweet): 
    analysis = TextBlob(tweet) 
    if analysis.sentiment.polarity > 0: 
        return 'positive'
    elif analysis.sentiment.polarity == 0: 
        return 'neutral'
    else: 
        return 'negative'


def findTweetsByKeywordAndFindSentiment(keyword):
    
    results = api.search(q=keyword, lang="en", count=10, tweet_mode="extended", show_user=True)
    returnObject = []
    for result in results:
        tweet = result.full_text #tweet
        cleaned_tweet = clean_tweet(result.full_text) #cleaned_tweet
        sentiment_of_tweet = get_tweet_sentiment(cleaned_tweet) #sentiment
        screen_name = result.user.screen_name     #user screen name
        name = result.user.name     #user name
        description = result.user.description   # user description
        profile_pic = result.user.profile_image_url_https # user profile photo

        returnObject.append({
            "tweet": tweet,
            "cleaned_tweet": cleaned_tweet,
            "sentiment": sentiment_of_tweet,
            "user":{
                "screen_name": screen_name,
                "name": name,
                "description": description,
                "profile_pic": profile_pic
            }
        })

    return { "response": returnObject}