from datetime import datetime

from sqlalchemy import Column, SMALLINT, TIMESTAMP
from sqlalchemy.orm import declarative_base

from models.model_columns.AreaDetectionResultModelColumns import AREA_DETECTION_RESULT_TABLE_NAME, \
    AREA_RESULT_ID_COLUMN, AREA_DETECTION_RESULT_COLUMN, AREA_DETECTION_TIME_COLUMN, AREA_ID_COLUMN

Base = declarative_base()


class AreaDetectionResultModel(Base):
    __tablename__ = AREA_DETECTION_RESULT_TABLE_NAME
    result_id = Column(AREA_RESULT_ID_COLUMN, SMALLINT, primary_key=True)
    area_id = Column(AREA_ID_COLUMN, SMALLINT)
    area_detection_result = Column(AREA_DETECTION_RESULT_COLUMN, SMALLINT)
    area_detection_time = Column(AREA_DETECTION_TIME_COLUMN, TIMESTAMP)

    def __init__(self, areaId: int, area_detection_result: int, area_detection_time: datetime):
        self.area_id = areaId
        self.area_detection_result = area_detection_result
        self.area_detection_time = area_detection_time
