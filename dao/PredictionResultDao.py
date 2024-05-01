from dao.AbstractDao import AbstractDao
from models.DetectionResultModel import PredictionResultModel


class PredictionResultDao(AbstractDao):

    def get_prediction_result_entities(self) -> list[PredictionResultModel]:
        return self.session.query(PredictionResultModel).all()

    def add_prediction_result(self, entity: PredictionResultModel):
        self.session.add(entity)
        self.session.commit()
