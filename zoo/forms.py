from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, \
BooleanField,IntegerField, DateTimeField, TextAreaField, DateField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from models import User, Admin, Visitor, Staff, Animal, Show, Exhibit, AnimalCare, \
VisitShow, VisitExhibit

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class ExhibitForm(FlaskForm):
    exhibit_name = StringField('Name:', validators=[],default='Pacific')
    min_animals = IntegerField('Minimum number of animals:', validators=[],default=0)
    max_animals = IntegerField('Maximum number of animals:', validators=[],default=100)
    min_size = IntegerField('Minimum Size:', validators=[],default=0)
    max_size = IntegerField('Maximum Size:', validators=[],default=1400)
    water_feature = BooleanField('Water Feature?')

class SearchAnimalForm(FlaskForm):
    animal_name = StringField('Animal Name:', validators=[])
    species = StringField('Species:', validators=[])
    min_age = StringField('Min Age:', validators=[])
    max_age = StringField('Max Age:', validators=[])
    animal_type = StringField('Type:', validators=[])

class ExhibitHistoryForm(FlaskForm):
    exhibit_name = StringField('Name:', validators=[],default='Pacific')
    min_visits = IntegerField('min_visits:', validators=[],default=0)
    max_visits = IntegerField('max_visits:', validators=[],default=0)
    visit_time = DateTimeField('visit_time', validators=[])

class SearchShowForm(FlaskForm):
    show_name = StringField('Name of the Show:', validators=[],default='Feed the fish')
    exhibit_name = StringField('Name:', validators=[],default='Pacific')
    date = DateTimeField('Date:', validators=[])

class ShowForm(FlaskForm):
    show_name = StringField('Name of the Show:', validators=[],default='Feed the fish')
    exhibit_name = StringField('Name:', validators=[],default='Pacific')
    staff = StringField('Staff:', validators=[],default='Ellen')
    date = DateField('Date:', validators=[])
    time = DateTimeField('Time:', validators=[])

class AnimalCareForm(FlaskForm):
    care_text = TextAreaField('Notes:')

class AnimalForm(FlaskForm):
    animal_name = StringField('Name:', validators=[],default='Jim')
    exhibit_name = StringField('Name:', validators=[],default='Pacific')
    animal_type = StringField('Type:', validators=[])
    species = StringField("Species: ", validators=[])
    age = StringField("Age: ", validators=[])

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
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    usertype = SelectField(u'User Type', choices=[('visitor', 'visitor'), ('staff', 'staff')])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(Email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(Username=field.data).first():
            raise ValidationError('Username already in use.')

