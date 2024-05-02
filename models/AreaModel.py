from sqlalchemy import Column, SMALLINT
from sqlalchemy.orm import declarative_base

from models.model_columns.AreaModelColumns import AREA_TABLE_NAME, AREA_ID_COLUMN, LOCATION_ID1_COLUMN, \
    LOCATION_ID2_COLUMN, LOCATION_ID3_COLUMN, LOCATION_ID4_COLUMN, LOCATION_ID5_COLUMN, LOCATION_ID6_COLUMN

Base = declarative_base()


class AreaModel(Base):
    __tablename__ = AREA_TABLE_NAME
    area_id = Column(AREA_ID_COLUMN, SMALLINT, primary_key=True)
    location_id1 = Column(LOCATION_ID1_COLUMN, SMALLINT)
    location_id2 = Column(LOCATION_ID2_COLUMN, SMALLINT)
    location_id3 = Column(LOCATION_ID3_COLUMN, SMALLINT)
    location_id4 = Column(LOCATION_ID4_COLUMN, SMALLINT)
    location_id5 = Column(LOCATION_ID5_COLUMN, SMALLINT)
    location_id6 = Column(LOCATION_ID6_COLUMN, SMALLINT)

    def __init__(self, location_id1, location_id2, location_id3, location_id4, location_id5, location_id6):
        self.location_id1 = location_id1
        self.location_id2 = location_id2
        self.location_id3 = location_id3
        self.location_id4 = location_id4
        self.location_id5 = location_id5
        self.location_id6 = location_id6

    def get_locations(self) -> list[int]:
        return [self.location_id1, self.location_id2, self.location_id3, self.location_id4, self.location_id5,
                self.location_id6]

    def __str__(self):
        return (
            f'area-{self.area_id}: [{self.location_id1}, {self.location_id2}, {self.location_id3}, {self.location_id4},'
            f' {self.location_id5}, {self.location_id6}]')
