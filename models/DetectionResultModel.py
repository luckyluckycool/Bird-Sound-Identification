from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, INTEGER, SMALLINT, Boolean, TIMESTAMP
from sqlalchemy.orm import declarative_base

from models.model_columns.DetectionResultModelColumns import DETECTION_RESULTS_TABLE_NAME, ID_RESULT_COLUMN, \
    LOCATION_COLUMN, PREDICTION_RESULT_COLUMN, DETECTION_TIME_COLUMN

Base = declarative_base()


class PredictionResultModel(Base):
    __tablename__ = DETECTION_RESULTS_TABLE_NAME
    id = Column(ID_RESULT_COLUMN, INTEGER, primary_key=True)
    location = Column(LOCATION_COLUMN, SMALLINT)
    predictionResult = Column(PREDICTION_RESULT_COLUMN, Boolean)
    detectionTime = Column(DETECTION_TIME_COLUMN, TIMESTAMP)

    def __init__(self, location: int, predictionResult: bool):
        self.location = location
        self.predictionResult = predictionResult

    def getLocation(self) -> int:
        return self.location

    def setLocation(self, location: int) -> PredictionResultModel:
        self.location = location
        return self

    def getPredictionResult(self) -> bool:
        return self.predictionResult

    def setPredictionResult(self, predictionResult: bool) -> PredictionResultModel:
        self.predictionResult = predictionResult
        return self

    def getDetectionTime(self) -> datetime:
        return self.detectionTime

    def setDetectionTime(self, detectionTime: datetime) -> PredictionResultModel:
        self.detectionTime = detectionTime
        return self

    def __str__(self):
        return f'Location = {self.location}, result = {self.predictionResult}, time = {self.detectionTime}'
