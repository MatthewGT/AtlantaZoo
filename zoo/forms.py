from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, \
BooleanField,IntegerField, DateTimeField, TextAreaField, DateField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from dbQuery import Database
from models import User, Admin, Visitor, Staff, Animal, Show, Exhibit, AnimalCare, \
VisitShow, VisitExhibit

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class ExhibitForm(FlaskForm):
    exhibit_name = StringField('Name:', validators=[])
    min_animals = IntegerField('Minimum number of animals:', validators=[],default=0)
    max_animals = IntegerField('Maximum number of animals:', validators=[],default=100)
    min_size = IntegerField('Minimum Size:', validators=[],default=0)
    max_size = IntegerField('Maximum Size:', validators=[],default=1400)
    water_feature = SelectField(u'water feature', choices=[('', ''),('yes', 'yes'), ('no', 'no')])

class VisitorForm(FlaskForm):
    username = StringField('Name:', validators=[])
    email = StringField('Email:', validators=[])



class ExhibitHistoryForm(FlaskForm):
    exhibit_name = StringField('Name:', validators=[])
    min_visits = IntegerField('min_visits:', validators=[],default=0)
    max_visits = IntegerField('max_visits:', validators=[],default=10000)
    visit_time = StringField('visit_time', validators=[])

class ShowHistoryForm(FlaskForm):
    show_name = StringField('Name of the Show:', validators=[])
    exhibit_name = StringField('Name of the Exhibit:', validators=[])
    date = StringField('Date:', validators=[])


class SearchShowForm(FlaskForm):
    show_name = StringField('Name of the Show:', validators=[])
    exhibit_name = StringField('Name of the Exhibit:', validators=[])
    date = StringField('Date:', validators=[])

class AdminShowForm(FlaskForm):
    show_name = StringField('Name of the Show:', validators=[Required()])
    exhibit_name = StringField('Exhibit Name:', validators=[Required()])
    staff = StringField('Host Staff:', validators=[Required()])
    date = StringField('Date:', validators=[Required()])
    time = StringField('Time:', validators=[Required()])

class AnimalCareForm(FlaskForm):
    care_text = TextAreaField('Notes:')

class SearchAnimalForm(FlaskForm):
    animal_name = StringField('Animal Name:', validators=[])
    exhibit_name = StringField('Exhibit Name:', validators=[])
    species = StringField('Species:', validators=[])
    min_age = StringField('Min Age:', validators=[],default= 0)
    max_age = StringField('Max Age:', validators=[],default= 10000)
    animal_type = StringField('Type:', validators=[])

class AdminAnimalForm(FlaskForm):
    animal_name = StringField('Animal Name:', validators=[Required()])
    exhibit_name = StringField('Exhibit Name:', validators=[Required()])
    animal_type = StringField('Type:', validators=[Required()])
    species = StringField("Species: ", validators=[Required()])
    age = StringField("Age: ", validators=[Required()])

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                           Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        Length(min=6,max=12,message='at least 8 characters'), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    usertype = SelectField(u'User Type', choices=[('visitor', 'visitor'), ('staff', 'staff')])
    submit = SubmitField('Register')
    
    def validate_email(self, field):
        # if User.query.filter_by(Email=field.data).first():
        if len(Database().get_user(field.data)) != 0:
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        # if User.query.filter_by(Username=field.data).first():
        if len(Database().get_user_username(field.data)) != 0:
            raise ValidationError('Username already in use.')

