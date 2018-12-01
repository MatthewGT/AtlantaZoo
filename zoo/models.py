import os
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer,ForeignKeyConstraint
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# Use the werkzeug to generate password hash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'mysql+pymysql://root:@localhost:3306/test?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
bootstrap = Bootstrap(app)
moment = Moment(app)
# delete?
db = SQLAlchemy(app)

# UserMixin is a class has default implementations of
# is_authenticated(), is_active(), is_anonymous(), get_id() methods

class User(UserMixin, db.Model):
    """docstring for ClassName"""
    __tablename__ = 'user'
    def get_id(self):
        try:
            return self.Username
        except AttributeError:
            raise NotImplementedError('No `Username` attribute - override `get_id`')
    Username = db.Column(db.String(64), primary_key=True, nullable=False)
    Email = db.Column(db.String(64), unique=True, nullable=False)
    UserType = db.Column(db.String(64), nullable=False)
    Password_hash = db.Column(db.String(128))
    admin = db.relationship('Admin', backref='user_admin', lazy='dynamic')
    visitor = db.relationship('Visitor', backref='user_visitor', lazy='dynamic')
    staff = db.relationship('Staff', backref='user_staff', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.Password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.Password_hash, password)


class Admin(db.Model):
    """docstring for ClassName"""
    __tablename__ = 'admin'
    Username = db.Column(db.String(64), db.ForeignKey('user.Username'),primary_key=True,nullable=False)


class Visitor(db.Model):
    """docstring for ClassName"""
    __tablename__ = 'visitor'
    Username = db.Column(db.String(64),db.ForeignKey('user.Username'), primary_key=True,nullable=False)
    visitshow = db.relationship('VisitShow', backref='visitor_visitshow', lazy='dynamic')
    visitexhibit = db.relationship('VisitExhibit', backref='visitor_visitexhibit', lazy='dynamic')


class Staff(db.Model):
    """docstring for ClassName"""
    __tablename__ = 'staff'
    Username = db.Column(db.String(64),db.ForeignKey('user.Username'), primary_key=True,nullable=False)
    show = db.relationship('Show', backref='staff_show', lazy='dynamic')
    animalcare = db.relationship('AnimalCare', backref='staff_animalcare',lazy='dynamic')


class Animal(db.Model):
    """docstring for ClassName"""
    __tablename__ = 'animal'
    Name = db.Column(db.String(64),primary_key=True,nullable=False)
    Species = db.Column(db.String(64),primary_key=True,nullable=False)
    Type = db.Column(db.String(64),nullable=False)
    Age = db.Column(db.Integer,nullable=False)
    Exhibit = db.Column(db.String(64),db.ForeignKey('exhibit.Name'),nullable=False)
    # animalcare_animal = db.relationship('AnimalCare', backref='animal_animalcare',foreign_keys=["animalcare.Animal"], lazy='dynamic')
    # animalcare_species = db.relationship('AnimalCare', backref='animal_animalcare',foreign_keys=["animalcare.Species"], lazy='dynamic')


class Show(db.Model):
    """docstring for ClassName"""
    __tablename__ = 'show'
    Name = db.Column(db.String(64),primary_key=True,nullable=False)
    Datetime = db.Column(db.String(64),primary_key=True,nullable=False)
    Host = db.Column(db.String(64),db.ForeignKey('staff.Username'),nullable=False)
    Exhibit = db.Column(db.String(64),db.ForeignKey('exhibit.Name'),nullable=False)


class Exhibit(db.Model):
    """docstring for ClassName"""
    __tablename__ = 'exhibit'
    Name = db.Column(db.String(64),primary_key=True,nullable=False)
    WaterFeature = db.Column(db.String(64),nullable=False)
    Size = db.Column(db.Integer,nullable=False)
    animal = db.relationship('Animal', backref='exhibit_animal', lazy='dynamic')
    show = db.relationship('Show', backref='exhibit_show', lazy='dynamic')
    visitexhibit = db.relationship('VisitExhibit', backref='exhibit_visitexhibit', lazy='dynamic')


class AnimalCare(db.Model):
    """docstring for ClassName"""
    __tablename__ = 'animalcare'
    AnimalName = db.Column(db.String(64),nullable=False)
    SpeciesName = db.Column(db.String(64),nullable=False)
    StaffMember = db.Column(db.String(64), db.ForeignKey('staff.Username'),primary_key=True,nullable=False)
    Datetime = db.Column(db.String(64),primary_key=True,nullable=False)
    Text = db.Column(db.Text,nullable=False)
    animalcare_animal = db.relationship('Animal', backref='animalcare_animal',foreign_keys=[AnimalName], uselist=False)
    animalcare_species = db.relationship('Animal', backref='animalcare_species',foreign_keys=[SpeciesName], uselist=False)
    __table_args__  = (ForeignKeyConstraint([AnimalName, SpeciesName],[Animal.Name, Animal.Species]),{})


class VisitShow(db.Model):
    """docstring for ClassName"""
    __tablename__ = 'visitshow'
    ShowName = db.Column(db.String(64),nullable=False)
    Datetime = db.Column(db.String(64),nullable=False)
    Visitor = db.Column(db.String(64),db.ForeignKey('visitor.Username'),primary_key=True,nullable=False)
    visitshow_showname = db.relationship('Show', backref='visitshow_showname', foreign_keys=[ShowName], uselist=False)
    visitshow_datetime = db.relationship('Show', backref='visitshow_datetime', foreign_keys=[Datetime], uselist=False)
    __table_args__  = (ForeignKeyConstraint([ShowName, Datetime],[Show.Name, Show.Datetime]),{})


class VisitExhibit(db.Model):
    """docstring for ClassName"""
    __tablename__ = 'visitexhibit'
    Exhibit = db.Column(db.String(64),db.ForeignKey('exhibit.Name'),primary_key=True,nullable=False, unique=True)
    Visitor = db.Column(db.String(64),db.ForeignKey('visitor.Username'),primary_key=True,nullable=False, unique=True)
    Datetime = db.Column(db.String(64),primary_key=True,nullable=False, unique=True)


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

