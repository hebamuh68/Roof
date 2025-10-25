from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import apartment_api, search_api, user_api, auth_api
from app.schemas import user_sql, apartment_sql  # Required for SQLAlchemy relationships
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS for frontend dev server
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_api.router)
app.include_router(apartment_api.router)
app.include_router(user_api.router)
app.include_router(auth_api.router)
