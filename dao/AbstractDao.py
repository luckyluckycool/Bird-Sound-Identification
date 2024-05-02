from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class AbstractDao(object):
    engine = create_engine("mariadb+mariadbconnector://root:111111@localhost:3307/bsi", echo=False, pool_size=5,
                           max_overflow=10)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)

    def get_session(self):
        return self.Session()
