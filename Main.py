from flask import Flask, session, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, EqualTo
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = "eocfgdgdgdfifhje9oshf9wos£hfsokj££eh-8902ufbnu3h7wu9houfbj££ef33knb834££8sdhfhosfsfep"

class Forms_users(db.Model):
    __tablename__= 'Forms_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index = True)
    email = db.Column(db.String(64), unique=True, index = True, nullable=False)
    password = db.Column(db.String(64), index = True, nullable=False)

class RegisterForm(FlaskForm):
    email = StringField("enter Email:",validators=[DataRequired()])
    username = StringField("enter username:",validators=[DataRequired()])
    password = PasswordField("enter password:",validators=[DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField("Confirm Password:",validators=[DataRequired(), EqualTo('confirm_password')])
    submit = SubmitField("submit")

class Answer(FlaskForm):
    answer = StringField("Answer:")

with app.app_context():
    db.create_all()

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/sign_up', methods = ['GET','POST'])
def sign_up_page():
    form = RegisterForm()
    if form.validate_on_submit():
        userEmail = Forms_users.query.filter_by(email=form.email.data).first()
        userName = Forms_users.query.filter_by(username=form.username.data).first()
        if userName is None and userEmail is None:
            user = Forms_users(username=form.username.data, email = form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
            flash("You aready have an account!")
        session['name'] = form.username.data
        form.username.data = ''
        return redirect("/")
    return render_template('sign_up_page.html', form=form, name=session.get('name'),known=session.get('known',False))

@app.route('/sign_in', methods = ['GET','POST'])
def sign_In_page():
    return render_template('sign_in_page.html')

@app.route('/profile', methods = ['GET','Post'])
def Profile_page():
    return render_template('Profile_page.html')

if __name__ == '__main__':
    app.run(debug=True)