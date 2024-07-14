from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,Email,EqualTo


class RegistrationForm(FlaskForm):
    name= StringField('Name',validators=[DataRequired(),Length(min=2 , max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    phone_no=StringField('Phone_no',validators=[DataRequired(),Length(min=10 , max=10)])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8 , max=20 )])
    password_conform=PasswordField('Password_conform',validators=[DataRequired(),Length(min=8 , max=20 ),EqualTo('password')])
    submit=SubmitField('Sign up')

class loginform(FlaskForm):
    email=StringField('Name',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8 , max=20)])
    submit=SubmitField('LOGIN')

class adminloginform(FlaskForm):
    username=StringField('Name',validators=[DataRequired()]) 
    email=StringField('emaill',validators=[DataRequired(),Email()]) 
    password=PasswordField('pass',validators=[DataRequired(),Length(min=8 , max=20)])  

    

