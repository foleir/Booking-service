INSERT INTO Users (user_login, user_pass, user_name, user_surname, user_role) -- Регистрация
-- VALUES 
--     ('biba', 'boba', 'Иван', 'Хомяков', 'A'); -- A-user, B-teacher, C-admin


INSERT INTO Equipment (object_name, object_series, obkect_gabaritType, object_description, object_photo) -- Добавление оборудования
-- VALUES 
--     ('Проектор', 'Epson EB-982', 'Средний', 'Яркий проектор с разрешением Full HD', '/photos/projector1.jpg');


INSERT INTO Rooms (room_name, room_size) -- Добавление аудитории
-- VALUES 
--     ('Аудитория 17', 'Малая');


INSERT INTO Favorites (user_id, object_id) -- Добавление Избранного
-- VALUES 
--     (1, 2); -- Пользователь 1 добавил микрофон в избранное


INSERT INTO Book_history (object_id, user_id, room_id, data_book) -- Добавление истории бронирования
-- VALUES 
--     (1, 2, 1, '2025-04-10'); -- Пользователь 2 забронировал проектор в аудитории 101


INSERT INTO Occupancy (object_id, user_id, room_id, dataa, time_start, time_end) -- Добавление таблицы занятости
-- VALUES 
--     (1, 2, 1, '2025-04-10', '2025-04-10 09:00:00', '2025-04-10 11:00:00');


INSERT INTO Revievs (object_id, user_id, reviev_text) -- Добавление Отзывов
-- VALUES 
--     (1, 2, 'Отличный проектор, яркое изображение даже при дневном свете');