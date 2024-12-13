from sqlalchemy import create_engine, Column, Integer, String, Float, Enum, Date, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime
import pymysql
import json
import os
from datetime import datetime






with open('/mnt/txt.txt' , 'r') as d:
    dicti = json.load(d)
PASS = dicti['mysql']
DATABASE_URI = f"mysql+pymysql://root:{PASS}@localhost:3306/abzar_database"
engine = create_engine(DATABASE_URI, echo=True)
Base = declarative_base()


Base = declarative_base()

# 1. مدل کاربران
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(String(50), unique=True, nullable=False)
    phone_number = Column(String(15), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    transaction_id = Column(String(50) , nullable=True)
    
    # ارتباط با جدول اشتراک‌ها
    subscriptions = relationship("UserSubscription", back_populates="user")

# 2. مدل پلن‌های اشتراک
class SubscriptionPlan(Base):
    __tablename__ = 'subscription_plans'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(20), nullable=True)
    price = Column(Float, nullable=False)
    duration_days = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # ارتباط با جدول اشتراک‌ها
    subscriptions = relationship("UserSubscription", back_populates="plan")

# 3. مدل اشتراک‌های کاربران
class UserSubscription(Base):
    __tablename__ = 'user_subscriptions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    plan_id = Column(Integer, ForeignKey('subscription_plans.id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(Enum('active', 'expired', 'canceled', name='subscription_status'), default='active')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # روابط
    user = relationship("User", back_populates="subscriptions")
    plan = relationship("SubscriptionPlan", back_populates="subscriptions")

def create_database():
    try:
        Base.metadata.create_all(engine)
        print("جداول با موفقیت ایجاد شدند.")
    except Exception as e:
        print(f"خطا در ایجاد جداول: {e}")

Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    create_database()
    free_plan =SubscriptionPlan(
        name = 'Free',
        description = 'بدون اشتراک',
        price = 0.0,
        duration_days = 1,
        created_at = datetime.now(),
        )
    one_month =SubscriptionPlan(
        name = 'One month',
        description = 'یک ماهه',
        price = 30000.0,
        duration_days = 30,
        created_at = datetime.now(),
        )
    two_month = SubscriptionPlan(
        name = 'Two month',
        description = 'دو ماهه',
        price = 50000.0,
        duration_days = 60,
        created_at = datetime.now(),
        )
    three_month = SubscriptionPlan(
        name = 'Three month',
        description = 'سه ماهه',
        price = 60000.0,
        duration_days = 60,
        created_at = datetime.now(),
        )
    try:
        session = Session()
        session.add(free_plan,one_month,two_month,three_month)
        session.commit()
    except Exception as e:
        print("plans are excist")
    

