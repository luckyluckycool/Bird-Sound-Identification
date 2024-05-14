from datetime import datetime

from dao.AreaDao import AreaDao
from dao.AreaDetectionResultDao import AreaDetectionResultDao
from dao.DetectionResultDao import DetectionResultDao
from models.AreaDetectionResultModel import AreaDetectionResultModel


class AreaService:
    detectionResultDao: DetectionResultDao
    areaDetectionResultDao: AreaDetectionResultDao
    areaDao: AreaDao

    def __init__(self):
        self.detectionResultDao = DetectionResultDao()
        self.areaDetectionResultDao = AreaDetectionResultDao()
        self.areaDao = AreaDao()

    def calculate_area_detections(self):
        time_groups = {}
        detection_result_ids = []
        detection_results = self.detectionResultDao.get_not_computed_detection_results()
        for detectionResult in detection_results:
            detection_result_ids.append(detectionResult.detection_result_id)
            minutes = (detectionResult.detection_time.minute // 10) * 10
            rounded_time = detectionResult.detection_time.replace(minute=minutes, second=0, microsecond=0)
            if rounded_time in time_groups:
                time_groups[rounded_time].append(detectionResult)
            else:
                time_groups[rounded_time] = [detectionResult]
        area_detections = []
        for key, value in time_groups.items():
            locations_ids = [x.location for x in value]
            areas = self.areaDao.get_areas_by_locations_ids(locations_ids)
            for area in areas:
                area_locations = area.get_locations()
                area_counter = 0
                for area_location in area_locations:
                    if area_location in locations_ids:
                        area_counter += 1
                area_detections.append(AreaDetectionResultModel(areaId=area.area_id, area_detection_result=area_counter,
                                                                area_detection_time=key))
        self.areaDetectionResultDao.insert_area_detection_results(area_detections)
        self.detectionResultDao.update_area_computed(detection_result_ids)
        return len(detection_results)

    def get_area_detection_results_by_time(self, time: datetime):
        area_detections = self.areaDetectionResultDao.get_area_detection_results_by_time(time)
        area_detections_dict = {}
        for area_detection in area_detections:
            area_detections_dict[area_detection.area_id] = area_detection.area_detection_result
        return area_detections_dict

    def get_times_for_map(self, time: datetime):
        return self.areaDetectionResultDao.get_times(time)

    def get_all_times(self):
        return [time[0] for time in self.areaDetectionResultDao.get_all_times()]
