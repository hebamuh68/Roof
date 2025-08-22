from fastapi import FastAPI
from app.api import apartment_api, search_api, user_api
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

app.include_router(search_api.router)
app.include_router(apartment_api.router)
app.include_router(user_api.router)
