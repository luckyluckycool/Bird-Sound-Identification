from sqlalchemy.sql import update

from dao.AbstractDao import AbstractDao
from models.DetectionResultModel import DetectionResultModel


class DetectionResultDao(AbstractDao):

    def get_not_computed_detection_results(self) -> list[DetectionResultModel]:
        session = self.get_session()
        result = session.query(DetectionResultModel).filter(DetectionResultModel.area_computed == 0).all()
        session.close()
        return result

    def update_area_computed(self, detection_result_ids: list[int]):
        session = self.get_session()
        stmt = update(DetectionResultModel).where(
            DetectionResultModel.detection_result_id.in_(detection_result_ids)).values(area_computed=True)
        session.execute(stmt)
        session.commit()
        session.close()
