import tensorflow as tf
from keras.models import model_from_json


class ModelService:
    model_name: str
    loaded_model: tf.keras.Model

    def __init__(self, model_name: str):
        self.model_name = model_name
        json_file = open(f'cnn_models/{model_name}.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights(f"cnn_models/{model_name}.h5")
        # print("Loaded model from disk")
        loaded_model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['accuracy'])
        self.loaded_model = loaded_model

    def get_model(self):
        return self.loaded_model
