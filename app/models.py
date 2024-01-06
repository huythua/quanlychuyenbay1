from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, event,Time, Boolean, Float
from datetime import datetime
from sqlalchemy.orm import relationship, declarative_base
from app import app, db
from flask_login import UserMixin
import enum
import hashlib
Base = declarative_base()
class RoleEnum(enum.Enum):
    ADMIN = "admin"
    PASSENGER = "passenger"

class HinhThucThanhToan(enum.Enum):
    CHUYENKHOAN= "Chuyển khoản"
    TIENMAT = "Tiền mặt"
class BaseModel(db.Model):
    __abstract__=True
    id = Column(Integer, primary_key=True, autoincrement=True)
class MayBay(BaseModel):
    __tablename__= 'maybay'
    name = Column(String(50), nullable=False)
    chuyenbay = relationship('ChuyenBay', backref='maybay', lazy=True)
    def __str__(self):
        return self.name
class TuyenBay(BaseModel):
    __tablename__ = 'tuyenbay'
    name = Column(String(50), nullable=False, unique= True )
    diemdi = Column(String(50), nullable=False)
    diemden = Column(String(50), nullable=False)
    sanbay_id = Column(Integer, ForeignKey('sanbay.id'), nullable=False)
    quangduong = Column(String(50), nullable=False)
    sanbaytrunggians = relationship('SanBayTrungGian',backref='tuyenbay')
    giave = relationship('GiaVe', backref='tuyenbay', lazy=True)
    def __str__(self):
        return self.name
class SanBay(BaseModel):
    __tablename__ = 'sanbay'
    name = Column(String(50), nullable=False, unique=True)
    quocgia = Column(String(50), nullable=False)
    sanbaytrunggians = relationship('SanBayTrungGian', backref='sanbay', lazy=True)
    tuyenbays = relationship('TuyenBay', backref='sanbay', lazy=True)
    def __str__(self):
        return self.name
class SanBayTrungGian(db.Model):
    __tablename__ = 'sanbaytrunggian'
    ghichu = Column(String(50), nullable=False)
    time = Column(String(20), default=10)
    tuyenbay_id = Column(Integer, ForeignKey('tuyenbay.id'), primary_key=True, nullable=False)
    sanbay_id = Column(Integer, ForeignKey('sanbay.id'), primary_key=True, nullable=False)
    def __str__(self):
        return self.sanbay.name
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
    thongtinve = relationship('ThongTinVe', backref='chuyenbay')
    tuyenbay = relationship('TuyenBay', backref='chuyenbay', lazy=False)
    def __str__(self):
        return self.name
class GiaVe(db.Model):
    __tablename__ = 'giave'
    hangghe_id = Column(Integer, ForeignKey('hangghe.id'), primary_key=True)
    tuyenbay_id = Column(Integer, ForeignKey('tuyenbay.id'), primary_key=True)
    giave = Column(Float,default=0)

class HangGhe(BaseModel):
    __tablename__ = 'hangghe'
    name = Column(String(50), nullable=False)
    ghe = relationship('Ghe', backref='hangghe')
    giave = relationship('GiaVe', backref='hangghe')
    def __str__(self):

        return self.name
class Ghe(BaseModel):
    __tablename__ = 'ghe'
    name = Column(String(50), nullable=False)
    hangghe_id = Column(Integer, ForeignKey('hangghe.id'))
    soluongghe = relationship('SoLuongGhe', backref='ghe')
    def __str__(self):

        return self.name
class SoLuongGhe(db.Model):
    __tablename__ = 'soluongghe'
    id = Column(Integer, primary_key=True)
    tinhtrang = Column(Boolean, default=False)
    ghe_id = Column(Integer, ForeignKey('ghe.id'), nullable=False)
    chuyenbay_id = Column(Integer, ForeignKey('chuyenbay.id'), nullable=False)
    thongtinve = relationship('ThongTinVe', backref='soluongghe')
    def __str__(self):

        return self.name

class ThongTinTaiKhoan(db.Model):
    __tablename__ = 'thongtintaikhoan'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, )
    name = Column(String(50),nullable=False)
    diachi = Column(String(50),nullable=False)
    cmnd = Column(String(50),nullable=False)
    sdt = Column(String(50),nullable=False)
    email = Column(String(50),nullable=False)
    user = relationship('User', uselist=False, back_populates='thongtintaikhoan')
    thongtinve = relationship('ThongTinVe', backref='thongtintaikhoan')
    def __str__(self):

        return self.name
