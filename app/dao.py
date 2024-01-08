import json, os
from app.models import *
import hashlib
from flask_login import current_user
from sqlalchemy import func
import  cloudinary.uploader

def load_tuyenbay():
    return TuyenBay.query.all()

def load_chuyenbay():
    return ChuyenBay.query.all()
def load_thongtintaikhoan():
    return ThongTinTaiKhoan.query.all()
def count_chuyenbay():
    return ChuyenBay.query.count()
def load_giave():
    return GiaVe.query.all()
def load_hangghe():
    return HangGhe.query.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)
def add_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User( username=username, password=password)
    db.session.add(u)
    db.session.commit()
def add_thongtin(user_id,name,diachi,sdt,mail,cmnd):
    info = ThongTinTaiKhoan(user_id=user_id,name=name, diachi=diachi, sdt=sdt, email=mail, cmnd=cmnd)
    db.session.add(info)
    db.session.commit()
def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()
def thongketheothang(thang):
    query= (db.session.query(
            ThongTinVe.tuyenbay_id,
            func.sum(ThongTinVe.giave).label('doanhthu')).filter(func.strftime('%Y-%m', ThongTinVe.ngaydat) == thang)
            .group_by(ThongTinVe.tuyenbay_id)
            .all()
            )
