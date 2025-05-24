# database_setup.py
# from operations import *
# from datetime import datetime, date, time

# def populate_database():
#     print("Заполнение базы данных тестовыми данными...")
    
#     # Создание пользователей
#     users = [
#         create_user("admin", "admin123", "Иван", "Иванов", "Администратор"),
#         create_user("teacher1", "teach1", "Петр", "Петров", "Преподаватель"),
#         create_user("teacher2", "teach2", "Сергей", "Сергеев", "Преподаватель"),
#         create_user("student1", "stud1", "Алексей", "Алексеев", "Студент"),
#         create_user("student2", "stud2", "Дмитрий", "Дмитриев", "Студент")
#     ]
#     print(f"Создано {len(users)} пользователей")

#     # Создание комнат
#     rooms = [
#         create_room("Лекционная 51", "Большая"),
#         create_room("Лаборатория 201", "Средняя"),
#         create_room("Компьютерный класс 301", "Малая"),
#         create_room("Конференц-зал", "Большая"),
#         create_room("Кабинет 405", "Малая")
#     ]
#     print(f"Создано {len(rooms)} комнат")

#     # Создание оборудования
#     equipment = [
#         create_equipment("output_devices", "Epson EB-980", "Крупный", "Проектор высокой яркости", "images/objects/projector.png"),
#         create_equipment("computers", "Leica DM750", "Средний", "Биологический микроскоп", "images/objects/comp1.png"),
#         create_equipment("computers", "Dell XPS 15", "Малый", "Ноутбук для презентаций", "images/objects/comp2.png"),
#         create_equipment("media", "Creality Ender 3", "Крупный", "Принтер для печати моделей", "images/objects/printer1.png"),
#         create_equipment("media", "iPad Pro", "Малый", "Графический планшет", "images/objects/ipad.png")
#     ]
#     print(f"Создано {len(equipment)} единиц оборудования")

#     # Добавление в избранное
#     favorites = [
#         add_to_favorites(users[1].user_id, equipment[0].object_id),
#         add_to_favorites(users[1].user_id, equipment[2].object_id),
#         add_to_favorites(users[2].user_id, equipment[1].object_id),
#         add_to_favorites(users[3].user_id, equipment[3].object_id),
#         add_to_favorites(users[4].user_id, equipment[4].object_id)
#     ]
#     print(f"Создано {len(favorites)} записей в избранном")

#     # Создание бронирований
#     bookings = [
#         create_booking(equipment[0].object_id, users[1].user_id, rooms[0].room_id, date(2025, 5, 15)),
#         create_booking(equipment[1].object_id, users[2].user_id, rooms[1].room_id, date(2025, 5, 16)),
#         create_booking(equipment[2].object_id, users[3].user_id, rooms[2].room_id, date(2025, 5, 17)),
#         create_booking(equipment[3].object_id, users[4].user_id, rooms[3].room_id, date(2025, 5, 18)),
#         create_booking(equipment[4].object_id, users[1].user_id, rooms[4].room_id, date(2025, 5, 19))
#     ]
#     print(f"Создано {len(bookings)} бронирований")

#     # Создание занятости (расписания)
#     occupancies = [
#         create_occupancy(
#             equipment[0].object_id, 
#             users[1].user_id, 
#             rooms[0].room_id, 
#             date(2025, 5, 15), 
#             datetime(2025, 5, 15, 9, 0), 
#             datetime(2025, 5, 15, 11, 0)
#         ),
#         create_occupancy(
#             equipment[1].object_id, 
#             users[2].user_id, 
#             rooms[1].room_id, 
#             date(2025, 5, 16), 
#             datetime(2025, 5, 16, 5, 0), 
#             datetime(2025, 5, 16, 12, 0)
#         ),
#         create_occupancy(
#             equipment[2].object_id, 
#             users[3].user_id, 
#             rooms[2].room_id, 
#             date(2025, 5, 17), 
#             datetime(2025, 5, 17, 13, 0), 
#             datetime(2025, 5, 17, 15, 0)
#         ),
#         create_occupancy(
#             equipment[3].object_id, 
#             users[4].user_id, 
#             rooms[3].room_id, 
#             date(2025, 5, 18), 
#             datetime(2025, 5, 18, 14, 0), 
#             datetime(2025, 5, 18, 16, 0)
#         ),
#         create_occupancy(
#             equipment[4].object_id, 
#             users[1].user_id, 
#             rooms[4].room_id, 
#             date(2025, 5, 19), 
#             datetime(2025, 5, 19, 9, 0), 
#             datetime(2025, 5, 19, 11, 0)
#         )
#     ]
#     print(f"Создано {len(occupancies)} записей о занятости")

