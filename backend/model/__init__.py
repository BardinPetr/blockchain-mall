from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

SQLALCHEMY_DATABASE_URL = r"postgresql://ogjgvcnbigxakp:fcfb3a56b1b44c4042d76e30aff2c50676070b438e07cd9b933ba50f4a46b4b8@ec2-34-255-225-151.eu-west-1.compute.amazonaws.com:5432/ddvhkkom56dup5"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()


def create_session():
    return scoped_session(sessionmaker(bind=engine))()