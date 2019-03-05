from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Boolean, Integer, String

Base = declarative_base()


class FeedTimes(Base):
    __tablename__ = 'feedtime'
    id = Column(Integer, autoincrement=True, primary_key=True)
    feed_time = Column(Integer)
    feed_length = Column(Float)
    user = Column(String, nullable=True)
    success = Column(Boolean)
