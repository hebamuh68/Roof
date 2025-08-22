from fastapi import FastAPI
from app.api import search, apartment
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

app.include_router(search.router)
app.include_router(apartment.router)