#     # Создание отзывов
#     reviews = [
#         create_review(equipment[0].object_id, users[1].user_id, "Отличный проектор, яркое изображение"),
#         create_review(equipment[1].object_id, users[2].user_id, "Микроскоп хорошего качества"),
#         create_review(equipment[2].object_id, users[3].user_id, "Ноутбук быстрый, но батарея держит недолго"),
#         create_review(equipment[3].object_id, users[4].user_id, "3D принтер печатает четко"),
#         create_review(equipment[4].object_id, users[1].user_id, "Планшет удобный для работы")
#     ]
#     print(f"Создано {len(reviews)} отзывов")

#     print("\nБаза данных успешно заполнена тестовыми данными!")

# def test_database_operations():
#     print("\nТестирование операций с базой данных:")
    
#     # 1. Тест аутентификации пользователя
#     print("\n1. Тест аутентификации пользователя:")
#     user = authenticate_user("admin", "admin123")
#     print(f"Аутентификация admin: {'успешна' if user else 'неудачна'} (ожидается успешна)")
#     user = authenticate_user("admin", "wrongpass")
#     print(f"Аутентификация с неверным паролем: {'успешна' if user else 'неудачна'} (ожидается неудачна)")

#     # 2. Тест получения пользователя по логину
#     print("\n2. Тест получения пользователя по логину:")
#     user = get_user_by_login("teacher1")
#     print(f"Пользователь teacher1: {user.user_name} {user.user_surname} (ожидается Петр Петров)")

#     # 3. Тест проверки ролей
#     print("\n3. Тест проверки ролей:")
#     print(f"Пользователь 1 - администратор: {is_admin(1)} (ожидается True)")
#     print(f"Пользователь 2 - преподаватель: {is_teacher(2)} (ожидается True)")
#     print(f"Пользователь 4 - преподаватель: {is_teacher(4)} (ожидается False)")

#     # 4. Тест получения оборудования
#     print("\n4. Тест получения оборудования:")
#     equipments = get_all_equipment()
#     print(f"Всего оборудования: {len(equipments)} (ожидается 5)")
#     print("Первое оборудование:", equipments[0].object_name, equipments[0].object_series)

#     # 5. Тест избранного
#     print("\n5. Тест избранного:")
#     favs = get_user_favorites(2)  # teacher1
#     print(f"Избранное teacher1: {len(favs)} элементов (ожидается 2)")
#     for f in favs:
#         print(f"- {f.object_name}")

#     # 6. Тест бронирований
#     print("\n6. Тест бронирований:")
#     books = get_user_bookings(2)  # teacher1
#     print(f"Бронирования teacher1: {len(books)} (ожидается 2)")
#     for b in books:
#         equipment = next(e for e in get_all_equipment() if e.object_id == b.object_id)
#         print(f"- {equipment.object_name} на {b.data_book}")

#     # 7. Тест проверки доступности
#     print("\n7. Тест проверки доступности:")
#     is_available = check_availability(
#         1,  # Проектор
#         1,  # Лекционная 51
#         date(2025, 5, 15), 
#         datetime(2025, 5, 15, 5, 0), 
#         datetime(2025, 5, 15, 12, 0)
#     )
#     print(f"Проектор в лекционной 51 15.5.2025 5:00-12:00: {'доступен' if is_available else 'занят'} (ожидается занят)")

#     # 8. Тест отзывов
#     print("\n8. Тест отзывов:")
#     revs = get_equipment_reviews(1)  # Проектор
#     print(f"Отзывов на проектор: {len(revs)} (ожидается 1)")
#     for r in revs:
#         user = get_user_by_id(r.user_id)
#         print(f"- {user.user_name}: {r.reviev_text}")

