from flask import Flask, request, request, render_template
from predict import predict_sentiments
from YTComments import get_video_comments
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

def get_video(video_id):
    if not video_id:
        return {"ERROR": "video_id is required"}

    comments = get_video_comments(video_id)
    predictions = predict_sentiments(comments)

    positive = predictions.count("Positive")
    negative = predictions.count("Negative")
    rating = round((positive / len(comments)) * 100, 2)

    summary = {
        "positive": positive,
        "negative": negative,
        "num_comments": len(comments),
        "rating": rating
    }

    return {"predictions": predictions, "comments": comments, "summary": summary}


@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    comments = []
    if request.method == 'POST':
        video_url = request.form.get('video_url')
        video_id = video_url.split("v=")[1]
        data = get_video(video_id)

        summary = data['summary']
        comments = list(zip(data['comments'], data['predictions']))
    return render_template('index.html', summary=summary, comments=comments)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)