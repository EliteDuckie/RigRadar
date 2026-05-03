from sqlalchemy import Column, Integer, String, DECIMAL, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class CPU(Base):
    __tablename__ = 'cpus'

    id = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(String(50))
    model_name = Column(String(255))
    socket_type = Column(String(50))
    core_count = Column(Integer)
    tdp = Column(Integer)
    lowest_price = Column(DECIMAL(10, 2))
    product_url = Column(Text)
    currency = Column(String(3), default="CAD")