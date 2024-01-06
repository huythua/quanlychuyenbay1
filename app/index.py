from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import UserMixin, login_user, login_required, logout_user, current_user



from app import dao, app, login_manager
from app.models import RoleEnum
import math

# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Login')
#
#
# class RegistrationForm(FlaskForm):
#     name = StringField('Name', validators=[DataRequired()])
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Register')
#
#
# @login_manager.user_loader
# def load_user(user_id):
#     return dao.get_user_by_id(user_id)


@app.route('/')
def index():
    tuyenbay = dao.load_tuyenbay()
    chuyenbay= dao.load_chuyenbay()
    num= dao.count_chuyenbay()
    giave = dao.load_giave()
    hangghe = dao.load_hangghe()
    return render_template('index.html',tuyenbay=tuyenbay, chuyenbay=chuyenbay, giave=giave,
                           hangghe=hangghe,
                           pages=math.ceil(num/app.config['PAGE_SIZE']))


# @app.route('/book/<int:flight_id>')
# @login_required
# def book(flight_id):
#     # load_data = dao.load_data()
#     flights = dao.load_chuyen_bay()
#     flight = next((f for f in flights if f.id == flight_id), None)
#     if flight:
#         return render_template('book.html', flight=flight, data=flights)
#     else:
#         return "Flight not found"
#
#
# @app.route('/confirm', methods=['POST'])
# @login_required
# def confirm():
#     flights = dao.load_chuyen_bay()
#     flight_id = int(request.form.get('flight_id'))
#
#     flight = next((f for f in flights if f.id == flight_id), None)
#     if flight:
#         booking = dao.add_booking(flight=flight)
#         return render_template('confirm.html', booking=booking, data=flights)
#     else:
#         return "Flight not found"
#
#
# @app.route("/books")
# @login_required
# def books():
#     bookings = current_user.bookings
#     return render_template('bookings.html', bookings=bookings)
#
#
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

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         username = form.username.data
#         password = form.password.data
#
#         from sqlalchemy.exc import IntegrityError
#         try:
#             user = dao.register_user(name=name, username=username, password=password)
#             login_user(user)
#             return redirect(url_for('home'))
#         except IntegrityError:
#             flash('Username already exists.', 'danger')
#
#     return render_template('register.html', form=form)
#

@app.route('/logout')
def process_user_logout():
    logout_user()
    return redirect("/")




@login_manager.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)
#
#
# @login_manager.unauthorized_handler
# def unauthorized_handler():
#     return redirect(url_for('login'))


if __name__ == '__main__':
    from app import admin

    app.run(debug=True)
