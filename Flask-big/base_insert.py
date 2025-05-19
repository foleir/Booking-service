from create_BD import db, Users, Equipment, Rooms, Favorites, BookHistory, Occupancy, Revievs
from datetime import datetime, date

def insert_sample_data():
    # Регистрация пользователя
    user1 = Users(
        user_login='biba',
        user_pass='boba',
        user_name='Иван',
        user_surname='Хомяков',
        user_role='A'
    )
    db.session.add(user1)

    # Добавление оборудования
    equipment1 = Equipment(
        object_name='Проектор',
        object_series='Epson EB-982',
        obkect_gabaritType='Средний',
        object_description='Яркий проектор с разрешением Full HD',
        object_photo='/photos/projector1.jpg'
    )
    db.session.add(equipment1)

    # Добавление аудитории
    room1 = Rooms(
        room_name='Аудитория 17',
        room_size='Малая'
    )
    db.session.add(room1)

    db.session.commit()

    # Добавление в избранное
    favorite1 = Favorites(
        user_id=user1.user_id,
        object_id=equipment1.object_id
    )
    db.session.add(favorite1)

    # Добавление истории бронирования
    booking1 = BookHistory(
        object_id=equipment1.object_id,
        user_id=user1.user_id,
        room_id=room1.room_id,
        data_book=date(2025, 4, 10)
    )
    db.session.add(booking1)

    # Добавление занятости
    occupancy1 = Occupancy(
        object_id=equipment1.object_id,
        user_id=user1.user_id,
        room_id=room1.room_id,
        dataa=date(2025, 4, 10),
        time_start=datetime(2025, 4, 10, 9, 0, 0),
        time_end=datetime(2025, 4, 10, 11, 0, 0)
    )
    db.session.add(occupancy1)

    # Добавление отзыва
    review1 = Revievs(
        object_id=equipment1.object_id,
        user_id=user1.user_id,
        reviev_text='Отличный проектор, яркое изображение даже при дневном свете'
    )
    db.session.add(review1)

    db.session.commit()