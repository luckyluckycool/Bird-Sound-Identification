from datetime import datetime, timedelta

from sqlalchemy.sql import between

from dao.AbstractDao import AbstractDao
from models.AreaDetectionResultModel import AreaDetectionResultModel


class AreaDetectionResultDao(AbstractDao):
    def insert_area_detection_results(self, area_detection_results: list):
        session = self.get_session()
        session.add_all(area_detection_results)
        session.commit()
        session.close()

    def get_area_detection_results_by_time(self, time: datetime):
        session = self.get_session()
        result = session.query(AreaDetectionResultModel).filter(
            AreaDetectionResultModel.area_detection_time == time).all()
        session.close()
        return result

    def get_times(self, time: datetime):
        session = self.get_session()
        result = self.get_session().query(AreaDetectionResultModel.area_detection_time).filter(
            between(AreaDetectionResultModel.area_detection_time, time - timedelta(minutes=10),
                    time + timedelta(minutes=10))).distinct().all()
        session.close()
        return result

    def get_all_times(self):
        session = self.get_session()
        result = self.get_session().query(AreaDetectionResultModel.area_detection_time).distinct().all()
        session.close()
        return result
