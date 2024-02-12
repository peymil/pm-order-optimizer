from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Column, Integer, String, Text, Float, INT
from ..database import engine
Base = declarative_base()


class Order(Base):
    __tablename__ = 'Order'
    id = Column(Integer, primary_key=True, index=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    address = Column(Text)
    group = Column(INT)


Base.metadata.create_all(engine)