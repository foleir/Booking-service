# database_setup.py
from operations import *
from datetime import datetime, date, time

def populate_database():
    print("Заполнение базы данных тестовыми данными...")
    
    # Создание пользователей
    users = [
        create_user("admin", "admin123", "Иван", "Иванов", "Администратор"),
        create_user("teacher1", "teach1", "Петр", "Петров", "Преподаватель"),
        create_user("teacher2", "teach2", "Сергей", "Сергеев", "Преподаватель"),
        create_user("student1", "stud1", "Алексей", "Алексеев", "Студент"),
        create_user("student2", "stud2", "Дмитрий", "Дмитриев", "Студент")
    ]
    print(f"Создано {len(users)} пользователей")

    # Создание комнат
    rooms = [
        create_room("Лекционная 101", "Большая"),
        create_room("Лаборатория 201", "Средняя"),
        create_room("Компьютерный класс 301", "Малая"),
        create_room("Конференц-зал", "Большая"),
        create_room("Кабинет 405", "Малая")
    ]
    print(f"Создано {len(rooms)} комнат")

    # Создание оборудования
    equipment = [
        create_equipment("Проектор", "Epson EB-980", "Крупногабаритный", "Проектор высокой яркости", "projector.jpg"),
        create_equipment("Микроскоп", "Leica DM750", "Среднегабаритный", "Биологический микроскоп", "microscope.jpg"),
        create_equipment("Ноутбук", "Dell XPS 15", "Малогабаритный", "Ноутбук для презентаций", "laptop.jpg"),
        create_equipment("3D принтер", "Creality Ender 3", "Крупногабаритный", "Принтер для печати моделей", "3dprinter.jpg"),
        create_equipment("Планшет", "iPad Pro", "Малогабаритный", "Графический планшет", "tablet.jpg")
    ]
    print(f"Создано {len(equipment)} единиц оборудования")

    # Добавление в избранное
    favorites = [
        add_to_favorites(users[1].user_id, equipment[0].object_id),
        add_to_favorites(users[1].user_id, equipment[2].object_id),
        add_to_favorites(users[2].user_id, equipment[1].object_id),
        add_to_favorites(users[3].user_id, equipment[3].object_id),
        add_to_favorites(users[4].user_id, equipment[4].object_id)
    ]
    print(f"Создано {len(favorites)} записей в избранном")

    # Создание бронирований
    bookings = [
        create_booking(equipment[0].object_id, users[1].user_id, rooms[0].room_id, date(2023, 10, 15)),
        create_booking(equipment[1].object_id, users[2].user_id, rooms[1].room_id, date(2023, 10, 16)),
        create_booking(equipment[2].object_id, users[3].user_id, rooms[2].room_id, date(2023, 10, 17)),
        create_booking(equipment[3].object_id, users[4].user_id, rooms[3].room_id, date(2023, 10, 18)),
        create_booking(equipment[4].object_id, users[1].user_id, rooms[4].room_id, date(2023, 10, 19))
    ]
    print(f"Создано {len(bookings)} бронирований")

    # Создание занятости (расписания)
    occupancies = [
        create_occupancy(
            equipment[0].object_id, 
            users[1].user_id, 
            rooms[0].room_id, 
            date(2023, 10, 15), 
            datetime(2023, 10, 15, 9, 0), 
            datetime(2023, 10, 15, 11, 0)
        ),
        create_occupancy(
            equipment[1].object_id, 
            users[2].user_id, 
            rooms[1].room_id, 
            date(2023, 10, 16), 
            datetime(2023, 10, 16, 10, 0), 
            datetime(2023, 10, 16, 12, 0)
        ),
        create_occupancy(
            equipment[2].object_id, 
            users[3].user_id, 
            rooms[2].room_id, 
            date(2023, 10, 17), 
            datetime(2023, 10, 17, 13, 0), 
            datetime(2023, 10, 17, 15, 0)
        ),
        create_occupancy(
            equipment[3].object_id, 
            users[4].user_id, 
            rooms[3].room_id, 
            date(2023, 10, 18), 
            datetime(2023, 10, 18, 14, 0), 
            datetime(2023, 10, 18, 16, 0)
        ),
        create_occupancy(
            equipment[4].object_id, 
            users[1].user_id, 
            rooms[4].room_id, 
            date(2023, 10, 19), 
            datetime(2023, 10, 19, 9, 0), 
            datetime(2023, 10, 19, 11, 0)
        )
    ]
    print(f"Создано {len(occupancies)} записей о занятости")

    # Создание отзывов
    reviews = [
        create_review(equipment[0].object_id, users[1].user_id, "Отличный проектор, яркое изображение"),
        create_review(equipment[1].object_id, users[2].user_id, "Микроскоп хорошего качества"),
        create_review(equipment[2].object_id, users[3].user_id, "Ноутбук быстрый, но батарея держит недолго"),
        create_review(equipment[3].object_id, users[4].user_id, "3D принтер печатает четко"),
        create_review(equipment[4].object_id, users[1].user_id, "Планшет удобный для работы")
    ]
    print(f"Создано {len(reviews)} отзывов")

    print("\nБаза данных успешно заполнена тестовыми данными!")

