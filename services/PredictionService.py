import os

import librosa
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.applications.resnet import preprocess_input
from matplotlib import pyplot as plt
from scipy import signal

from dao.DetectionResultDao import DetectionResultDao
from models.DetectionResultModel import DetectionResultModel
from services.ModelService import ModelService


def soundPath(id):
    return f'/kaggle/input/bird-voice-detection/ff1010bird_wav/wav/{id}.wav'


def preprocess(images, labels):
    return preprocess_input(images), labels


class PredictionService:
    modelService: ModelService
    detectionResultDao: DetectionResultDao

    def __init__(self):
        self.modelService = ModelService('tuned')
        self.detectionResultDao = DetectionResultDao()

    def convert_to_spectrogram(self, absolute_path, high_freq):
        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True
        fig, ax = plt.subplots()
        hl = 512
        hi = 256
        wi = 256
        y, sr = librosa.load(absolute_path)

        def get_high_freq(y, sr):
            b, a = signal.butter(10, 2000 / (sr / 2), btype='highpass')
            yf = signal.lfilter(b, a, y)
            return yf

        if high_freq:
            y = get_high_freq(y, sr)

        window = y[0:wi * hl]
        S = librosa.feature.melspectrogram(y=window, sr=sr, n_mels=hi, hop_length=hl)
        S_dB = librosa.power_to_db(S, ref=np.max)
        librosa.display.specshow(S_dB, x_axis='time', y_axis='mel', sr=sr, ax=ax)

        if not os.path.exists('/to_predict'):
            os.mkdir('/to_predict')
        path = os.path.basename(absolute_path)
        plt.axis('off')
        plt.savefig(f'/to_predict/{path}.png', bbox_inches='tight', pad_inches=0)
        plt.close()

    def predict_audio_file(self, path):
        self.convert_to_spectrogram(path, high_freq=True)
        image = tf.keras.utils.load_img(path=f'/to_predict/{os.path.basename(path)}.png', target_size=(256, 256),
                                        interpolation='bilinear')
        input_arr = tf.keras.utils.img_to_array(image)
        input_arr = np.array([input_arr])

        y_pred = self.modelService.get_model().predict(input_arr)
        y_pred = np.round(y_pred[0][0], 2) > 0.75
        return y_pred

    def predict_several_files(self, directory_path):
        file_list = os.listdir(directory_path)
        skipped_files = []
        true_count = 0
        print(f'Test by {len(file_list)} samples')
        for filename in file_list:
            if '.wav' not in filename:
                skipped_files.append(filename)
                continue
            prob_temp = self.predict_audio_file(directory_path + '/' + filename)
            if int(np.round(prob_temp)) == 1:
                true_count += 1
            print(f'Probability of sample {filename} - {prob_temp}')
        print(f'Indentified by {len(file_list) - len(skipped_files)} samples')
        print(f'The bird was detected by {true_count} microphones')
        return [true_count, skipped_files]

    def predict_and_insert_audios(self, directory_path):
        file_list = os.listdir(directory_path)
        annotation_filenames = [f for f in file_list if f.endswith('.csv')]
        if len(annotation_filenames) == 0:
            raise FileNotFoundError('.csv file not found')
        if len(annotation_filenames) > 1:
            raise ValueError('more than one .csv file found')
        csv_file_path = directory_path + '/' + annotation_filenames[0]
        annotations = pd.read_csv(csv_file_path, header=0, names=['audio_id', 'location_id', 'detection_time'],
                                  parse_dates=['detection_time'])
        file_list.remove(annotation_filenames[0])
        detection_results = []
        bad_files = []
        for index, row in annotations.iterrows():
            temp_path = [f for f in file_list if f == str(row['audio_id']) + '.wav']
            if len(temp_path) != 1:
                bad_files.append(temp_path)
                continue
            audio_path = directory_path + '/' + temp_path[0]
            if not os.path.isfile(audio_path):
                bad_files.append(audio_path)
                continue
            prob = self.predict_audio_file(audio_path)
            if prob:
                detection_results.append(
                    DetectionResultModel(location=row['location_id'],
                                         detection_time=row['detection_time'].to_pydatetime(), area_computed=False))
        if len(detection_results) > 0:
            self.detectionResultDao.insert_detection_results(detection_results)
        return len(detection_results), len(annotations), len(bad_files)
