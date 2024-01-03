from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from app import dao, app, login_manager
from app.models import RoleEnum


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


@login_manager.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/')
def home():
    # load_data = dao.load_data()
    flights = dao.load_chuyen_bay()
    return render_template('index.html', data=flights)


@app.route('/book/<int:flight_id>')
@login_required
def book(flight_id):
    # load_data = dao.load_data()
    flights = dao.load_chuyen_bay()
    flight = next((f for f in flights if f.id == flight_id), None)
    if flight:
        return render_template('book.html', flight=flight, data=flights)
    else:
        return "Flight not found"


@app.route('/confirm', methods=['POST'])
@login_required
def confirm():
    flights = dao.load_chuyen_bay()
    flight_id = int(request.form.get('flight_id'))

    flight = next((f for f in flights if f.id == flight_id), None)
    if flight:
        booking = dao.add_booking(flight=flight)
        return render_template('confirm.html', booking=booking, data=flights)
    else:
        return "Flight not found"


@app.route("/books")
@login_required
def books():
    bookings = current_user.bookings
    return render_template('bookings.html', bookings=bookings)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = dao.auth_user(username, password)
        if user:
            login_user(user)
            #   flash('Login successful!', 'success')
            print(user.role)
            if user.role == RoleEnum.ADMIN:
                return redirect('/admin')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        password = form.password.data

        from sqlalchemy.exc import IntegrityError
        try:
            user = dao.register_user(name=name, username=username, password=password)
            login_user(user)
            return redirect(url_for('home'))
        except IntegrityError:
            flash('Username already exists.', 'danger')

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful!', 'success')
    return redirect(url_for('login'))


@login_manager.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))


if __name__ == '__main__':
    from app import admin

    app.run(debug=True)
