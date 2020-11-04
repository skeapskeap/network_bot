from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SwList(Base):
    __tablename__ = 'switch_list'

    id = Column('id', Integer, primary_key=True)
    vendor = Column('vendor', String)
    name = Column('name', String, unique=True)
    ip = Column('ip', String)


engine = create_engine('sqlite:///hosts.db')
Base.metadata.create_all(bind=engine)
