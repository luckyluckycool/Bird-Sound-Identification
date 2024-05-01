from __future__ import annotations

from sqlalchemy import Column, SMALLINT
from sqlalchemy.orm import declarative_base

from models.model_columns.AreaModelColumns import AREA_TABLE_NAME, AREA_ID_COLUMN, LOCATION_ID1_COLUMN, \
    LOCATION_ID2_COLUMN, LOCATION_ID3_COLUMN, LOCATION_ID4_COLUMN, LOCATION_ID5_COLUMN, LOCATION_ID6_COLUMN

Base = declarative_base()


class AreaModel(Base):
    __tablename__ = AREA_TABLE_NAME
    areaId = Column(AREA_ID_COLUMN, SMALLINT, primary_key=True)
    locationId1 = Column(LOCATION_ID1_COLUMN, SMALLINT)
    locationId2 = Column(LOCATION_ID2_COLUMN, SMALLINT)
    locationId3 = Column(LOCATION_ID3_COLUMN, SMALLINT)
    locationId4 = Column(LOCATION_ID4_COLUMN, SMALLINT)
    locationId5 = Column(LOCATION_ID5_COLUMN, SMALLINT)
    locationId6 = Column(LOCATION_ID6_COLUMN, SMALLINT)

    def __init__(self, locationId1, locationId2, locationId3, locationId4, locationId5, locationId6):
        self.locationId1 = locationId1
        self.locationId2 = locationId2
        self.locationId3 = locationId3
        self.locationId4 = locationId4
        self.locationId5 = locationId5
        self.locationId6 = locationId6

    def getLocations(self) -> list[int]:
        return [self.locationId1, self.locationId2, self.locationId3, self.locationId4, self.locationId5,
                self.locationId6]

    def setLocations(self, location: list[int]) -> AreaModel:
        self.locationId1 = location[0]
        self.locationId2 = location[1]
        self.locationId3 = location[2]
        self.locationId4 = location[3]
        self.locationId5 = location[4]
        self.locationId6 = location[5]
        return self