#     # 9. Тест статистики оборудования
#     print("\n9. Тест статистики оборудования:")
#     stats = get_equipment_stats()
#     print("Статистика по оборудованию:")
#     for stat in stats:
#         print(f"- {stat.object_name}: бронирований - {stat.booking_count}, отзывов - {stat.review_count}")

#     # 5. Тест доступных комнат
#     print("\n5. Тест доступных комнат:")
#     available_rooms = get_available_rooms(
#         date(2025, 5, 15), 
#         datetime(2025, 5, 15, 5, 0), 
#         datetime(2025, 5, 15, 14, 0)
#     )
#     print(f"Доступных комнат 15.05.2025 5:00-14:00: {len(available_rooms)} (ожидается 4, так как лекционная 51 занята)")
from models import db, Users, Equipment, Rooms, Favorites, BookHistory, Occupancy, Revievs
from datetime import datetime, date, time
from security import hash_password
from operations import *
from datetime import timedelta

today = date.today()
def populate_database():
    print("Заполнение базы данных тестовыми данными...")
    
    # Создание пользователей
    users = [
        create_user("admin", "admin123", "Иван", "Иванов", "Администратор"),
        create_user("teacher1", "teach1", "Петр", "Петров", "Преподаватель"),
        create_user("teacher2", "teach2", "Сергей", "Сергеев", "Преподаватель"),
        create_user("student1", "stud1", "Алексей", "Алексеев", "Студент"),
        create_user("student2", "stud2", "Дмитрий", "Дмитриев", "Студент"),
        create_user("teacher3", "teach3", "Анна", "Смирнова", "Преподаватель"),
        create_user("admin2", "admin456", "Ольга", "Кузнецова", "Администратор")
    ]
    print(f"Создано {len(users)} пользователей")

    # Создание комнат
    rooms = [
        create_room("Лекционная 51", "Большая"),
        create_room("Лаборатория 201", "Средняя"),
        create_room("Компьютерный класс 301", "Малая"),
        create_room("Конференц-зал", "Большая"),
        create_room("Кабинет 405", "Малая"),
        create_room("Лаборатория 102", "Средняя"),
        create_room("Аудитория 215", "Большая")
    ]
    print(f"Создано {len(rooms)} комнат")

    # Создание оборудования
    equipment = [
        # output_devices
        create_equipment("output_devices", "Epson EB-980", "Крупный", "Проектор высокой яркости", "images/objects/projector.png"),
        create_equipment("output_devices", "BenQ MW632", "Средний", "Проектор для образовательных учреждений", "images/objects/projector2.png"),
        create_equipment("output_devices", "LG UltraFine 4K", "Малый", "Монитор с высоким разрешением", "images/objects/monitor1.png"),
        
        # computers
        create_equipment("computers", "Dell XPS 15", "Малый", "Ноутбук для презентаций", "images/objects/comp1.png"),
        create_equipment("computers", "HP EliteDesk 800", "Средний", "Настольный компьютер для лабораторий", "images/objects/comp2.png"),
        create_equipment("computers", "Apple Mac Mini M2", "Малый", "Компактный компьютер для мультимедиа", "images/objects/macmini1.png"),
        
        # media
        create_equipment("media", "iPad Pro 12.9", "Малый", "Графический планшет", "images/objects/ipad1.png"),
        create_equipment("media", "Wacom Cintiq 22", "Средний", "Графический планшет с экраном", "images/objects/wacom1.png"),
        create_equipment("media", "GoPro Hero 10", "Малый", "Экшн-камера для съемки", "images/objects/gopro1.png"),
        
        # cables_adapters
        create_equipment("cables_adapters", "HDMI 2.1", "Малый", "Кабель HDMI 4K 120Hz", "images/objects/hdmi1.png"),
        create_equipment("cables_adapters", "USB-C Hub", "Малый", "Концентратор с 6 портами", "images/objects/usbhub1.png"),
        create_equipment("cables_adapters", "VGA-DVI адаптер", "Малый", "Адаптер для подключения мониторов", "images/objects/adapter1.png"),
        
        # input_devices
        create_equipment("input_devices", "Logitech MX Keys", "Малый", "Беспроводная клавиатура", "images/objects/keyboard1.png"),
        create_equipment("input_devices", "Apple Magic Mouse", "Малый", "Беспроводная мышь", "images/objects/mouse1.png"),
        create_equipment("input_devices", "Blue Yeti Nano", "Средний", "USB микрофон", "/images/objects/microphone1.png"),
        
        # monitors
        create_equipment("monitors", "Dell UltraSharp 27", "Средний", "4K монитор с точной цветопередачей", "images/objects/monitor2.png"),
        create_equipment("monitors", "Samsung Odyssey G7", "Средний", "Игровой монитор 240Hz", "images/objects/monitor3.png"),
        create_equipment("monitors", "LG 34WN80C", "Крупный", "Широкоформатный монитор", "images/objects/monitor4.png"),
        
        # network_equipment
        create_equipment("network_equipment", "Ubiquiti UniFi AP", "Малый", "Точка доступа для образовательных учреждений", "images/objects/accesspoint1.png"),
        create_equipment("network_equipment", "NETGEAR GS308", "Малый", "8-портовый коммутатор", "images/objects/switch1.png"),
        
        # printers_scanners
        create_equipment("printers_scanners", "Epson EcoTank ET-4760", "Средний", "МФУ с СНПЧ", "images/objects/printer1.png"),
        create_equipment("printers_scanners", "Canon imageFORMULA DR-C240", "Средний", "Скоростной сканер документов", "images/objects/scanner1.png"),
        create_equipment("printers_scanners", "HP LaserJet Pro MFP", "Средний", "Лазерное МФУ", "images/objects/printer2.png"),
        
        # accessories
        create_equipment("accessories", "Amazon Echo Dot", "Малый", "Умная колонка", "images/objects/speaker1.png"),
        create_equipment("accessories", "Anker PowerCore 26800", "Малый", "Внешний аккумулятор", "images/objects/powerbank1.png"),
        create_equipment("accessories", "Logitech C920", "Малый", "Веб-камера HD", "images/objects/webcam1.png"),
        
        # routers_modems
        create_equipment("routers_modems", "ASUS RT-AX86U", "Малый", "Wi-Fi 6 роутер", "images/objects/adapter1.png"),
        create_equipment("routers_modems", "Huawei E8372", "Малый", "4G модем", "images/objects/modem1.png"),
        create_equipment("routers_modems", "MikroTik hEX S", "Малый", "Гигабитный роутер", "images/objects/router1.png")
    ]
    print(f"Создано {len(equipment)} единиц оборудования")

    # Добавление в избранное
    favorites = [
        add_to_favorites(users[1].user_id, equipment[0].object_id),
        add_to_favorites(users[1].user_id, equipment[2].object_id),
        add_to_favorites(users[2].user_id, equipment[1].object_id),
        add_to_favorites(users[3].user_id, equipment[3].object_id),
        add_to_favorites(users[4].user_id, equipment[4].object_id),
        add_to_favorites(users[5].user_id, equipment[5].object_id),
        add_to_favorites(users[6].user_id, equipment[6].object_id)
    ]
    print(f"Создано {len(favorites)} записей в избранном")

    # Создание бронирований (прошедшие и будущие в 2025 году)
    bookings = [
        # Прошедшие бронирования
        create_booking(equipment[0].object_id, users[1].user_id, rooms[0].room_id, date(2025, 1, 15)),
        create_booking(equipment[1].object_id, users[2].user_id, rooms[1].room_id, date(2025, 2, 10)),
        create_booking(equipment[2].object_id, users[3].user_id, rooms[2].room_id, date(2025, 3, 5)),
        create_booking(equipment[3].object_id, users[4].user_id, rooms[3].room_id, date(2025, 4, 20)),
        create_booking(equipment[4].object_id, users[5].user_id, rooms[4].room_id, date(2025, 5, 12)),
        
        # Будущие бронирования
        create_booking(equipment[5].object_id, users[1].user_id, rooms[5].room_id, date(2025, 8, 15)),
        create_booking(equipment[6].object_id, users[2].user_id, rooms[6].room_id, date(2025, 9, 1)),
        create_booking(equipment[7].object_id, users[3].user_id, rooms[0].room_id, date(2025, 10, 10)),
        create_booking(equipment[8].object_id, users[4].user_id, rooms[1].room_id, date(2025, 11, 25)),
        create_booking(equipment[9].object_id, users[5].user_id, rooms[2].room_id, date(2025, 12, 5)),
        create_booking(equipment[0].object_id, users[1].user_id, rooms[0].room_id, today),
        create_booking(equipment[1].object_id, users[2].user_id, rooms[1].room_id, today + timedelta(days=1)),
        create_booking(equipment[2].object_id, users[3].user_id, rooms[2].room_id, today + timedelta(days=2)),
        create_booking(equipment[3].object_id, users[4].user_id, rooms[3].room_id, today + timedelta(days=3)),
        create_booking(equipment[4].object_id, users[5].user_id, rooms[4].room_id, today + timedelta(days=4)),
        create_booking(equipment[5].object_id, users[6].user_id, rooms[5].room_id, today + timedelta(days=5)),
        create_booking(equipment[6].object_id, users[1].user_id, rooms[6].room_id, today + timedelta(days=2)),
        create_booking(equipment[6].object_id, users[2].user_id, rooms[1].room_id, today + timedelta(days=3)),
        create_booking(equipment[6].object_id, users[4].user_id, rooms[4].room_id, today + timedelta(days=2)),
        create_booking(equipment[6].object_id, users[3].user_id, rooms[4].room_id, today + timedelta(days=2)),
    ]
    print(f"Создано {len(bookings)} бронирований")

    # Создание занятости (расписания)
    occupancies = [
    # Прошедшие занятия
    create_occupancy(
        equipment[0].object_id, 
        users[1].user_id, 
        rooms[0].room_id, 
        date(2025, 1, 15), 
        datetime(2025, 1, 15, 9, 0), 
        datetime(2025, 1, 15, 11, 0)
    ),
    create_occupancy(
        equipment[1].object_id, 
        users[2].user_id, 
        rooms[1].room_id, 
        date(2025, 2, 10), 
        datetime(2025, 2, 10, 13, 0), 
        datetime(2025, 2, 10, 15, 0)
    ),
    create_occupancy(
        equipment[2].object_id, 
        users[3].user_id, 
        rooms[2].room_id, 
        date(2025, 3, 5), 
        datetime(2025, 3, 5, 10, 0), 
        datetime(2025, 3, 5, 12, 0)
    ),
    
    # Будущие занятия
    create_occupancy(
        equipment[5].object_id, 
        users[1].user_id, 
        rooms[5].room_id, 
        date(2025, 8, 15), 
        datetime(2025, 8, 15, 14, 0), 
        datetime(2025, 8, 15, 16, 0)
    ),
    create_occupancy(
        equipment[6].object_id, 
        users[2].user_id, 
        rooms[6].room_id, 
        date(2025, 9, 1), 
        datetime(2025, 9, 1, 9, 0), 
        datetime(2025, 9, 1, 11, 0)
    ),
    create_occupancy(
        equipment[7].object_id, 
        users[3].user_id, 
        rooms[0].room_id, 
        date(2025, 10, 10), 
        datetime(2025, 10, 10, 13, 0), 
        datetime(2025, 10, 10, 15, 0)
    ),
    
    # Занятия на будущую неделю (24.05.2025 - 30.05.2025)
    # Понедельник 26.05 - проектор и компьютер
    create_occupancy(
        equipment[0].object_id,  # Проектор Epson
        users[1].user_id, 
        rooms[0].room_id, 
        date(2025, 5, 26), 
        datetime(2025, 5, 26, 9, 0), 
        datetime(2025, 5, 26, 11, 0)
    ),
    create_occupancy(
        equipment[3].object_id,  # Ноутбук Dell
        users[2].user_id, 
        rooms[1].room_id, 
        date(2025, 5, 26), 
        datetime(2025, 5, 26, 13, 0), 
        datetime(2025, 5, 26, 15, 0)
    ),
    
    # Вторник 27.05 - монитор и сетевое оборудование
    create_occupancy(
        equipment[14].object_id,  # Монитор Dell
        users[3].user_id, 
        rooms[2].room_id, 
        date(2025, 5, 27), 
        datetime(2025, 5, 27, 10, 0), 
        datetime(2025, 5, 27, 12, 0)
    ),
    create_occupancy(
        equipment[16].object_id,  # Точка доступа Ubiquiti
        users[4].user_id, 
        rooms[3].room_id, 
        date(2025, 5, 27), 
        datetime(2025, 5, 27, 14, 0), 
        datetime(2025, 5, 27, 16, 0)
    ),
    
    # Среда 28.05 - принтер и планшет
    create_occupancy(
        equipment[21].object_id,  # Принтер Epson
        users[5].user_id, 
        rooms[4].room_id, 
        date(2025, 5, 28), 
        datetime(2025, 5, 28, 9, 0), 
        datetime(2025, 5, 28, 11, 0)
    ),
    create_occupancy(
        equipment[6].object_id,  # iPad Pro
        users[6].user_id, 
        rooms[5].room_id, 
        date(2025, 5, 28), 
        datetime(2025, 5, 28, 13, 0), 
        datetime(2025, 5, 28, 15, 0)
    ),
    
    # Четверг 29.05 - роутер и камера
    create_occupancy(
        equipment[25].object_id,  # Роутер ASUS
        users[1].user_id, 
        rooms[6].room_id, 
        date(2025, 5, 29), 
        datetime(2025, 5, 29, 10, 0), 
        datetime(2025, 5, 29, 12, 0)
    ),
    create_occupancy(
        equipment[27].object_id,  # Веб-камера Logitech
        users[2].user_id, 
        rooms[0].room_id, 
        date(2025, 5, 29), 
        datetime(2025, 5, 29, 14, 0), 
        datetime(2025, 5, 29, 16, 0)
    ),
    
    # Пятница 30.05 - микрофон и адаптер
    create_occupancy(
        equipment[17].object_id,  # Микрофон Blue Yeti
        users[3].user_id, 
        rooms[1].room_id, 
        date(2025, 5, 30), 
        datetime(2025, 5, 30, 9, 0), 
        datetime(2025, 5, 30, 11, 0)
    ),
    create_occupancy(
        equipment[9].object_id,  # Адаптер VGA-DVI
        users[4].user_id, 
        rooms[2].room_id, 
        date(2025, 5, 30), 
        datetime(2025, 5, 30, 13, 0), 
        datetime(2025, 5, 30, 15, 0)
    )
    ]
    print(f"Создано {len(occupancies)} записей о занятости")

    # Создание отзывов (от преподавателей и администраторов)
    reviews = [
        # Отзывы от преподавателей
        create_review(equipment[0].object_id, users[1].user_id, "Отличный проектор, яркое изображение даже в освещенной аудитории."),
        create_review(equipment[1].object_id, users[2].user_id, "Мощный компьютер, справляется с любыми задачами."),
        create_review(equipment[2].object_id, users[5].user_id, "Удобный монитор с точной цветопередачей для дизайнерских работ."),
        create_review(equipment[3].object_id, users[1].user_id, "Ноутбук отличного качества, но батарея держит недолго."),
        create_review(equipment[4].object_id, users[2].user_id, "Надежный стационарный компьютер для лабораторных работ."),
        
        # Отзывы от администраторов
        create_review(equipment[5].object_id, users[0].user_id, "Отличное оборудование для мобильной работы."),
        create_review(equipment[6].object_id, users[6].user_id, "Графический планшет высокого качества, но требует привыкания."),
        create_review(equipment[7].object_id, users[0].user_id, "Удобный кабель, никаких проблем с подключением."),
        create_review(equipment[8].object_id, users[6].user_id, "Хороший концентратор, но греется при активном использовании."),
        create_review(equipment[9].object_id, users[0].user_id, "Клавиатура удобная, но клавиши немного шумные.")
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
    print(f"Всего оборудования: {len(equipments)} (ожидается 30)")
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
        1,  # Лекционная 51
        date(2025, 1, 15), 
        datetime(2025, 1, 15, 5, 0), 
        datetime(2025, 1, 15, 12, 0)
    )
    print(f"Проектор в лекционной 51 15.1.2025 5:00-12:00: {'доступен' if is_available else 'занят'} (ожидается занят)")

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
        date(2025, 1, 15), 
        datetime(2025, 1, 15, 5, 0), 
        datetime(2025, 1, 15, 14, 0)
    )
    print(f"Доступных комнат 15.01.2025 5:00-14:00: {len(available_rooms)} (ожидается 6, так как лекционная 51 занята)")