from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from flask_login import current_user, logout_user
from flask import redirect
from app import app, db, admin
from app.caesar_cipher import caesar_decrypt
from app.models import User, Booking, RoleEnum, TuyenBay


admin = Admin(app=app, name='HỆ THỐNG ĐẶT VÉ MÁY BAY', template_mode='bootstrap4')


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == RoleEnum.ADMIN


class UserView(AuthenticatedAdmin):
    column_display_pk = True

    can_view_details = False
    edit_modal = False
    can_create = False
    can_edit = False

    column_list = ('id', 'name', 'username', 'password', 'role')
class TuyenBayView(AuthenticatedAdmin):
    column_list = ('id','name', 'diemden','diemdi','quangduong','chuyenbay')
    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    can_create = True
class BookingView(AuthenticatedAdmin):
    column_list = ('id', 'flight', 'user_id', 'user', 'time')

    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    can_create = True


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(UserView(User, db.session))
admin.add_view(BookingView(Booking, db.session))
admin.add_view(TuyenBayView(TuyenBay, db.session))
admin.add_view(LogoutView(name="Đăng xuất"))
