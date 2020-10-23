from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy import create_engine
from datetime import datetime


Base = declarative_base()


"""
this is anly used one time to create the table in the database
can be done manualy but this is more simple
the table spec contain all the data 
"""


class Spec(Base):
    __tablename__ = 'spec'
    id = Column(Integer, primary_key=True)
    listing_id=Column(Integer, unique=False, nullable=False)
    palce_id = Column(Integer, unique=False, nullable=False)
    price = Column(Integer, unique=False, nullable=False)
    area = Column(Integer, unique=False, nullable=False)
    room_count = Column(Integer, unique=False, nullable=False)
    #date_mel = Column(DateTime, nullable=False)
    date_maj = Column(DateTime, nullable=True, default=datetime.utcnow)
    
    def __repr__(self):
        return "<Spec(palce_id='{}', price='{}', area={}, room_count={})>"\
                .format(self.palce_id, self.price, self.area, self.room_count)

DATABASE_URI = 'postgres+psycopg2://meilleursagents:pikachu42!@@localhost:5432/meilleursagents'
engine = create_engine(DATABASE_URI)


# used 1 time to create table 
# from models import Base, engine 
# Base.metadata.create_all(engine)


