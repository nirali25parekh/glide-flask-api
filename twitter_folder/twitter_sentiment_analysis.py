import config
import tweepy
import re
import pickle
import string
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

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


#  TODO: change model to the best one TAKE CARE: put path from pov of app.py as we are importing there
new_bidi_lstm_model = tf.keras.models.load_model('./twitter_folder/twitter_sentiment_cnn_model')
new_bidi_lstm_model.summary()

def predictSentiment(results):
    global new_bidi_lstm_model
    max_length = 25     
    padding_type='post'
    returnObject = []



    for i in results:
        print('retweeted_status' in dir(i))
        if 'retweeted_status' in dir(i):
            text = i.retweeted_status.full_text
        else:
            text=i.full_text

        tempText = text[:]
        # 1. clean data
        text = re.sub(r'@[A-Za-z0-9]+', '', text) # remove @mentions
        text = re.sub(r'#', '', text) # remove # sign
        text = re.sub(r'RT[\s]+', '', text) # remove RT
        text = re.sub(r'http\S+', '', text)  # remove hyperlinks
        text = text.lower()   # convert to lower case
        for punct in string.punctuation:  # remove punctuations
            text = text.replace(punct, " ")

        text = text.strip()   # remove whitespace

        # 2. Create the sequences via tokenizer 
        with open('./twitter_folder/tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)

        # 3. padding to be done same as training data
        sample_sequences = tokenizer.texts_to_sequences([text])      # tokenize according to our tokens
        reviews_padded = pad_sequences(sample_sequences, padding=padding_type, 
                                        maxlen=max_length) 
        classes = new_bidi_lstm_model.predict(reviews_padded)   # gives back prediction
        print("-----------------------------------------------")
        print('text', i.full_text)
        print('prediction is :', float(classes[0][0]))
        print()

        finalText = tempText.replace("undefined","")
        finaText = finalText.replace("Undefined","")
        finalText = finalText.strip()
        returnObject.append({
                "text": finalText,
                "sentiment" : float(classes[0][0]),
            })
    return returnObject

def findTweetsByKeywordAndFindSentiment(keyword):
    
    results = api.search(q=keyword, lang="en", count=30, tweet_mode="extended")
    returnObject = predictSentiment(results)
    return { "response": returnObject}