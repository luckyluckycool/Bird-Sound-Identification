import numpy as np
from matplotlib import pyplot as plt
import os
import librosa
from scipy import signal
import keras
import tensorflow as tf


def soundPath(id):
    return f'/kaggle/input/bird-voice-detection/ff1010bird_wav/wav/{id}.wav'

def coverting_to_spectrogram(path, high_freq):
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()
    hl = 512  # number of samples per time-step in spectrogram
    hi = 256  # Height of image
    wi = 256  # Width of image
    y, sr = librosa.load(path)

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

    plt.axis('off')
    plt.savefig(f'/to_predict/{path}.png', bbox_inches='tight', pad_inches=0)
    plt.close()

    os.remove(path)

def predict_audio(path, model):

    coverting_to_spectrogram(path, high_freq=True)
    image = tf.keras.utils.load_img(path=f'/to_predict/{path}.png', target_size=(256, 256),
                                    interpolation='bilinear')
    input_arr = tf.keras.utils.img_to_array(image)
    input_arr = np.array([input_arr])
    y_pred = model.predict(input_arr)
    y_pred = int(np.round(y_pred[0][0]))
    return y_pred