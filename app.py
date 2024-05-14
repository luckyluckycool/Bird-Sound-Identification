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


def extract_zip_file(file):
    temp_dir_path = 'temp'
    os.makedirs(temp_dir_path, exist_ok=True)
    file_path = os.path.join(temp_dir_path, file.filename).replace('\\', '/')
    file.save(file_path)
    zip_files_path = temp_dir_path + '/' + os.path.splitext(os.path.basename(file.filename))[0]
    os.makedirs(zip_files_path, exist_ok=True)
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(zip_files_path)
    os.remove(file_path)
    return zip_files_path


@app.route('/predictAudio', methods=['POST'])
def success():
    file = request.files['file']
    if file.filename.endswith('.wav'):
        temp_dir_path = 'temp'
        os.makedirs(temp_dir_path, exist_ok=True)
        file_path = os.path.join(temp_dir_path, file.filename).replace('\\', '/')
        file.save(file_path)
        prediction = predictionService.predict_audio_file(file_path)
        result = 'contains' if prediction else 'does not contain'
        os.remove(file_path)
        return render_template("file_identification_result.html", result=result, file_path=file.filename)
    elif file.filename.endswith('.zip'):
        zip_files_path = extract_zip_file(file)
        result, skipped_files = predictionService.predict_several_files(
            zip_files_path)
        shutil.rmtree(zip_files_path)
        return render_template("zip_identification_result.html", result=result, file_path=file.filename,
                               skipped_files=skipped_files)
    else:
        return render_template("wrong_file.html")


@app.route('/migrationMap', methods=["GET"])
def migration_map():
    time_param = request.args.get('time')
    time = None
    times = {}
    if time_param is None:
        all_times = areaService.get_all_times()
        if len(all_times) > 0:
            time = all_times[len(all_times) // 2]
            times = areaService.get_times_for_map(time)
    else:
        time = datetime.strptime(time_param, "%Y-%m-%dT%H:%M:%S")
        times = areaService.get_times_for_map(time)
    area_data, centroid = locationService.get_areas_with_locations()
    area_detections = areaService.get_area_detection_results_by_time(time)
    return render_template("migration_map.html", areas=area_data, areaDetections=area_detections, times=times,
                           centroid=centroid)


@app.route('/locationIdentification', methods=['GET'])
def location_identification():
    return render_template("location_identification.html")


@app.route('/predictAndInsertAudios', methods=['POST'])
def predict_and_insert_audios():
    file = request.files['file']
    if file.filename.endswith('.zip'):
        zip_files_path = extract_zip_file(file)
        try:
            detection_results, annotations, bad_files = predictionService.predict_and_insert_audios(zip_files_path)
        except (FileNotFoundError, ValueError) as e:
            return render_template('wrong_zip_file.html', error=str(e))
        finally:
            shutil.rmtree(zip_files_path)
        return render_template('location_identification_result.html', detection_results=detection_results,
                               all_files=annotations - bad_files, bad_files=bad_files)
    return render_template('wrong_zip_file.html', error='input file is not a zip file')


import time

@app.route('/computeAreasDetections', methods=['GET'])
def computeAreasDetections():
    is_from_map = bool(request.args.get('isFromMap'))
    detection_results = areaService.calculate_area_detections()
    if is_from_map:
        return redirect(url_for('migration_map'))
    return render_template('areas_calculation_result.html', detectionResults=detection_results)


if __name__ == '__main__':
    app.run(debug=True)
