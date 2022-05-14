from flask import Flask,request,jsonify
from flask_cors import CORS
from multiprocessing import Pool
from YoutubeAnalyzer import getAndPredictVideoById

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/",methods=['GET'])
def home() :
    return {"msg":"api working fine"}
    
@app.route("/api/video", methods = ['POST'])
def getCommentsForVideo(): 

    try :
        videoID = request.json["videoID"]
        video_res = getAndPredictVideoById(videoID,report=True)
        return jsonify(video_res)

    except Exception as e :
        print(e)
        return {"error" : "sorry,We couldn't process this video's comment, please verify your video ID and try again"}

@app.route("/api/videos", methods = ['POST'])
def getLabelForVideos() :
    try : 
        videoIds = request.form["videoIDs"]
        videoIds = videoIds.split(",")

        video_res = []

        with Pool() as p:
            video_res = p.map(getAndPredictVideoById, videoIds)

        # for videoID in videoIds : 
        #     video_res.append(getAndPredictVideoById(videoID))

        return jsonify(video_res)

    except Exception as e :
        print(e)
        return {"error" : "sorry,We couldn't process this video's comment, please verify your video ID and try again"}


if __name__ == "__main__" :
    app.run(debug=True)
