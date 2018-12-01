from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, \
BooleanField,IntegerField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from models import User, Admin, Visitor, Staff, Animal, Show, Exhibit, AnimalCare, \
VisitShow, VisitExhibit

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class ExhibitForm(FlaskForm):
    exhibit_name = StringField('Name:', validators=[],default='Pacific')
    min_animals = IntegerField('min_animals:', validators=[],default=0)
    max_animals = IntegerField('max_animals:', validators=[],default=100)
    min_size = IntegerField('min_size:', validators=[],default=0)
    max_size = IntegerField('max_size:', validators=[],default=1400)

    # min_animals = SelectField(u'Min Number of Animals', choices=[('0','100','600')])
    # max_animals = SelectField(u'Max Number of Animals', choices=[('10')])
    # min_size = SelectField(u'Min Number of Size', choices=[('min_low','2'), ('min_up', '8')])
    # max_size = SelectField(u'Max Number of Size', choices=[('20')])
    water_feature = BooleanField('Water Feature?')



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


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[Required()])
    password = PasswordField('New password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[Required()])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('New Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')

class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
