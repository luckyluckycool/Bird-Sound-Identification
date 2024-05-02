from __future__ import annotations

from sqlalchemy import Column, SMALLINT, DOUBLE
from sqlalchemy.orm import declarative_base

from models.model_columns.LocationModelColumns import LOCATIONS_TABLE_NAME, LOCATION_ID_COLUMN, LATITUDE_COLUMN, \
    LONGITUDE_COLUMN

Base = declarative_base()


class LocationModel(Base):
    __tablename__ = LOCATIONS_TABLE_NAME
    location_id = Column(LOCATION_ID_COLUMN, SMALLINT, primary_key=True)
    latitude = Column(LATITUDE_COLUMN, DOUBLE)
    longitude = Column(LONGITUDE_COLUMN, DOUBLE)

    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"LocationId: {self.location_id}, Latitude: {self.latitude}, Longitude: {self.longitude}"
