from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import Required

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class ExhibitForm(FlaskForm):
    name = StringField('Name:', validators=[Required()])
    min_animals = SelectField(u'Min Number of Animals', choices=[('4','6')])
    max_animals = SelectField(u'Max Number of Animals', choices=[('10')])
    min_size = SelectField(u'Min Number of Size', choices=[('min_low','2'), ('min_up', '8')])
    max_size = SelectField(u'Max Number of Size', choices=[('20')])
    language = SelectField(u'Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    water_feature = BooleanField('Water Feature?')