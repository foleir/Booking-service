from models import db, Users, Equipment, Rooms, Favorites, BookHistory, Occupancy, Revievs
from datetime import datetime, date
from security import hash_password, verify_password

# Создание таблиц
def create_tables():
    db.create_all()

# Удаление таблиц
def drop_tables():
    db.drop_all()

# === Users operations ===
def create_user(login, password, name, surname, role):
    hashed_password = hash_password(password)  # Используем новую функцию
    user = Users(
        user_login=login,
        user_pass=hashed_password,
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
    user = Users.query.filter_by(user_login=login).first()
    if user and verify_password(user.user_pass, password):
        return user
    return None

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
        object_gabaritType=gabarit_type,
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

# def get_equipment_by_category(category):
#     """Получить оборудование по категории"""
#     return Equipment.query.filter(
#         Equipment.object_name.ilike(f'%{category}%')
#     ).join(Rooms, Equipment.room_id == Rooms.room_id, isouter=True).all()

def check_equipment_availability(equipment_id):
    """Проверить доступность оборудования"""
    from datetime import datetime
    now = datetime.now()
    
    active_booking = Occupancy.query.filter(
        Occupancy.object_id == equipment_id,
        Occupancy.time_start <= now,
        Occupancy.time_end >= now
    ).first()
    
    return active_booking is None




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









def check_equipment_availability(equipment_id):
    """Проверить доступность оборудования"""
    from datetime import datetime
    now = datetime.now()
    
    # Проверяем, есть ли текущие бронирования
    active_booking = Occupancy.query.filter(
        Occupancy.object_id == equipment_id,
        Occupancy.time_start <= now,
        Occupancy.time_end >= now
    ).first()
    
    return active_booking is None

def get_equipment_bookings(equipment_id, limit=5):
    """Получить последние бронирования оборудования"""
    return BookHistory.query.filter_by(object_id=equipment_id)\
                           .order_by(BookHistory.data_book.desc())\
                           .limit(limit)\
                           .all()

# get_equipment_reviews уже реализована в вашем коде

def get_equipment_by_id(equipment_id):
    """
    Получить оборудование по ID с полной информацией
    :param equipment_id: ID оборудования
    :return: Объект Equipment или None, если не найдено
    """
    try:
        equipment = Equipment.query.get(equipment_id)
        
        if not equipment:
            app.logger.warning(f"Оборудование с ID {equipment_id} не найдено")
            return None
            
        # Добавляем дополнительную информацию о статусе оборудования
        equipment.is_available = check_equipment_availability(equipment_id)
        equipment.bookings = get_equipment_bookings(equipment_id)
        equipment.reviews = get_equipment_reviews(equipment_id)
        
        return equipment
        
    except Exception as e:
        app.logger.error(f"Ошибка при получении оборудования {equipment_id}: {str(e)}")
        return None
    

# для dashboard
def get_bookings_last_7_days():
    from datetime import datetime, timedelta, date
    from sqlalchemy import func
    
    today = date.today()
    seven_days_later = today + timedelta(days=7)
    print(today, seven_days_later)
    print()
    # Получаем количество бронирований по дням
    stats = db.session.query(
        BookHistory.data_book.label('date'),
        func.count(BookHistory.boking_id).label('count')
    ).filter(
        BookHistory.data_book >= today,
        BookHistory.data_book <= seven_days_later
    ).group_by(
        BookHistory.data_book
    ).order_by(
        BookHistory.data_book
    ).all()
    print(stats)
    
    # Создаем полный диапазон дат, даже если нет бронирований
    result = []
    current_date = today
    while current_date <= seven_days_later:
        date_str = current_date.isoformat()
        stat = next((s for s in stats if s.date.isoformat() == date_str), None)
        result.append({
            'date': date_str,
            'count': stat.count if stat else 0
        })
        current_date += timedelta(days=1)
    
    return result

def get_equipment_utilization_stats():
    from datetime import date, timedelta
    from sqlalchemy import func

    today = date.today()
    end_date = today + timedelta(days=7)

    total_equipment = db.session.query(func.count(Equipment.object_id)).scalar() or 1

    # Считаем количество уникального оборудования в бронированиях на каждый день
    booking_counts = db.session.query(
        BookHistory.data_book.label('date'),
        func.count(func.distinct(BookHistory.object_id)).label('booked_equipment')
    ).filter(
        BookHistory.data_book >= today,
        BookHistory.data_book <= end_date
    ).group_by(BookHistory.data_book).all()

    # Определяем самую популярную категорию на каждый день
    popular_categories = db.session.query(
        BookHistory.data_book.label('date'),
        Equipment.object_name.label('category'),
        func.count(BookHistory.boking_id).label('count')
    ).join(Equipment, Equipment.object_id == BookHistory.object_id
    ).filter(
        BookHistory.data_book >= today,
        BookHistory.data_book <= end_date
    ).group_by(BookHistory.data_book, Equipment.object_name).all()

    # Группируем по дате
    category_map = {}
    for entry in popular_categories:
        if entry.date not in category_map or entry.count > category_map[entry.date]['count']:
            category_map[entry.date] = {
                'popular_category': entry.category,
                'count': entry.count
            }

    # Собираем полные данные по дням
    result = []
    current_date = today
    while current_date <= end_date:
        booked_equipment = next((b.booked_equipment for b in booking_counts if b.date == current_date), 0)
        popular_category = category_map.get(current_date, {}).get('popular_category', 'Нет данных')
        result.append({
            'date': current_date.isoformat(),
            'booked_equipment': booked_equipment,
            'total_equipment': total_equipment,
            'popular_category': popular_category
        })
        current_date += timedelta(days=1)

    return result
