from typing import Optional

import pymysql.cursors
from fastapi import FastAPI
from pydantic import BaseModel

import config


class User(BaseModel):
    name: str
    description: Optional[str]


app = FastAPI()


@app.get("/users/")
async def read_user() -> list:
    conn = pymysql.connect(
        host=config.DB_HOST,
        port=int(config.DB_PORT),
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        db="test_db",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

    try:
        with conn.cursor() as cursor:
            #            sql = "SELECT * FROM user WHERE id = %s"
            sql = "SELECT * FROM user"
            cursor.execute(sql, ())
            result = cursor.fetchall()
            print(type(result))
    finally:
        conn.close()
    return list(result)


@app.post("/users/")
async def create_user(user: User) -> User:
    conn = pymysql.connect(
        host=config.DB_HOST,
        port=int(config.DB_PORT),
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        db="test_db",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO user (name) values (%s)"
            cursor.execute(sql, (user.name))
            conn.commit()

    finally:
        conn.close()
    return user
