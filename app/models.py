from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, event,Time, Boolean, Float, JSON
from datetime import datetime
from sqlalchemy.orm import relationship, declarative_base
from app import app, db
from flask_login import UserMixin
import enum
import hashlib
from caesar_cipher import *

SHIFT_CAESAR = 3

Base = declarative_base()
class RoleEnum(enum.Enum):
    ADMIN = "admin"
    PASSENGER = "passenger"

class BaseModel(db.Model):
    __abstract__=True
    id = Column(Integer, primary_key=True, autoincrement=True)
class SanBay(BaseModel):
    __tablename__ = 'sanbay'
    name = Column(String(50), nullable=False)
    quocgia = Column(String(50), nullable=False)
    tuyenbay = relationship('TuyenBay', backref='sanbay',lazy=True)
    sanbaytrunggian = relationship('SanBayTrungGian', back_populates='sanbay', uselist=False)

class MayBay(BaseModel):
    __tablename__= 'maybay'
    name = Column(String(50), nullable=False)
    chuyenbay = relationship('ChuyenBay', backref='maybay', lazy=True)
class TuyenBay(BaseModel):
    __tablename__ = 'tuyenbay'
    name = Column(String(50), nullable=False)
    diemdi = Column(String(50), nullable=False)
    diemden = Column(String(50), nullable=False)
    quangduong = Column(String(50), nullable=False)
    sanbay_id=Column(Integer, ForeignKey('sanbay.id'),nullable=False)
    chuyenbay = relationship('ChuyenBay', backref='tuyenbay', lazy=False)
    sanbaytrunggian1 = Column(String(50), nullable=True)
    sanbaytrunggian2 = Column(String(50), nullable=True)
    sanbaytrunggian = relationship('SanBayTrungGian',)
    def __str__(self):
        return self.name
class SanBayTrungGian(BaseModel):
    __tablename__ = 'sanbaytrunggian'
    name = Column(String(50), nullable=False)
    ghichu = Column(String(50), nullable=False)
    time = Column(Time, nullable=10)
    tuyenbay_id = Column(Integer, ForeignKey('tuyenbay.id'), nullable=False)
    sanbay_id = Column(Integer,ForeignKey('sanbay.id'), unique=True, nullable=False)
    sanbay = relationship('SanBay', back_populates='sanbaytrunggian')
class ChuyenBay(BaseModel):
    __tablename__= 'chuyenbay'
    name = Column(String(50), nullable=False)
    image = Column(String(100))
    tinhtrang = Column(Boolean, default=True)
    ngaybay = Column(DateTime, default=datetime.now())
    tuyenbay_id= Column(Integer, ForeignKey('tuyenbay.id'),nullable=False)
    maybay_id = Column(Integer, ForeignKey('maybay.id'), nullable=False)
    soluongghe1 = Column(Integer,default=0)
    soluongghe2 = Column(Integer, default=0)
    soluonghe = relationship('SoLuongGhe',backref='chuyenbay')
    def __str__(self):
        return self.name
class GiaVe(db.Model):
    __tablename__ = 'giave'
    hangve_id = Column(Integer, ForeignKey('hangghe.id'), primary_key=True)
    tuyenbay_id = Column(Integer, ForeignKey('tuyenbay.id'), primary_key=True)
    giave = Column(Float,default=0)
    hangghe = relationship('HangGhe', backref='giave')
    tuyenbay = relationship('TuyenBay', backref='giave')
class HangGhe(BaseModel):
    __tablename__ = 'hangghe'
    name = Column(String(50), nullable=False)
    ghe = relationship('Ghe', backref='hanghe')
class Ghe(BaseModel):
    __tablename__ = 'ghe'
    name = Column(String(50), nullable=False)
    hangghe_id = Column(Integer, ForeignKey('hangghe.id'))
    soluongghe = relationship('SoLuongGhe', backref='ghe')
