from pydantic import BaseModel
from datetime import datetime

class URLBase(BaseModel):
    url: str 
    target_url: str  # stores the target url


class URL(URLBase):
    is_active: bool     # inherits the class variable as well; determines if the url is active and delete
    clicks: int
 
    class Config:
        orm_mode = True     # for db relationship with sqlalchemy


class URLInfo(URL):     # (admin)details about the url
    id: int
    admin_url: str
    clicked_at: datetime
