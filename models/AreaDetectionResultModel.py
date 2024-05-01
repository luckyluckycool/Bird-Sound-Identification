from datetime import datetime

from sqlalchemy import Column, SMALLINT, BOOLEAN, TIMESTAMP
from sqlalchemy.orm import declarative_base

from models.model_columns.AreaDetectionResultModelColumns import AREA_DETECTION_RESULT_TABLE_NAME, RESULT_ID_COLUMN, \
    AREA_DETECTION_RESULT_COLUMN, AREA_DETECTION_TIME_COLUMN

Base = declarative_base()


class AreaDetectionResultModel(Base):
    __tablename__ = AREA_DETECTION_RESULT_TABLE_NAME
    resultId = Column(RESULT_ID_COLUMN, SMALLINT, primary_key=True)
    areaId = Column(RESULT_ID_COLUMN, SMALLINT)
    areaDetectionResult = Column(AREA_DETECTION_RESULT_COLUMN, BOOLEAN)
    areaDetectionTime = Column(AREA_DETECTION_TIME_COLUMN, TIMESTAMP)

    def __init__(self, areaId: int, areaDetectionResult: bool, areaDetectionTime: datetime):
        self.areaId = areaId
        self.areaDetectionResult = areaDetectionResult
        self.areaDetectionTime = areaDetectionTime

    