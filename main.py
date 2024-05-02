import json
import os

# dataService = DataService()

#areaDao = AreaDao()
# locationDao = LocationDao()

# detectionResultDao = DetectionResultDao()

# results = detectionResultDao.getNotComputedDetectionResults()
# for result in results:
# print(result)

# areas = areaDao.getAreasByLocationsId([1, 2, 3, 4, 5, 6])
# for area in areas:
#     print(area)

# areaService = AreaService()
# # areaService.calculateAreaDetections()
#
#
# results = areaService.getAllTimes()
#
# print(results[len(results)//2])
#
# #

with open('configs/config.json') as config_file:
    config = json.load(config_file)