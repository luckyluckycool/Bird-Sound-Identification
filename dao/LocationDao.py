from dao.AbstractDao import AbstractDao
from models.LocationModel import LocationModel


class LocationDao(AbstractDao):
    def get_locations(self):
        session = self.get_session()
        result = session.query(LocationModel).order_by(LocationModel.location_id).all()
        session.close()
        return result
