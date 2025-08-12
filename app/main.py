from fastapi import FastAPI
from app.api import search 


app = FastAPI()

app.include_router(search.router)
