from create_BD import db, Users, Equipment, Rooms, Favorites, BookHistory, Occupancy, Revievs
from datetime import date

# Удаление пользователей
def delete_user_by_id(user_id):
    Users.query.filter_by(user_id=user_id).delete()
    db.session.commit()

def delete_user_by_login(login):
    Users.query.filter_by(user_login=login).delete()
    db.session.commit()

def delete_users_by_role(role):
    Users.query.filter_by(user_role=role).delete()
    db.session.commit()

# Удаление оборудования
def delete_equipment_by_id(object_id):
    Equipment.query.filter_by(object_id=object_id).delete()
    db.session.commit()

def delete_equipment_by_name(name):
    Equipment.query.filter_by(object_name=name).delete()
    db.session.commit()

def delete_equipment_by_series(series):
    Equipment.query.filter_by(object_series=series).delete()
    db.session.commit()

# Удаление аудиторий
def delete_room_by_id(room_id):
    Rooms.query.filter_by(room_id=room_id).delete()
    db.session.commit()

def delete_room_by_name(room_name):
    Rooms.query.filter_by(room_name=room_name).delete()
    db.session.commit()

def delete_rooms_by_size(size):
    Rooms.query.filter(Rooms.room_size.like(f'%{size}%')).delete()
    db.session.commit()

# Удаление из избранного
def delete_favorite(user_id, object_id):
    Favorites.query.filter_by(user_id=user_id, object_id=object_id).delete()
    db.session.commit()

def delete_all_user_favorites(user_id):
    Favorites.query.filter_by(user_id=user_id).delete()
    db.session.commit()

def delete_all_equipment_favorites(object_id):
    Favorites.query.filter_by(object_id=object_id).delete()
    db.session.commit()

# Удаление истории бронирования
def delete_booking_by_id(booking_id):
    BookHistory.query.filter_by(boking_id=booking_id).delete()
    db.session.commit()

def delete_bookings_by_equipment(object_id):
    BookHistory.query.filter_by(object_id=object_id).delete()
    db.session.commit()

def delete_old_bookings(cutoff_date):
    BookHistory.query.filter(BookHistory.data_book < cutoff_date).delete()
    db.session.commit()

# Удаление занятости
def delete_occupancy_by_id(key_id):
    Occupancy.query.filter_by(key_id=key_id).delete()
    db.session.commit()

def delete_occupancy_by_room(room_id):
    Occupancy.query.filter_by(room_id=room_id).delete()
    db.session.commit()

def delete_past_occupancies():
    Occupancy.query.filter(Occupancy.dataa < date.today()).delete()
    db.session.commit()

# Удаление отзывов
def delete_review_by_id(review_id):
    Revievs.query.filter_by(riviev_id=review_id).delete()
    db.session.commit()

def delete_user_reviews(user_id):
    Revievs.query.filter_by(user_id=user_id).delete()
    db.session.commit()

def delete_equipment_reviews(object_id):
    Revievs.query.filter_by(object_id=object_id).delete()
    db.session.commit()