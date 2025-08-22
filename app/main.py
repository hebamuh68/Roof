from fastapi import FastAPI
from app.api import search 
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

app.include_router(search.router)
