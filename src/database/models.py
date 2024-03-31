from sqlalchemy import Column, Integer, String, JSON, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MyBase(Base):
    __abstract__ = True

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.c}


class Contact(MyBase):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    phone_number = Column(String(15))
    birth_date = Column(Date)
    additional_data = Column(JSON, nullable=True)
