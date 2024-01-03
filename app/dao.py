import json, os
from app.models import *
import hashlib
from flask_login import current_user


def load_chuyen_bay():
    return Flight.query.all()


def add_booking(flight):
    booking = Booking()
    booking.user = current_user
    booking.flight = flight
    db.session.add(booking)
    db.session.commit()

    return booking


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
    username = caesar_encrypt(username, SHIFT_CAESAR)

    return User.query.filter(User._username.__eq__(username),
                             User.password.__eq__(password)).first()