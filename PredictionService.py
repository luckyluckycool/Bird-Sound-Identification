import os

import librosa
import numpy as np
import tensorflow as tf
from keras.applications.resnet import preprocess_input
from matplotlib import pyplot as plt
from scipy import signal

import Model


def soundPath(id):
    return f'/kaggle/input/bird-voice-detection/ff1010bird_wav/wav/{id}.wav'


def preprocess(images, labels):
    return preprocess_input(images), labels


class PredictionService:
    model = None

    def __init__(self, model=None):
        if self.model is None:
            if model is None:
                self.model = Model.import_model('tuned')
            else:
                self.model = model

    def coverting_to_spectrogram(self, absolute_path, high_freq):
        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True
        fig, ax = plt.subplots()
        hl = 512  # number of samples per time-step in spectrogram
        hi = 256  # Height of image
        wi = 256  # Width of image
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
        img = librosa.display.specshow(S_dB, x_axis='time', y_axis='mel', sr=sr, ax=ax)

        if not os.path.exists('/to_predict'):
            os.mkdir('/to_predict')
        path = os.path.basename(absolute_path)
        plt.axis('off')
        plt.savefig(f'/to_predict/{path}.png', bbox_inches='tight', pad_inches=0)
        plt.close()

        # os.remove(path)

    def predict_audio(self, path, preprocess=False):

        self.coverting_to_spectrogram(path, high_freq=True)
        image = tf.keras.utils.load_img(path=f'/to_predict/{os.path.basename(path)}.png', target_size=(256, 256),
                                        interpolation='bilinear')
        input_arr = tf.keras.utils.img_to_array(image)
        input_arr = np.array([input_arr])

        if preprocess:
            input_arr = preprocess_input(input_arr)

        y_pred = self.model.predict(input_arr)
        # y_pred = int(np.round(y_pred[0][0]))
        return y_pred[0][0]

    def predict_territory(self, directory_path):
        file_list = os.listdir(directory_path)
        skipped_files = []
        true_count = 0
        print(f'Test by {len(file_list)} samples')
        for filename in file_list:
            if '.wav' not in filename:
                skipped_files.append(filename)
                continue
            prob_temp = self.predict_audio(directory_path + filename)
            if int(np.round(prob_temp)) == 1:
                true_count += 1
            print(f'Probability of sample {filename} - {prob_temp}')
        print(f'Indentified by {len(file_list) - len(skipped_files)} samples')
        print(f'The bird was detected by {true_count} microphones')
        return [true_count, skipped_files]
