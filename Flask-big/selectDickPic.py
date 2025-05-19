from create_BD import db, Users, Equipment, Rooms, Favorites, BookHistory, Occupancy, Revievs
from datetime import datetime, date
from sqlalchemy import func, case, and_, or_, not_

# 1. Проверка при регистрации
def check_user_exists(login):
    return db.session.query(Users.user_id).filter_by(user_login=login).first() is not None

# 2. Аутентификация пользователя
def authenticate(login, password):
    return Users.query.filter_by(user_login=login, user_pass=password).first()

# 3. Получение избранного оборудования
def get_user_favorites(user_id):
    return db.session.query(
        Equipment.object_id,
        Equipment.object_name,
        Equipment.object_photo
    ).join(Favorites).filter(Favorites.user_id == user_id).all()

# 4. История бронирования пользователя
def get_user_bookings(user_id):
    return db.session.query(
        Users.user_name,
        Users.user_surname,
        Equipment.object_name,
        Equipment.object_series,
        Equipment.object_photo,
        Rooms.room_name,
        BookHistory.data_book
    ).join(Users, BookHistory.user_id == Users.user_id
    ).join(Equipment, BookHistory.object_id == Equipment.object_id
    ).join(Rooms, BookHistory.room_id == Rooms.room_id
    ).filter(BookHistory.user_id == user_id
    ).order_by(BookHistory.data_book.desc()).all()

# 5. Проверка занятости
def check_availability(object_id, room_id, date, start_time, end_time):
    exists = db.session.query(Occupancy.key_id).filter(
        Occupancy.object_id == object_id,
        Occupancy.room_id == room_id,
        Occupancy.dataa == date,
        Occupancy.time_start <= end_time,
        Occupancy.time_end >= start_time
    ).first()
    return 'Занято' if exists else 'Свободно'

def get_scheduled_times(object_id, room_id, date):
    return db.session.query(
        Occupancy.time_start,
        Occupancy.time_end,
        Users.user_name,
        Users.user_surname
    ).join(Users).filter(
        Occupancy.object_id == object_id,
        Occupancy.room_id == room_id,
        Occupancy.dataa == date
    ).order_by(Occupancy.time_start).all()

def get_extended_availability(room_id, date, start_time, end_time):
    return db.session.query(
        Occupancy.time_start,
        Occupancy.time_end,
        Equipment.object_name,
        Rooms.room_name,
        func.concat(Users.user_name, ' ', Users.user_surname).label('booked_by')
    ).join(Equipment).join(Rooms).join(Users).filter(
        Occupancy.room_id == room_id,
        Occupancy.dataa == date,
        Occupancy.time_start <= end_time,
        Occupancy.time_end >= start_time
    ).order_by(Occupancy.time_start).all()

# 6. Получение отзывов
def get_equipment_reviews(object_id):
    return db.session.query(
        Equipment.object_name,
        Users.user_id,
        Users.user_name,
        Users.user_surname,
        Revievs.reviev_text
    ).join(Equipment).join(Users).filter(
        Revievs.object_id == object_id
    ).order_by(Revievs.riviev_id.desc()).all()

# 7. Дополнительные запросы
def get_user_role(user_id):
    return Users.query.with_entities(Users.user_role).filter_by(user_id=user_id).scalar()

def get_all_rooms():
    return Rooms.query.with_entities(
        Rooms.room_id,
        Rooms.room_name,
        Rooms.room_size
    ).order_by(Rooms.room_name).all()

def get_all_equipment():
    return Equipment.query.with_entities(
        Equipment.object_id,
        Equipment.object_name,
        Equipment.object_series
    ).order_by(Equipment.object_name).all()

def is_teacher(user_id):
    return Users.query.with_entities(
        case([(Users.user_role == 'B', True)], else_=False)
    ).filter_by(user_id=user_id).scalar()

def is_admin(user_id):
    return Users.query.with_entities(
        case([(Users.user_role == 'C', True)], else_=False)
    ).filter_by(user_id=user_id).scalar()

def get_available_rooms(date, start_time, end_time):
    occupied_rooms = db.session.query(Occupancy.room_id).filter(
        Occupancy.dataa == date,
        Occupancy.time_start <= end_time,
        Occupancy.time_end >= start_time
    ).subquery()
    
    return Rooms.query.filter(~Rooms.room_id.in_(occupied_rooms)).all()

def get_equipment_stats():
    return db.session.query(
        Equipment.object_name,
        func.count(BookHistory.object_id).label('booking_count'),
        func.count(Revievs.object_id).label('review_count')
    ).outerjoin(BookHistory, Equipment.object_id == BookHistory.object_id
    ).outerjoin(Revievs, Equipment.object_id == Revievs.object_id
    ).group_by(Equipment.object_name
    ).order_by(func.count(BookHistory.object_id).desc()).all()