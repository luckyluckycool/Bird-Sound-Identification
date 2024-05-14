from datetime import datetime

from dao.AbstractDao import AbstractDao
from models.AreaDetectionResultModel import AreaDetectionResultModel


class AreaDetectionResultDao(AbstractDao):
    def insert_area_detection_results(self, area_detection_results: list[AreaDetectionResultModel]):
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
        result = self.get_session().query(AreaDetectionResultModel.area_detection_time).distinct().order_by(
            AreaDetectionResultModel.area_detection_time).all()
        session.close()
        result = [res[0] for res in result]
        index = result.index(time)
        times = [result[index]]
        if index - 1 >= 0:
            times.insert(0, result[index - 1])
        if index + 1 < len(result):
            times.append(result[index + 1])
        return times

    def get_all_times(self):
        session = self.get_session()
        result = self.get_session().query(AreaDetectionResultModel.area_detection_time).distinct().all()
        session.close()
        return result
