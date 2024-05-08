from sqlalchemy import Column, Integer, String
from database import Base


class Users(Base):
    __tablename__: str = 'users'

    id: int = Column(Integer, primary_key=True, nullable=False)
    email: str = Column(String, nullable=False)
    hashed_password: str = Column(String, nullable=False)