class SoLuongGhe(db.Model):
    __tablename__ = 'soluongghe'
    id = Column(Integer, primary_key=True)
    tinhtrang = Column(Boolean, default=False)
    ghe_id = Column(Integer, ForeignKey('ghe.id'), nullable=False)
    chuyenbay_id = Column(Integer, ForeignKey('chuyenbay.id'), nullable=False)














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

        # t1 = TuyenBay(name='Ngoài nước', diemdi='TP. HCM', diemden='Hà Nội', quangduong='1200km')
        # t2 = TuyenBay(name='Quốc tê', diemdi='TP. HCM', diemden='Huế', quangduong='64000km')
        # c1 = ChuyenBay(name=t1.diemdi + t1.diemden, image='https://wallpapercave.com/wp/9aungfd.jpg', giave=2000000, tuyenbay_id=1)
        # c2 = ChuyenBay(name=t2.diemdi + t2.diemden, image='https://wallpapercave.com/wp/9aungfd.jpg', giave=3000000, tuyenbay_id=2)
        # db.session.add(t1)
        # db.session.add(t2)
        # db.session.add(c1)
        # db.session.add(c2)
        sb1 = SanBay(name='Sân bay Hồ Chí Minh', quocgia='Việt Nam')
        sb2 = SanBay(name='Sân bay Hà Nội', quocgia='Việt Nam')
        sb3 = SanBay(name='Sân bay Pháp', quocgia='Pháp')
        sb4 = SanBay(name='Sân bay Hongkong', quocgia='Trung Quốc')
        sb5 = SanBay(name='Sân bay Tokyo', quocgia='Nhật Bản')
        sb6 = SanBay(name='Sân bay Seul', quocgia='Hàn Quốc')
        db.session.add_all([sb1, sb2, sb3, sb4, sb5, sb6])

        mb1 = MayBay(name='Máy bay 1')
        mb2 = MayBay(name='Máy bay 2')
        mb3 = MayBay(name='Máy bay 3')
        mb4 = MayBay(name='Máy bay 4')
        mb5 = MayBay(name='Máy bay 5')
        mb6 = MayBay(name='Máy bay 6')
        db.session.add_all([mb1, mb2, mb3, mb4, mb5, mb6])

        tb1 = TuyenBay(name='Quốc tế', diemdi=sb1.name, diemden=sb6.name, quangduong=20000, sanbay_id=1, sanbaytrunggian1=sb2.name, sanbaytrunggian2=sb3.name)
        tb2 = TuyenBay(name='Trong nước', diemdi=sb1.name, diemden=sb2.name, quangduong=20000, sanbay_id=1)

        db.session.add_all([tb1,tb2])

        hangghe1 = HangGhe(name='Hạng 1')
        hangghe2 = HangGhe(name='Hạng 2')
        db.session.add_all([hangghe1, hangghe2])

        g1 = Ghe(name='001', hangghe_id=1)
        g2 = Ghe(name='002', hangghe_id=1)
        g3 = Ghe(name='003', hangghe_id=1)
        g4 = Ghe(name='004', hangghe_id=1)
        g5 = Ghe(name='005', hangghe_id=1)
        g6 = Ghe(name='006', hangghe_id=1)
        g7 = Ghe(name='007', hangghe_id=1)
        g8 = Ghe(name='008', hangghe_id=1)
        g9 = Ghe(name='009', hangghe_id=1)
        g10 = Ghe(name='010', hangghe_id=1)
        g11 = Ghe(name='011', hangghe_id=2)
        g12 = Ghe(name='012', hangghe_id=2)
        g13 = Ghe(name='013', hangghe_id=2)
        g14 = Ghe(name='014', hangghe_id=2)
        g15 = Ghe(name='015', hangghe_id=2)
        g16 = Ghe(name='016', hangghe_id=2)
        g17 = Ghe(name='017', hangghe_id=2)
        g18 = Ghe(name='018', hangghe_id=2)
        g19 = Ghe(name='019', hangghe_id=2)
        db.session.add_all([g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12, g13, g14, g15, g16, g17, g18, g19])

        gv1 = GiaVe(giave=2000000, hangve_id=1, tuyenbay_id=1)
        gv2 = GiaVe(giave=3000000, hangve_id=2, tuyenbay_id=1)
        gv3 = GiaVe(giave=1000000, hangve_id=1, tuyenbay_id=2)
        gv4 = GiaVe(giave=1500000, hangve_id=2, tuyenbay_id=2)
        db.session.add_all([gv1, gv2, gv3, gv4])

        ngay=datetime(2024,2,12,12,40,00)
        cb1 = ChuyenBay(tuyenbay_id=1, maybay_id=1, soluongghe1= 5, soluongghe2= 9,ngaybay=ngay, tinhtrang=True,image="https://wallpapercave.com/wp/9aungfd.jpg", name=' ')
        cb2 = ChuyenBay(tuyenbay_id=2, maybay_id=2, soluongghe1=10, soluongghe2= 6,ngaybay=ngay, tinhtrang=True,
                        image="https://wallpapercave.com/wp/9aungfd.jpg", name=' ')
        db.session.add_all([cb1,cb2])

        ghe1cb1= SoLuongGhe()


        db.session.commit()
