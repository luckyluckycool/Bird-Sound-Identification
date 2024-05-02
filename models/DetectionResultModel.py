from datetime import datetime

from sqlalchemy import Column, INTEGER, SMALLINT, Boolean, TIMESTAMP
from sqlalchemy.orm import declarative_base

from models.model_columns.DetectionResultModelColumns import DETECTION_RESULTS_TABLE_NAME, ID_DETECTION_RESULT_COLUMN, \
    LOCATION_COLUMN, DETECTION_TIME_COLUMN, AREA_COMPUTED_COLUMN

Base = declarative_base()


class DetectionResultModel(Base):
    __tablename__ = DETECTION_RESULTS_TABLE_NAME
    detection_result_id = Column(ID_DETECTION_RESULT_COLUMN, INTEGER, primary_key=True)
    location = Column(LOCATION_COLUMN, SMALLINT)
    detection_time = Column(DETECTION_TIME_COLUMN, TIMESTAMP)
    area_computed = Column(AREA_COMPUTED_COLUMN, Boolean)

    def __init__(self, location: int, detection_time: datetime, area_computed: bool):
        self.location = location
        self.detection_time = detection_time
        self.area_computed = area_computed

    def __str__(self):
        return f'Location = {self.location}, time = {self.detection_time}'
