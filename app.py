#!flask/bin/python
from flask import Flask, request, jsonify
from flask_cors import CORS,cross_origin
import json

# TODO: uncomment this for twitter analysis1
import twitter_folder.twitter_sentiment_analysis as tsa     # for twitter sentiment analysis

# TODO: uncomment this for twitter analysis2
import twitter_folder_2.twitter_analysis as ta     # for twitter sentiment analysis

# TODO: uncomment this for reddit mining
import reddit_folder.reddit_mining as rm        # for mining reddit

# TODO: uncomment this for video indexing
import video_indexer_folder.video_indexing as vi       # for mining reddit

app = Flask(__name__)
CORS(app, support_credentials=True)

#  for twitter sentiment analysis
@app.route('/keyword', methods=['POST'])
def getTweetsOnKeyword():
    keyword = request.form.get('keyword', '')
    return ta.findTweetsByKeywordAndFindSentiment(keyword)

#  for reddit links
@app.route('/reddit',methods=['POST'])
def send_reddits():
    sectors = request.form.get('sector')
    rm.mine_reddit(sectors)
    Rlist=[]
    Rlist=rm.preprocess()
    return jsonify(Rlist)

# for video indexer
@app.route('/uploader', methods=['GET', 'POST'])
def upload():
    language=request.form.get('lang')
    f = request.files['file']
    name=vi.upload_file(f)
    video_id = vi.createinstance(name,language)

    while(True):
        info = vi.indexvideo(video_id,language)
        if info['state']=='Processed':
            info1=json.dumps(info)
            return info1


if __name__ == '__main__':
    app.run(debug=True)

