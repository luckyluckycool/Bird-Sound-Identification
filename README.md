# Bird-Sound-Identification

System to identificate bird sound in audio file

## Project structure
+ Model.py - module for importing model from .json and .h5
+ PredictionService.py - module for identification sound of birds in audio
+ app.py - the main module for running the API
+ templates - folder with static html files
+ models - folder with models for system
+ cnn-spectrogram - Jypiter Notebook for model training and export
---
## To run locally:
1. Clone repository to local system
2. `pip install requirements.txt`
3. `python app.py`
---
## Technologies
| **Technology** | **Version**  |
|----------------|--------------|
| Tensorflow     | 2.11.0       |
| Librosa        | 0.10.0.post2 |
| Scipy          | 1.9.3        |
| Flask          | 2.2.3        |
---