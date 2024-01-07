import json, os
from app.models import *
import hashlib
from flask_login import current_user
from sqlalchemy import func


def load_tuyenbay():
    return TuyenBay.query.all()

def load_chuyenbay():
    return ChuyenBay.query.all()

def count_chuyenbay():
    return ChuyenBay.query.count()
def load_giave():
    return GiaVe.query.all()
def load_hangghe():
    return HangGhe.query.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)
def register_user(name, username, password):
    user = User()
    user.name = name
    user.username = username
    user.password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user.role = RoleEnum.PASSENGER
    db.session.add(user)
    db.session.commit()
    return user



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