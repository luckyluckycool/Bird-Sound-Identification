import tensorflow as tf
import keras
from keras.models import model_from_json


def import_model(name):
    json_file = open(f'models/{name}.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(f"models/{name}.h5")
    #print("Loaded model from disk")

    loaded_model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['accuracy'])

    return loaded_model

