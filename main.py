from fastapi import FastAPI, HTTPException
from . import schema
import validators
from . import models, schema
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . database import engine, get_db
import psycopg2
import psycopg
import psycopg_binary
from psycopg2.extras import RealDictCursor



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
async def read_root():
    return 'Welcome to URL Shortening API'


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)
    # handling bad request if the url is invalid (Leveraging on validators)


@app.post(('/url'))
async def create_url(url: schema.URLBase):
    if not validators.url(url.target_url):
        raise_bad_request(message='The URL is invalid')
    return f"TODO: Create database entry for: {url.target_url}"
    # this is a to do for the actual posting if the url is valid


@app.get('/{url_key}')
async def get_url_key():
    return


@app.get('/admin/{secret_key}')
def get_secret_key():
    return

@app.delete('/admin/{secret_key}')
def delete_secretkey():
    return