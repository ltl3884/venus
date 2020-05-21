import os
from contextlib import contextmanager
from datetime import datetime

import yaml
from scrapy.utils.project import get_project_settings
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

settings = get_project_settings()

# declare a Mapping,this is the class describe map to table column
Base = declarative_base()
dirname = os.path.dirname(__file__)
path = os.path.join(dirname, "config.yml")
with open(path) as file:
    config = yaml.full_load(file)

m = config["mysql"]
engine = create_engine(
    "mysql://%s:%s@%s:%s/%s?charset=%s" % (m["username"], m["password"], m["host"], m["port"], m["db"], m["charset"]),
    encoding="utf8",
    echo=False
)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


@contextmanager
def scoped_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        Session.remove()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), nullable=True, default=None) #user_id
    user_name = Column(String(255), nullable=True, default=None) #nickname
    unique_id = Column(String(255), nullable=True, default=None) #unique_id
    aweme_count = Column(Integer, nullable=True, default=None) #aweme_count
    follower_count = Column(Integer, nullable=True, default=None) #follower_count
    user_score = Column(Integer, nullable=True, default=None) #user_score
    last_update_time = Column(DateTime, nullable=True, default=None) #last_update_time
    source_type = Column(String(255), nullable=True, default=None)
    category = Column(String(255), nullable=True, default=None)
    keyword = Column(String(255), nullable=True, default=None)
    created_at = Column(DateTime, nullable=True, default=datetime.now())
    updated_at = Column(DateTime, nullable=True, default=datetime.now())
    share_url = Column(String(255), nullable=True, default=None)
    avatar_larger = Column(String(255), nullable=True, default=None)


def map_orm_item(scrapy_item, sql_item):
    for k, v in scrapy_item.items():
        sql_item.__setattr__(k, v)
    return sql_item
