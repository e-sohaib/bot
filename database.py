from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Index, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import pymysql
import json
import os





with open('/mnt/txt.txt' , 'r') as d:
    dicti = json.load(d)
PASS = dicti['mysql']
DATABASE_URI = f"mysql+pymysql://root:{PASS}@localhost:3306/abzar_database"
engine = create_engine(DATABASE_URI, echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(String(50), unique=True, nullable=False, index=True)
    date_joined = Column(DateTime, default=datetime.now())
    balance_curency = Column(String(50) ,nullable=True)
    balance_amount = Column(Float, default=0.0)
    daily_requests = Column(Integer , default=0)
    last_deposit_date = Column(DateTime, default=None)
    transaction_id = Column(String(50), unique=True, nullable=True)
    deposit_count = Column(Integer, default=0)
    max_requests = Column(Integer, default=3)
    lang = Column(String(2), nullable=True)

    __table_args__ = (
        Index('idx_telegram_id', 'telegram_id'),
    )

def create_database():
    try:
        Base.metadata.create_all(engine)
        print("جداول با موفقیت ایجاد شدند.")
    except SQLAlchemyError as e:
        print(f"خطا در ایجاد جداول: {e}")

Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    create_database()