class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    username = Column(String(50),nullable=False)
    password = Column(String(50),nullable=False)
    image = Column(String(100),nullable=True)
    thongtintaikhoan = relationship('ThongTinTaiKhoan', back_populates='user')
    role = Column(Enum(RoleEnum), nullable=False)
    def __str__(self):
        return self.name
class ThongTinVe(BaseModel):
    __tablename__= 'thongtinve'
    thongtintaikhoan_id = Column(Integer, ForeignKey('thongtintaikhoan.user_id'), nullable=False)
    chuyenbay_id = Column(Integer, ForeignKey('chuyenbay.id'), nullable=False)
    soluongghe_id = Column(Integer, ForeignKey('soluongghe.id'), nullable=False)
    hoadon_id = relationship('HoaDon', backref='thongtinve')
class HoaDon(BaseModel):
    __tablename__ = 'HoaDon'
    tongtien = Column(Float, default=0)
    hinhthucthanhtoan= Column(Enum(HinhThucThanhToan),nullable=False )
    ve_id = Column(Integer,ForeignKey('thongtinve.id'), nullable= False)





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




class User1(db.Model, UserMixin):
    __tablename__ = 'user1'

    id = Column(Integer, primary_key=True, autoincrement=True)
    _name = Column(String(50), nullable=False)
    _username = Column(String(50), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)







