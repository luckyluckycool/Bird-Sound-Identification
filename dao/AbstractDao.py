from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class AbstractDao(object):
    engine = create_engine("mariadb+mariadbconnector://root:111111@localhost:3307/bsi")
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
