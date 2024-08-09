from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DecimalField,IntegerField
from wtforms.validators import DataRequired,Length,Email,EqualTo,NumberRange,Optional


class RegistrationForm(FlaskForm):
    name= StringField('Name',validators=[DataRequired(),Length(min=2 , max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    phone_no=StringField('Phone_no',validators=[DataRequired(),Length(min=10 , max=10)])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8 , max=20 )])
    password_conform=PasswordField('Password_conform',validators=[DataRequired(),Length(min=8 , max=20 ),EqualTo('password')])
    submit=SubmitField('Sign up')

class loginform(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8 , max=20)])
    submit=SubmitField('LOGIN')

class adminloginform(FlaskForm):
    name=StringField('Name',validators=[DataRequired()]) 
    email=StringField('Email',validators=[DataRequired(),Email()]) 
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8 , max=20)])
    submit=SubmitField('LOGIN AS ADMIN')  
class insertproduct(FlaskForm):
    name=StringField('ProductName',validators=[DataRequired()]) 
    price=DecimalField('PRICE',validators=[DataRequired()]) 
    description=StringField('Description',validators=[DataRequired()])
    photo=StringField('PHOTO LINK',validators=[DataRequired()])
    quantity=IntegerField('Quantity',validators=[DataRequired()])
    submit=SubmitField('ADD PRODUCT')
class searchform(FlaskForm):
    var=StringField('')
    submit=SubmitField('SEARCH')
class deleteproduct(FlaskForm):
    description=StringField('Description',validators=[DataRequired()])
    column=StringField('Item name',validators=[DataRequired()])
    quan=IntegerField('Quantity',validators=[DataRequired()])
    submit=SubmitField('DELETE')
class reviewsform(FlaskForm):
    review=StringField('Enter your review')
    rating=IntegerField('Rating',  validators=[Optional(),NumberRange(min=0 , max=5)])
    submit=SubmitField('SUMBIT')
class selectionform(FlaskForm) :
    table=StringField('Table Name',validators=[DataRequired()]) 
    submit=SubmitField ("Display") 
class quantityform(FlaskForm) :
    quant=IntegerField('Quantity')  
    submit=SubmitField ("Submit Quantity") 


        
    
          

    

