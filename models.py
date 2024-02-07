import database
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship



class Urls(Base):
    __tablename__ = 'url_list'

    id = Column(Integer, primary_key= True, nullable= False, index= True)
    target_url = Column(String, nullable= True)
    changed_url = Column(String, nullable= True)  # stores the converted target url
    is_active = Column(Boolean, default= True) 
    clicks = Column(Integer) 

    admin_data = relationship("AdminData", back_populates= "owner")


class AdminData(Base):
    __tablename__ = 'admin_data'

    id = Column(Integer, primary_key= True, nullable= False)
    target_url = Column(String, ForeignKey("url_list.target_url"), nullable= True)
    times_clicked = Column(Integer, nullable= False)
    secret_url_key = Column(String, nullable= False)

    owner = relationship("Urls", back_populates= 'admin_data')
