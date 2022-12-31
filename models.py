from .database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Urls(Base):
    __tablename__ = 'url_list'

    id = Column(Integer, primary_key= True, nullable= False)
    url = Column(String, nullable= False)
    target_url = Column(String, nullable= False)  # stores the target url
    admin_url = Column(String, nullable= False)
    is_active = Column(Boolean, nullable= True) 
    clicks = Column(Integer) 