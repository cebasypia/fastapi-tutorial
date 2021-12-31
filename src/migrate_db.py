from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

import config

DB_URL = f"mysql+pymysql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/test_db"
engine = create_engine(DB_URL, echo=True)

Base = declarative_base()


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
