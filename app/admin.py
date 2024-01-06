from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from flask_login import current_user, logout_user
from flask import redirect
from app import app, db, Admin
from app.models import  RoleEnum, TuyenBay, User, SanBay, SanBayTrungGian


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
    column_list = ('id','name', 'diemdi','diemden','sanbay_id','quangduong','giave', 'sanbaytrunggians')
    can_export = True
    column_searchable_list = ['name']
    column_filters = ['giave', 'name']
    column_editable_list = [ 'giave']
    details_modal = True
    edit_modal = True
    form_create_rules = [
        'name',
        'diemdi',
        'diemden',
        'sanbay',
        'quangduong',
        'sanbaytrunggians',
        'giave'
    ]

    # Tùy chỉnh trường chuyenbay để không hiển thị trong mẫu tạo mới
    form_excluded_columns = ['chuyenbay']
class SanBayTrungGianView(AuthenticatedAdmin):
    column_list = ('tuyenbay_id','sanbay_id', 'ghichu','time','')
    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    can_create = True

class SanBayView(AuthenticatedAdmin):
    column_list = ('id','name', 'quocgia')
    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    can_create = True


class BookingView(AuthenticatedAdmin):
    column_list = ('id', 'flight', 'user_id')

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
admin.add_view(TuyenBayView(TuyenBay, db.session))
admin.add_view(SanBayTrungGianView(SanBayTrungGian, db.session))
admin.add_view(SanBayView(SanBay, db.session))
admin.add_view(LogoutView(name="Đăng xuất"))
