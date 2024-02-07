from fastapi import FastAPI, HTTPException, Response, status, Depends, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import update, insert
import models, schemas, database
#from models import Urls
from database import engine
import validators
import secrets
import random
import string

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

clicks = 0

@app.post("/urlshortener/", status_code= status.HTTP_201_CREATED)
async def create_url(url: schemas.URLBase, db: Session= Depends(database.get_db)): 

    if not validators.url(url.target_url):
        raise_bad_request(message='The URL is invalid')

    key = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
    secret_key = "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(8))

    db_url = models.Urls(
        target_url=url.target_url, changed_url= key, is_active= True
    )

    clicks_query = db.query(models.AdminData.times_clicked).filter(models.AdminData.target_url==url.target_url)
    clicks = clicks_query.first()
    
    if clicks == None:
        clicks = 1
        admin_db =  models.AdminData( 
        target_url = url.target_url, times_clicked=clicks, secret_url_key= secret_key
        )
        db.add(admin_db)
        detail = f"Succesfully shortened to {key}"

    else:
        clicks = clicks.times_clicked + 1
        stmt = update(models.AdminData).values(times_clicked=clicks, target_url = url.target_url, secret_url_key= secret_key).where(models.AdminData.target_url == url.target_url)
        admin_db =  db.execute(stmt,  execution_options={"synchronize_session": "auto"})
        detail = f"Succesfully shortened to {key}"
    
    db.add(db_url)    
    db.commit()
    db.refresh(db_url)
   
    return detail


@app.get("/{url_key}", status_code= status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect_url(url_key: str, request: Request ,db: Session= Depends(database.get_db)):
    converted_url = db.query(models.Urls).filter(models.Urls.changed_url==url_key).first()
    if not converted_url:
        raise HTTPException(status_code=404, detail="url does not exist")
    else:
        detail = "Successfully Redirected"
        return detail