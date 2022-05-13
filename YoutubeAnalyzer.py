from collections import Counter
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def getAndPredictVideoById(videoID,report=False) :

    sid_obj = SentimentIntensityAnalyzer()

    URL = "https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyAhx5jhsQ2dNIgYjZBju2J53oopcTV8Xj0&part=snippet%2Creplies&videoId="+ videoID +"&fbclid=IwAR3WZwXpCYSKETtvn6MkxRP4ZkHOlc5AKS86bPrIjA15S-r372QRHdx1JPE&maxResults=100"   
    r = requests.get(url = URL)
    data = r.json()
    comments = []
    n_iter = 0
    cpt = 0

    while True :

        n_iter += 1
        for item in data["items"] : 
            comment = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
            
            # blob = TextBlob(comment)
            sentiment_dict = sid_obj.polarity_scores(comment)
            cl = ""
            if sentiment_dict["compound"] >= .05 :
                cl = "Positive"
            elif sentiment_dict["compound"] <= -.05 :
                cl = "Negative"
            else :
                cl = "Neutral"

            comments.append({"comment" : comment,
                            "class": cl,
                            "score" : sentiment_dict["compound"],
                            "Negative": sentiment_dict['neg']*100,
                            "Neutral" : sentiment_dict['neu']*100,
                            "Positive" :  sentiment_dict["pos"] *100
                            })
            cpt += 1
        if "nextPageToken" not in data or n_iter > 10 : 
            break
        
        URL += "&pageToken=" + data["nextPageToken"]
        r = requests.get(url = URL)
        data = r.json()

    ctr = Counter(comment['class'] for comment in comments)

    if report == True : 
        video_res = {
            "class" : ctr.most_common(1)[0][0],
            "negative" : round(ctr["Negative"] * 100 / cpt,2),
            "positive" : round(ctr["Positive"] * 100 / cpt,2),
            "neutral" : round(ctr["Neutral"] * 100 / cpt,2),
            "top_comments" : sorted(comments,key=lambda c : c["score"],reverse=True)[:10],
            "worse_comments" : sorted(comments,key=lambda c : c["score"])[:10],
            "bar_chart_data" : list(map(lambda c : c['class'],comments)),
            "histogramm_data" : list(map(lambda c : c['score'],comments)),
        }
    else : 
         video_res = {
            "class" : ctr.most_common(1)[0][0],
            "negative" : round(ctr["Negative"] * 100 / cpt,2),
            "positive" : round(ctr["Positive"] * 100 / cpt,2),
            "neutral" : round(ctr["Neutral"] * 100 / cpt,2),
        }

    return video_res

