import os
import shutil
import zipfile
from datetime import datetime

from flask import *

from services.AreaService import AreaService
from services.LocationService import LocationService
from services.PredictionService import PredictionService

app = Flask(__name__)
predictionService = PredictionService()
locationService = LocationService()
areaService = AreaService()


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')


@app.route('/fileIdentification', methods=['GET'])
def file_identification():
    return render_template("file_identification.html")


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        prediction_service = PredictionService()
        if f.filename.endswith('.wav'):
            f.save(f.filename)
            prediction = prediction_service.predict_audio(f.filename)
            result = 'contains' if prediction == 1 else 'does not contain'
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


@app.route('/migrationMap')
def migrationMap():
    time = request.args.get('time')
    if time is None:
        all_times = areaService.get_all_times()
        time = all_times[len(all_times) // 2]
    else:
        time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
    times = areaService.get_times_for_map(time)
    area_data, centroid = locationService.get_areas_with_locations()
    area_detections = areaService.get_area_detection_results_by_time(time)
    return render_template("migration_map.html", areas=area_data, areaDetections=area_detections, times=times,
                           centroid=centroid)


if __name__ == '__main__':
    app.run(debug=True)