def test_database_operations():
    print("\nТестирование операций с базой данных:")
    
    # 1. Тест аутентификации пользователя
    print("\n1. Тест аутентификации пользователя:")
    user = authenticate_user("admin", "admin123")
    print(f"Аутентификация admin: {'успешна' if user else 'неудачна'} (ожидается успешна)")
    user = authenticate_user("admin", "wrongpass")
    print(f"Аутентификация с неверным паролем: {'успешна' if user else 'неудачна'} (ожидается неудачна)")

    # 2. Тест получения пользователя по логину
    print("\n2. Тест получения пользователя по логину:")
    user = get_user_by_login("teacher1")
    print(f"Пользователь teacher1: {user.user_name} {user.user_surname} (ожидается Петр Петров)")

    # 3. Тест проверки ролей
    print("\n3. Тест проверки ролей:")
    print(f"Пользователь 1 - администратор: {is_admin(1)} (ожидается True)")
    print(f"Пользователь 2 - преподаватель: {is_teacher(2)} (ожидается True)")
    print(f"Пользователь 4 - преподаватель: {is_teacher(4)} (ожидается False)")

    # 4. Тест получения оборудования
    print("\n4. Тест получения оборудования:")
    equipments = get_all_equipment()
    print(f"Всего оборудования: {len(equipments)} (ожидается 5)")
    print("Первое оборудование:", equipments[0].object_name, equipments[0].object_series)

    # 5. Тест избранного
    print("\n5. Тест избранного:")
    favs = get_user_favorites(2)  # teacher1
    print(f"Избранное teacher1: {len(favs)} элементов (ожидается 2)")
    for f in favs:
        print(f"- {f.object_name}")

    # 6. Тест бронирований
    print("\n6. Тест бронирований:")
    books = get_user_bookings(2)  # teacher1
    print(f"Бронирования teacher1: {len(books)} (ожидается 2)")
    for b in books:
        equipment = next(e for e in get_all_equipment() if e.object_id == b.object_id)
        print(f"- {equipment.object_name} на {b.data_book}")

    # 7. Тест проверки доступности
    print("\n7. Тест проверки доступности:")
    is_available = check_availability(
        1,  # Проектор
        1,  # Лекционная 101
        date(2023, 10, 15), 
        datetime(2023, 10, 15, 10, 0), 
        datetime(2023, 10, 15, 12, 0)
    )
    print(f"Проектор в лекционной 101 15.10.2023 10:00-12:00: {'доступен' if is_available else 'занят'} (ожидается занят)")

    # 8. Тест отзывов
    print("\n8. Тест отзывов:")
    revs = get_equipment_reviews(1)  # Проектор
    print(f"Отзывов на проектор: {len(revs)} (ожидается 1)")
    for r in revs:
        user = get_user_by_id(r.user_id)
        print(f"- {user.user_name}: {r.reviev_text}")

    # 9. Тест статистики оборудования
    print("\n9. Тест статистики оборудования:")
    stats = get_equipment_stats()
    print("Статистика по оборудованию:")
    for stat in stats:
        print(f"- {stat.object_name}: бронирований - {stat.booking_count}, отзывов - {stat.review_count}")

    # 10. Тест доступных комнат
    print("\n10. Тест доступных комнат:")
    available_rooms = get_available_rooms(
        date(2023, 10, 15), 
        datetime(2023, 10, 15, 10, 0), 
        datetime(2023, 10, 15, 14, 0)
    )
    print(f"Доступных комнат 15.10.2023 10:00-14:00: {len(available_rooms)} (ожидается 4, так как лекционная 101 занята)")