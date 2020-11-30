from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from settings import AST_FW_DB_USER, AST_FW_DB_PWD, AST_FW_DB_ADDRESS

engine = create_engine(
    f'mysql+pymysql://{AST_FW_DB_USER}:{AST_FW_DB_PWD}@{AST_FW_DB_ADDRESS}')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class FWRec(Base):
    __tablename__ = 'permit_ip'
    id = Column(Integer, primary_key=True, default=None)
    created = Column(DateTime(timezone=True), server_default=func.now())
    ip = Column(String(19), unique=True, default=None)
    client = Column(String(100), default=None)
    koza_аpplication = Column(String(100), nullable=True, default=None)
    user = Column(String(30), nullable=True, default=None)


def search(key):
    reply = []
    key = f'%{key}%'
    results = session.query(FWRec).filter(FWRec.ip.like(key)).all()
    if not results:
        return False
    for result in results:
        reply.append(
                {'ip': result.ip,
                 'client': result.client}
            )
    return reply


if __name__ == '__main__':
    reply = search('95.181.128.104')
    if reply:
        for record in reply:
            print(f"{record['ip']} {record['client']}")
    else:
        print('No records found')
