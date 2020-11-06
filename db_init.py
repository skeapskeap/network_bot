from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SwList(Base):
    __tablename__ = 'switch_list'

    index = Column('index', Integer, primary_key=True)
    vendor = Column('vendor', String)
    name = Column('name', String, unique=True)
    ip = Column('ip', String)

    def __repr__(self):
        return f'<SwList({self.name} {self.ip})>'


engine = create_engine('sqlite:///hosts.db', echo=False)
Base.metadata.create_all(bind=engine)
