from dao.PredictionResultDao import PredictionResultDao


class DataService:
    predictionResultDao = PredictionResultDao()

    def printPredictionResults(self):
        for predictionResult in self.predictionResultDao.get_prediction_result_entities():
            print(predictionResult)
