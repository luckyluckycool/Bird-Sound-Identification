from __future__ import annotations

from sqlalchemy import Column, SMALLINT, Float
from sqlalchemy.orm import declarative_base

from models.model_columns.LocationModelColumns import LOCATIONS_TABLE_NAME, LOCATION_ID_COLUMN, LATITUDE_COLUMN, \
    LONGITUDE_COLUMN

Base = declarative_base()


class LocationModel(Base):
    __tablename__ = LOCATIONS_TABLE_NAME
    locationId = Column(LOCATION_ID_COLUMN, SMALLINT, primary_key=True)
    latitude = Column(LATITUDE_COLUMN, Float)
    longitude = Column(LONGITUDE_COLUMN, Float)

    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def getLocationId(self) -> int:
        return self.locationId

    def setLocationId(self, locationId: int) -> LocationModel:
        self.locationId = locationId
        return self

    def getLatitude(self) -> float:
        return self.latitude

    def setLatitude(self, latitude: float) -> LocationModel:
        self.latitude = latitude
        return self

    def getLongitude(self) -> float:
        return self.longitude

    def setLongitude(self, longitude: float) -> LocationModel:
        self.longitude = longitude
        return self

    def __str__(self):
        return f"LocationId: {self.locationId}, Latitude: {self.latitude}, Longitude: {self.longitude}"
