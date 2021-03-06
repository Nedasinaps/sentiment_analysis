import time
from sentiment_classifier import SentimentClassifier
from flask import Flask, render_template, request

app = Flask(__name__)

print("Preparing classifier")
start_time = time.time()
classifier = SentimentClassifier()
print("Classifier is ready")
print(time.time() - start_time, "seconds")


@app.route('/', methods=["POST", "GET"])
def index_page(text="", prediction_message=""):
    if request.method == "POST":
        text = request.form["text"]
        print(text)
        prediction_message = classifier.get_prediction_message(text)
        print(prediction_message)

    return render_template('sentiment_analisys.html',
                           text=text,
                           prediction_message=prediction_message)


if __name__ == "__main__":
    app.run()