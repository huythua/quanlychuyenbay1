from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, event, Boolean, Float
from datetime import datetime
from sqlalchemy.orm import relationship
from app import app, db
from flask_login import UserMixin
import enum
import hashlib
from caesar_cipher import *

SHIFT_CAESAR = 3

class RoleEnum(enum.Enum):
    ADMIN = "admin"
    PASSENGER = "passenger"

class BaseModel(db.Model):
    __abstract__=True
    id = Column(Integer, primary_key=True, autoincrement=True)
class TuyenBay(BaseModel):
    __tablename__ = 'TuyenBay'
    name = Column(String(50), nullable=False)
    diemdi = Column(String(50), nullable=False)
    diemden = Column(String(50), nullable=False)
    quangduong = Column(String(50), nullable=False)
    chuyenbay = relationship('ChuyenBay', backref='TuyenBay', lazy=False)
    def __str__(self):
        return self.name

class ChuyenBay(BaseModel):
    __tablename__= 'ChuyenBay'
    name = Column(String(50), nullable=False)
    image = Column(String(100))
    tinhtrang = Column(Boolean, default=True)
    ngaybay = Column(DateTime, default=datetime.now())
    giave = Column(Float, default=0)
    tuyenbay_id= Column(Integer, ForeignKey(TuyenBay.id),nullable=False)
    def __str__(self):
        return self.name

class Flight(db.Model):
    __tablename__ = 'flight'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)
    image = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class Booking(db.Model):
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", backref='bookings')

    flight_id = Column(Integer, ForeignKey('flight.id'), nullable=False)
    flight = relationship("Flight")

    time = Column(DateTime, default=datetime.now())

    @property
    def passenger_name(self):
        return self.user.name


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    _name = Column(String(50), nullable=False)
    _username = Column(String(50), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)

    def __str__(self):
        return self.name

    @property
    def name(self):
        return caesar_decrypt(self._name, SHIFT_CAESAR)

    @name.setter
    def name(self, value):
        self._name = caesar_encrypt(value, SHIFT_CAESAR)

    @property
    def username(self):
        return caesar_decrypt(self._username, SHIFT_CAESAR)

    @username.setter
    def username(self, value):
        self._username = caesar_encrypt(value, SHIFT_CAESAR)



if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

        khachhang_user = User(name="Khach hang",
                              username="khachhang",
                              password=str(hashlib.md5("123".encode('utf-8')).hexdigest()),
                              role=RoleEnum.PASSENGER)

        thanhdat_user = User(name="Thanh Dat",
                             username="thanhdat",
                             password=str(hashlib.md5("123".encode('utf-8')).hexdigest()),
                             role=RoleEnum.PASSENGER)

        admin_user = User(name="admin",
                          username="admin",
                          password=str(hashlib.md5("123".encode('utf-8')).hexdigest()),
                          role=RoleEnum.ADMIN)
        db.session.add_all([khachhang_user, thanhdat_user, admin_user])

        f1 = Flight(name="Hà Nội tới TP.HCM", price=2400000, image="https://wallpapercave.com/wp/9aungfd.jpg")
        f2 = Flight(name="Nha Trang tới Phú Quốc", price=2500000, image="https://wallpapercave.com/wp/9aungfd.jpg")
        f3 = Flight(name="Đà Lạt tới Đà Nẵng", price=2000000, image="https://wallpapercave.com/wp/9aungfd.jpg")
        f4 = Flight(name="Cà Mau tới Cần Thơ", price=1500000, image="https://wallpapercave.com/wp/9aungfd.jpg")
        f5 = Flight(name="Hải Phòng tới Huế", price=3000000, image="https://wallpapercave.com/wp/9aungfd.jpg")
        f6 = Flight(name="Cần Thơ tới Nha Trang", price=1700000, image="https://wallpapercave.com/wp/9aungfd.jpg")
        f7 = Flight(name="Cà Mau tới Buôn Ma Thuột", price=2600000, image="https://wallpapercave.com/wp/9aungfd.jpg")
        f8 = Flight(name="Hải Phòng tới Huế", price=2900000, image="https://wallpapercave.com/wp/9aungfd.jpg")

        db.session.add_all([f1, f2, f3, f4, f5, f6, f7, f8])



        b1 = Booking(user=thanhdat_user, flight=f4)
        b2 = Booking(user=thanhdat_user, flight=f6)
        b3 = Booking(user=thanhdat_user, flight=f5)

        b4 = Booking(user=khachhang_user, flight=f2)
        b5 = Booking(user=khachhang_user, flight=f8)
        b6 = Booking(user=khachhang_user, flight=f5)

        db.session.add_all([b1, b2, b3, b4, b5, b6])

        t1 = TuyenBay(name='Ngoài nước', diemdi='TP. HCM', diemden='Hà Nội', quangduong='1200km')
        t2 = TuyenBay(name='Quốc tê', diemdi='TP. HCM', diemden='Huế', quangduong='64000km')
        c1 = ChuyenBay(name=t1.diemdi + t1.diemden, image='https://wallpapercave.com/wp/9aungfd.jpg', giave=2000000, tuyenbay_id=1)
        c2 = ChuyenBay(name=t2.diemdi + t2.diemden, image='https://wallpapercave.com/wp/9aungfd.jpg', giave=3000000, tuyenbay_id=2)
        db.session.add(t1)
        db.session.add(t2)
        db.session.add(c1)
        db.session.add(c2)


        db.session.commit()
