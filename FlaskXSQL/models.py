from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Rooms(db.Model):
    __tablename__ = 'rooms'
    room_id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(255), nullable=False)
    room_size = db.Column(db.String(255), nullable=False)
    
    occupancies = db.relationship('Occupancy', backref='room', cascade='all, delete-orphan')
    book_history = db.relationship('BookHistory', backref='room', cascade='all, delete-orphan')

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(255), nullable=False, unique=True)
    user_pass = db.Column(db.String(255), nullable=False)
    user_name = db.Column(db.String(255), nullable=False)
    user_surname = db.Column(db.String(255), nullable=False)
    user_role = db.Column(db.String(5), nullable=False)
    
    reviews = db.relationship('Revievs', backref='user', cascade='all, delete-orphan')
    favorites = db.relationship('Favorites', backref='user', cascade='all, delete-orphan')
    occupancies = db.relationship('Occupancy', backref='user', cascade='all, delete-orphan')
    book_history = db.relationship('BookHistory', backref='user', cascade='all, delete-orphan')

class Equipment(db.Model):
    __tablename__ = 'equipment'
    object_id = db.Column(db.Integer, primary_key=True)
    object_name = db.Column(db.String(255), nullable=False)
    object_series = db.Column(db.String(255), nullable=False)
    obkect_gabaritType = db.Column(db.String(255), nullable=False)
    object_description = db.Column(db.Text)
    object_photo = db.Column(db.Text)
    
    reviews = db.relationship('Revievs', backref='equipment', cascade='all, delete-orphan')
    favorites = db.relationship('Favorites', backref='equipment', cascade='all, delete-orphan')
    occupancies = db.relationship('Occupancy', backref='equipment', cascade='all, delete-orphan')
    book_history = db.relationship('BookHistory', backref='equipment', cascade='all, delete-orphan')

class Revievs(db.Model):
    __tablename__ = 'revievs'
    riviev_id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey('equipment.object_id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    reviev_text = db.Column(db.Text)
    
    __table_args__ = (
        db.UniqueConstraint('object_id', 'user_id', name='_object_user_uc'),
    )

class BookHistory(db.Model):
    __tablename__ = 'book_history'
    boking_id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey('equipment.object_id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.room_id', ondelete='CASCADE'), nullable=False)
    data_book = db.Column(db.Date, nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('object_id', 'user_id', 'room_id', 'data_book', name='_booking_uc'),
    )

class Occupancy(db.Model):
    __tablename__ = 'occupancy'
    key_id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey('equipment.object_id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.room_id', ondelete='CASCADE'), nullable=False)
    dataa = db.Column(db.Date, nullable=False)
    time_start = db.Column(db.DateTime, nullable=False)
    time_end = db.Column(db.DateTime, nullable=False)
    
    __table_args__ = (
        db.CheckConstraint('time_end > time_start', name='valid_time_range'),
        db.UniqueConstraint('object_id', 'user_id', 'room_id', 'time_start', 'time_end', name='_occupancy_uc'),
    )

class Favorites(db.Model):
    __tablename__ = 'favorites'
    object_id = db.Column(db.Integer, db.ForeignKey('equipment.object_id', ondelete='CASCADE'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    
    __table_args__ = (
        db.UniqueConstraint('object_id', 'user_id', name='_favorite_uc'),
    )