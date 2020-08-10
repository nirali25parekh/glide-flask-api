from flask import Flask, request, jsonify
from flask_cors import CORS,cross_origin
import praw
import csv
import datetime
import pandas as pd

def mine_reddit(sectors):
    sectorsArray = sectors.split(" ")
    print('array',sectorsArray)
    def writeheaders():
        f.writerow(["Number", "Keyword", "Title", "Score", "Comments", "URL", "Domain", "Permalink", "ID", "Subreddit",
                    "CreatedDate"])

    def writefields():
        f.writerow([startNum, search.strip(), submission.title,
                    submission.score, submission.num_comments,
                    submission.url, submission.domain, submission.permalink, submission.id,
                    submission.subreddit, datetime.datetime.utcfromtimestamp(submission.created).strftime('%m-%d-%Y')])

    for i in range(5):
        try:
            reddit = praw.Reddit(client_id=os.environ.get('REDDIT_CLIENTID'),
                                client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                                password=os.environ.get('REDDIT_PASSWORD'),
                                user_agent='Reddit search data extractor by /u/' + os.environ.get('REDDIT_USERNAME') + '',
                                username=os.environ.get('REDDIT_USERNAME'))

            print("Authentication for " + str(reddit.user.me()) + " is verified. Proceeding.\r\n")

            outfilename = './reddit_folder/reddit-data.csv'

            sortsub = 'relevance'
            filtersub = 'No'

            search_list = sectorsArray

            if (filtersub.lower() == "yes"):
                subreddit = input("Enter the subreddit names delimited with commas (i.e., BigSEO):\r\n")
                subreddit_list = subreddit.split(',')
                file = open(outfilename, "w+", newline="\n", encoding="utf-8")
                f = csv.writer(file)
                writeheaders()
                for subs in subreddit_list:
                    for search in search_list:
                        startNum = 0
                        for submission in reddit.subreddit(subs.strip()).search(search, sort=sortsub):
                            startNum += 1
                            writefields()
                        print(
                            "Writing out posts results for the search '" + search.strip() + "' in 'r/" + subs.strip() + "'\r\n")
                    file.close
                    break
            else:
                file = open(outfilename, "w+", newline="\n", encoding="utf-8")
                f = csv.writer(file)
                writeheaders()
                for search in search_list:
                    startNum = 0
                    for submission in reddit.subreddit('all').search(search.lower(), sort=sortsub):
                        startNum += 1
                        writefields()
                    print("Writing out posts results for the search '" + search.strip() + "' in 'r/all'\r\n")
                file.close
                break
        except Exception as e:
            print(e)
            if i>=4:
                raise
            print('Timeout', i)


def preprocess():
    df=pd.read_csv('./reddit_folder/reddit-data.csv')
    df=pd.DataFrame(df)
    df=df.groupby('Keyword').head(10)
    df=df[['Keyword','URL','Domain','Permalink','Subreddit','CreatedDate']]
    Row_list=[]
    for index,rows in df.iterrows():
        my_list=[rows.Keyword,rows.URL,rows.Domain,rows.Permalink,rows.Subreddit,rows.CreatedDate]
        Row_list.append(my_list)
    return Row_list