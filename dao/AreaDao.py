from sqlalchemy import or_

from dao.AbstractDao import AbstractDao
from models.AreaModel import AreaModel


class AreaDao(AbstractDao):
    def get_areas(self):
        session = self.get_session()
        result = self.get_session().query(AreaModel).all()
        session.close()
        return result

    def get_areas_by_locations_ids(self, location_ids: list[int]) -> list[AreaModel]:
        session = self.get_session()
        result = session.query(AreaModel).filter(or_(
            AreaModel.location_id1.in_(location_ids),
            AreaModel.location_id2.in_(location_ids),
            AreaModel.location_id3.in_(location_ids),
            AreaModel.location_id4.in_(location_ids),
            AreaModel.location_id5.in_(location_ids),
            AreaModel.location_id6.in_(location_ids))).all()
        session.close()
        return result