if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        taikhoan1 = User(username='phat', password=str(hashlib.md5("123".encode('utf-8')).hexdigest()),
                             role=RoleEnum.ADMIN)
        taikhoan2 = User(username='thua', password=str(hashlib.md5("123".encode('utf-8')).hexdigest()),
                             role=RoleEnum.ADMIN)
        taikhoan3 = User(username='chien', password=str(hashlib.md5("123".encode('utf-8')).hexdigest()),
                             role=RoleEnum.PASSENGER)
        taikhoan4 = User(username='thien', password=str(hashlib.md5("123".encode('utf-8')).hexdigest()),
                             role=RoleEnum.PASSENGER)
        taikhoan5 = User(username='phu', password=str(hashlib.md5("123".encode('utf-8')).hexdigest()),
                             role=RoleEnum.PASSENGER)
        db.session.add_all([taikhoan1,taikhoan2,taikhoan3,taikhoan4,taikhoan5])
        thongtintaikhoan1 = ThongTinTaiKhoan(name='Đặng Xuân Phát', diachi='Nhà Bè', cmnd='123', sdt='0123456789',
                                             email='phat@123.com',user_id=1)
        thongtintaikhoan2 = ThongTinTaiKhoan(name='Trần Huy Thừa', diachi='Quận 7', cmnd='456', sdt='0123456789',
                                             email='thua@123.com', user_id=2)
        thongtintaikhoan3 = ThongTinTaiKhoan(name='Lê Đình Chiến', diachi='Gò Vấp', cmnd='789', sdt='0123456789',
                                             email='chien@123.com', user_id=3)
        thongtintaikhoan4 = ThongTinTaiKhoan(name='Lê Chí Thiện', diachi='Tân Bình', cmnd='012', sdt='0123456789',
                                             email='thien@123.com', user_id=4)
        thongtintaikhoan5 = ThongTinTaiKhoan(name='Huy Phú', diachi='Nhà Bè', cmnd='345', sdt='0123456789',
                                             email='phu@123.com', user_id=5)
        db.session.add_all(
            [thongtintaikhoan1, thongtintaikhoan2, thongtintaikhoan3, thongtintaikhoan4, thongtintaikhoan5])
        sb1 = SanBay(name='Sân bay Tân Sơn Nhất', quocgia='Việt Nam')
        sb2 = SanBay(name='Sân bay Nội Bài', quocgia='Việt Nam')
        sb3 = SanBay(name='Sân bay Pháp', quocgia='Pháp')
        sb4 = SanBay(name='Sân bay Hongkong', quocgia='Trung Quốc')
        sb5 = SanBay(name='Sân bay Tokyo', quocgia='Nhật Bản')
        sb6 = SanBay(name='Sân bay Seul', quocgia='Hàn Quốc')
        sb7 = SanBay(name='Sân bay Los Angeles', quocgia='Mỹ')
        sb8 = SanBay(name='Sân bay BangKok', quocgia='Thái Lan')
        sb9 = SanBay(name='Sân bay Đà Nẵng', quocgia='Việt Nam')
        sb10 = SanBay(name='Sân bay Phú Quốc', quocgia='Kiên Giang')
        db.session.add_all([sb1, sb2, sb3, sb4, sb5, sb6,sb7,sb8,sb9,sb10])
        sbtg1 = SanBayTrungGian( ghichu='ádhasdhasjdas', tuyenbay_id=1, sanbay_id=9)
        sbtg2 = SanBayTrungGian( ghichu='ádhasdhasjdas', tuyenbay_id=2, sanbay_id=9)
        sbtg3 = SanBayTrungGian( ghichu='ádhasdhasjdas', tuyenbay_id=3, sanbay_id=6)
        sbtg4 = SanBayTrungGian( ghichu='ádhasdhasjdas', tuyenbay_id=1, sanbay_id=8)
        sbtg5 = SanBayTrungGian( ghichu='ádhasdhasjdas', tuyenbay_id=3, sanbay_id=4)

        db.session.add_all([sbtg1, sbtg2, sbtg3, sbtg4, sbtg5])
        mb1 = MayBay(name='Máy bay 1')
        mb2 = MayBay(name='Máy bay 2')
        mb3 = MayBay(name='Máy bay 3')
        mb4 = MayBay(name='Máy bay 4')
        mb5 = MayBay(name='Máy bay 5')
        mb6 = MayBay(name='Máy bay 6')
        db.session.add_all([mb1, mb2, mb3, mb4, mb5, mb6])

        tb1 = TuyenBay(name=sb1.name + sb6.name, diemdi=sb1.name, diemden=sb6.name, quangduong=100000, sanbay_id=1)
        tb2 = TuyenBay(name=sb1.name + sb2.name, diemdi=sb1.name, diemden=sb2.name, quangduong=90000, sanbay_id=1)
        tb3 = TuyenBay(name=sb1.name + sb7.name, diemdi=sb2.name, diemden=sb7.name, quangduong=300000, sanbay_id=2)
        tb4 = TuyenBay(name=sb1.name + sb10.name, diemdi=sb1.name, diemden=sb10.name, quangduong=50000, sanbay_id=1)
        db.session.add_all([tb1,tb2,tb3,tb4])

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

        gv1 = GiaVe(giave=2000000, hangghe_id=1, tuyenbay_id=1)
        gv2 = GiaVe(giave=3000000, hangghe_id=2, tuyenbay_id=1)
        gv3 = GiaVe(giave=500000, hangghe_id=1, tuyenbay_id=2)
        gv4 = GiaVe(giave=700000, hangghe_id=2, tuyenbay_id=2)
        gv5 = GiaVe(giave=1000000, hangghe_id=1, tuyenbay_id=3)
        gv6 = GiaVe(giave=1200000, hangghe_id=2, tuyenbay_id=3)
        gv7 = GiaVe(giave=4000000, hangghe_id=1, tuyenbay_id=4)
        gv8 = GiaVe(giave=5000000, hangghe_id=2, tuyenbay_id=4)
        db.session.add_all([gv1, gv2, gv3, gv4, gv5,gv6,gv7,gv8])

        ngay=datetime(2024,2,12,12,40,00)
        ngay1 = datetime(2024, 2, 2, 10, 00, 00)
        ngay2 = datetime(2024, 2, 22, 10, 00, 00)
        cb1 = ChuyenBay(tuyenbay_id=1, maybay_id=1, soluongghe1= 5, soluongghe2= 4,ngaybay=ngay, tinhtrang=True,
                        image="https://wallpapercave.com/wp/9aungfd.jpg", name='Không khứ hồi')
        cb2 = ChuyenBay(tuyenbay_id=2, maybay_id=2, soluongghe1=4, soluongghe2= 6,ngaybay=ngay, tinhtrang=True,
                        image="https://wallpapercave.com/wp/9aungfd.jpg", name='Không khứ hồi')
        cb3 = ChuyenBay(tuyenbay_id=3, maybay_id=3, soluongghe1=2, soluongghe2=2, ngaybay=ngay1, tinhtrang=True,
                        image="https://wallpapercave.com/wp/9aungfd.jpg", name='Không khứ hồi')
        cb4 = ChuyenBay(tuyenbay_id=4, maybay_id=4, soluongghe1=4, soluongghe2=4, ngaybay=ngay1, tinhtrang=True,
                        image="https://wallpapercave.com/wp/9aungfd.jpg", name='Không khứ hồi')
        cb5 = ChuyenBay(tuyenbay_id=1, maybay_id=5, soluongghe1=6, soluongghe2=6, ngaybay=ngay2, tinhtrang=True,
                        image="https://wallpapercave.com/wp/9aungfd.jpg", name='Không khứ hồi')
        cb6 = ChuyenBay(tuyenbay_id=2, maybay_id=6, soluongghe1=4, soluongghe2=4, ngaybay=ngay2, tinhtrang=True,
                        image="https://wallpapercave.com/wp/9aungfd.jpg", name='Không khứ hồi')
        cb7 = ChuyenBay(tuyenbay_id=3, maybay_id=1, soluongghe1=4, soluongghe2=4, ngaybay=ngay2, tinhtrang=True,
                        image="https://wallpapercave.com/wp/9aungfd.jpg", name='Không khứ hồi')
        cb8 = ChuyenBay(tuyenbay_id=4, maybay_id=4, soluongghe1=4, soluongghe2=4, ngaybay=ngay2, tinhtrang=True,
                        image="https://wallpapercave.com/wp/9aungfd.jpg", name='Không khứ hồi')
        db.session.add_all([cb1,cb2,cb3,cb4,cb5,cb6,cb7,cb8])

        ghe1cb1= SoLuongGhe(ghe_id=1, chuyenbay_id=1)
        ghe2cb1 = SoLuongGhe(ghe_id=2, chuyenbay_id=1)
        ghe3cb1 = SoLuongGhe(ghe_id=3, chuyenbay_id=1)
        ghe4cb1 = SoLuongGhe(ghe_id=4, chuyenbay_id=1)
        ghe5cb1 = SoLuongGhe(ghe_id=5, chuyenbay_id=1)
        ghe6cb1 = SoLuongGhe(ghe_id=11, chuyenbay_id=2)
        ghe7cb1 = SoLuongGhe(ghe_id=12, chuyenbay_id=2)
        ghe8cb1 = SoLuongGhe(ghe_id=13, chuyenbay_id=2)
        ghe9cb1 = SoLuongGhe(ghe_id=14, chuyenbay_id=2)
        db.session.add_all([ghe1cb1, ghe2cb1,ghe3cb1, ghe4cb1, ghe5cb1, ghe6cb1,ghe7cb1, ghe8cb1,ghe9cb1])

        ghe1cb2 = SoLuongGhe(ghe_id=1, chuyenbay_id=1)
        ghe2cb2 = SoLuongGhe(ghe_id=2, chuyenbay_id=1)
        ghe3cb2 = SoLuongGhe(ghe_id=3, chuyenbay_id=1)
        ghe4cb2 = SoLuongGhe(ghe_id=4, chuyenbay_id=1)
        ghe5cb2 = SoLuongGhe(ghe_id=11, chuyenbay_id=2)
        ghe6cb2 = SoLuongGhe(ghe_id=12, chuyenbay_id=2)
        ghe7cb2 = SoLuongGhe(ghe_id=13, chuyenbay_id=2)
        ghe8cb2 = SoLuongGhe(ghe_id=14, chuyenbay_id=2)
        db.session.add_all([ghe1cb2, ghe2cb2, ghe3cb2, ghe4cb2, ghe5cb2, ghe6cb2, ghe7cb2, ghe8cb2, ghe8cb2])

        # kh1 = TaiKhoanKH(name='Trần Huy Thừa', diachi='Tây Ninh', cmnd='072203003612',sdt='0368141334', email='huythua0@gmail.com')
        # kh2 = TaiKhoanKH(name='Trần Huy Thừa', diachi='Tây Ninh', cmnd='072203003612', sdt='0368141334',
        #                  email='huythua0@gmail.com')
        db.session.commit()
