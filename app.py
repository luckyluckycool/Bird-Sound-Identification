import Model
from flask import Flask
from distutils.log import debug
from fileinput import filename
from flask import *
import PredictionService


app = Flask(__name__)


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']

        if '.wav' in f.filename:

            f.save(f.filename)

            prediction_service = PredictionService.Prediction()
            prediction = prediction_service.predict_audio(f.filename)

            #print(prediction)

            result = 'contains' if prediction == 1 else 'does not contain'
            #print(f.filename)

            return render_template("file_upload.html", result=result, file_path=f.filename)
        else:
            return render_template("wrong_file.html")


if __name__ == '__main__':
    app.run()
