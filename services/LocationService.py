from dao.AreaDao import AreaDao
from dao.DetectionResultDao import DetectionResultDao
from dao.LocationDao import LocationDao


class LocationService:
    predictionResultDao: DetectionResultDao
    areaDao: AreaDao
    locationDao: LocationDao

    def __init__(self):
        self.predictionResultDao = DetectionResultDao()
        self.areaDao = AreaDao()
        self.locationDao = LocationDao()

    def get_areas_with_locations(self):
        areas = self.areaDao.get_areas()
        locations = self.locationDao.get_locations()
        lat_c = 0
        lng_c = 0
        for location in locations:
            lat_c += location.latitude
            lng_c += location.longitude
        lat_c /= len(locations)
        lng_c /= len(locations)
        areas_dict = {}
        for area in areas:
            location_dict = {}
            for index, location_id in enumerate(area.get_locations()):
                location_dict[index] = next(([location.latitude, location.longitude] for location in locations if
                                            location.location_id == location_id), None)
            areas_dict[area.area_id] = location_dict
        return areas_dict, [lat_c, lng_c]
