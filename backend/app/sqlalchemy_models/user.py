from sqlalchemy import Column, Integer, String
from app.database.database import Base
from sqlalchemy.dialects.postgresql import ARRAY


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    location = Column(String, nullable=False)
    flatmate_pref = Column(ARRAY(String), nullable=True)
    keywords = Column(ARRAY(String), nullable=True)