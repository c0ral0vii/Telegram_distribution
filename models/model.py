from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


class Account(BaseModel):
    __tablename__ = 'account'


class Proxy():
    __tablename__ = 'proxy'