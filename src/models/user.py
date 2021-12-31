from sqlalchemy import Column, String

from src.db import Base


class User(Base):
    __tablename__ = "user"

    id = Column(String(26), primary_key=True)
    name = Column(String(10))
