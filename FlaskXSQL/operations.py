from models import db, Users, Equipment, Rooms, Favorites, BookHistory, Occupancy, Revievs
from datetime import datetime, date

# Создание таблиц
def create_tables():
    db.create_all()

# Удаление таблиц
def drop_tables():
    db.drop_all()

# === Users operations ===
def create_user(login, password, name, surname, role):
    user = Users(
        user_login=login,
        user_pass=password,
        user_name=name,
        user_surname=surname,
        user_role=role
    )
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_id(user_id):
    return Users.query.get(user_id)

def get_user_by_login(login):
    return Users.query.filter_by(user_login=login).first()

def authenticate_user(login, password):
    return Users.query.filter_by(user_login=login, user_pass=password).first()

def delete_user(user_id):
    user = Users.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False

# === Equipment operations ===
def create_equipment(name, series, gabarit_type, description=None, photo=None):
    equipment = Equipment(
        object_name=name,
        object_series=series,
        obkect_gabaritType=gabarit_type,
        object_description=description,
        object_photo=photo
    )
    db.session.add(equipment)
    db.session.commit()
    return equipment

def get_all_equipment():
    return Equipment.query.order_by(Equipment.object_name).all()

def delete_equipment(equipment_id):
    equipment = Equipment.query.get(equipment_id)
    if equipment:
        db.session.delete(equipment)
        db.session.commit()
        return True
    return False

# Для фильтрации оборудования
def get_equipment_by_category(category):
    return Equipment.query.filter(
        Equipment.object_name.ilike(f'%{category}%')
    ).all()

# === Rooms operations ===
def create_room(name, size):
    room = Rooms(
        room_name=name,
        room_size=size
    )
    db.session.add(room)
    db.session.commit()
    return room

def get_all_rooms():
    return Rooms.query.order_by(Rooms.room_name).all()

def delete_room(room_id):
    room = Rooms.query.get(room_id)
    if room:
        db.session.delete(room)
        db.session.commit()
        return True
    return False

# === Favorites operations ===
def add_to_favorites(user_id, equipment_id):
    favorite = Favorites(
        user_id=user_id,
        object_id=equipment_id
    )
    db.session.add(favorite)
    db.session.commit()
    return favorite

def get_user_favorites(user_id):
    return Equipment.query.join(Favorites).filter(Favorites.user_id == user_id).all()

def remove_from_favorites(user_id, equipment_id):
    favorite = Favorites.query.filter_by(user_id=user_id, object_id=equipment_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return True
    return False

# === Booking operations ===
def create_booking(equipment_id, user_id, room_id, booking_date):
    booking = BookHistory(
        object_id=equipment_id,
        user_id=user_id,
        room_id=room_id,
        data_book=booking_date
    )
    db.session.add(booking)
    db.session.commit()
    return booking

def get_user_bookings(user_id):
    return BookHistory.query.filter_by(user_id=user_id).order_by(BookHistory.data_book.desc()).all()

# === Occupancy operations ===
def create_occupancy(equipment_id, user_id, room_id, date, start_time, end_time):
    occupancy = Occupancy(
        object_id=equipment_id,
        user_id=user_id,
        room_id=room_id,
        dataa=date,
        time_start=start_time,
        time_end=end_time
    )
    db.session.add(occupancy)
    db.session.commit()
    return occupancy

def check_availability(equipment_id, room_id, date, start_time, end_time):
    existing = Occupancy.query.filter(
        Occupancy.object_id == equipment_id,
        Occupancy.room_id == room_id,
        Occupancy.dataa == date,
        Occupancy.time_start <= end_time,
        Occupancy.time_end >= start_time
    ).first()
    return existing is None

def get_room_schedule(room_id, date):
    return Occupancy.query.filter_by(room_id=room_id, dataa=date).order_by(Occupancy.time_start).all()

# === Reviews operations ===
def create_review(equipment_id, user_id, text):
    review = Revievs(
        object_id=equipment_id,
        user_id=user_id,
        reviev_text=text
    )
    db.session.add(review)
    db.session.commit()
    return review

def get_equipment_reviews(equipment_id):
    return Revievs.query.filter_by(object_id=equipment_id).order_by(Revievs.riviev_id.desc()).all()

# === Utility functions ===
def is_teacher(user_id):
    user = Users.query.get(user_id)
    return user and user.user_role == 'Преподаватель'

def is_admin(user_id):
    user = Users.query.get(user_id)
    return user and user.user_role == 'Администратор'


def get_available_rooms(date, start_time, end_time):
    from sqlalchemy import select
    occupied_rooms = select(Occupancy.room_id).where(
        Occupancy.dataa == date,
        Occupancy.time_start <= end_time,
        Occupancy.time_end >= start_time
    )
    return Rooms.query.filter(~Rooms.room_id.in_(occupied_rooms)).all()

def get_equipment_stats():
    from sqlalchemy import func
    return db.session.query(
        Equipment.object_name,
        func.count(BookHistory.object_id).label('booking_count'),
        func.count(Revievs.object_id).label('review_count')
    ).outerjoin(BookHistory, Equipment.object_id == BookHistory.object_id
    ).outerjoin(Revievs, Equipment.object_id == Revievs.object_id
    ).group_by(Equipment.object_name
    ).order_by(func.count(BookHistory.object_id).desc()).all()