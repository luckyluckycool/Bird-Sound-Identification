import os
import zipfile
from flask import *
from services import PredictionService
import shutil

app = Flask(__name__)
predictionService: PredictionService = None


@app.route('/', methods=['GET'])
def main():
    return render_template("index.html")


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        prediction_service = PredictionService.PredictionService()
        if f.filename.endswith('.wav'):
            f.save(f.filename)
            prediction = prediction_service.predict_audio(f.filename)

            # print(prediction)

            result = 'contains' if prediction == 1 else 'does not contain'
            # print(f.filename)

            return render_template("file_upload.html", result=result, file_path=f.filename)
        elif '.zip' in f.filename:
            temp_dir_path = 'temp'
            os.makedirs(temp_dir_path, exist_ok=True)
            file_path = os.path.join(temp_dir_path, f.filename).replace('\\', '/')
            f.save(file_path)
            zip_files_path = temp_dir_path + '/' + os.path.splitext(os.path.basename(f.filename))[0]
            os.makedirs(zip_files_path, exist_ok=True)
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(zip_files_path)
            os.remove(file_path)
            result, skipped_files = prediction_service.predict_territory(
                zip_files_path)
            shutil.rmtree(zip_files_path)
            return render_template("zip_identification.html", result=result, file_path=f.filename,
                                   skipped_files=skipped_files)
        else:
            return render_template("wrong_file.html")


if __name__ == '__main__':
    app.run()
    if predictionService is None:
        predictionService = PredictionService.PredictionService()
