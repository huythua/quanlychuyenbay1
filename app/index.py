from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from app import dao, app, login_manager,db
from app.models import RoleEnum
import math
from app.models import ThongTinTaiKhoan, User
@app.route('/')
def index():
    print(dao.thongketheothang(2))
    tuyenbay = dao.load_tuyenbay()
    chuyenbay= dao.load_chuyenbay()
    num= dao.count_chuyenbay()
    giave = dao.load_giave()
    hangghe = dao.load_hangghe()
    return render_template('index.html',tuyenbay=tuyenbay, chuyenbay=chuyenbay, giave=giave,
                           hangghe=hangghe,
                           pages=math.ceil(num/app.config['PAGE_SIZE']))

@app.route("/login", methods=['get', 'post'])
def process_user_login():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            next = request.args.get('next')
            return redirect('/' if next is None else next)
    return render_template('login.html')
@app.route('/admin/login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)
    return redirect('/admin')
@app.route('/register', methods=['get', 'post'])
def register_user():
    err_msg = None

    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            try:
                dao.add_user(
                             username=request.form.get('username'),
                             password=password)

            except Exception as ex:
                print(str(ex))
                err_msg = 'Hệ thống đang bị lỗi!'
            else:
                return redirect('/login')
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('/register.html', err_msg=err_msg)
@app.route('/thongtin', methods=['get', 'post'])
def add_thongtin():
    if request.method == 'POST':
        user_id = current_user.id
        name = request.form['name']
        diachi = request.form['diachi']
        cmnd = request.form['cmnd']
        sdt = request.form['sdt']
        email = request.form['mail']

        # Kiểm tra xem user_id đã có trong bảng thongtintaikhoan hay chưa
        existing_thongtin = ThongTinTaiKhoan.query.filter_by(user_id=user_id).first()

        if existing_thongtin:
            # Nếu tồn tại, thực hiện cập nhật thông tin
            existing_thongtin.name = name
            existing_thongtin.diachi = diachi
            existing_thongtin.cmnd = cmnd
            existing_thongtin.sdt = sdt
            existing_thongtin.email = email
        else:
            user_id = current_user.id
            new_user_info = ThongTinTaiKhoan(name=name, diachi=diachi, cmnd=cmnd, sdt=sdt, email=email, user_id=user_id)
            db.session.add(new_user_info)
        db.session.commit()
        return redirect('/')
    return render_template('thongtin.html')
@app.route('/logout')
def process_user_logout():
    logout_user()
    return redirect("/")
@login_manager.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)
@app.context_processor
def common_response():
    return {
        'chuyenbay': dao.load_chuyenbay(),
        'tuyenbay':dao.load_tuyenbay()
    }
if __name__ == '__main__':
    from app import admin

    app.run(debug=True)
