-- Пользователя (из таблицы Users)
-- Пользователя по ID
DELETE FROM Users WHERE user_id = 1;

-- Пользователя по логину
DELETE FROM Users WHERE user_login = 'ivanov';

-- Всех пользователей с ролью 'user'
DELETE FROM Users WHERE user_role = 'user';


-- Оборудования (из таблицы Equipment)
-- Оборудования по ID
DELETE FROM Equipment WHERE object_id = 2;

-- Оборудования по названию
DELETE FROM Equipment WHERE object_name = 'Проектор';

-- Всего оборудования определенной серии
DELETE FROM Equipment WHERE object_series = 'Epson EB-982';


-- Аудитории (из таблицы Rooms)
-- Аудитории по ID
DELETE FROM Rooms WHERE room_id = 3;

-- Аудитории по названию
DELETE FROM Rooms WHERE room_name = 'Аудитория 101';

-- Всех малых аудиторий
DELETE FROM Rooms WHERE room_size LIKE '%Малая%';


-- Избранное (из таблицы Favorites)
-- Конкретной записи из избранного
DELETE FROM Favorites WHERE user_id = 1 AND object_id = 2;

-- Всех избранных для конкретного пользователя
DELETE FROM Favorites WHERE user_id = 2;

-- Всех избранных для конкретного оборудования
DELETE FROM Favorites WHERE object_id = 3;


-- Истории бронирования (из таблицы Book_history)
-- Конкретной записи бронирования
DELETE FROM Book_history WHERE boking_id = 1;

-- Всех бронирований для конкретного оборудования
DELETE FROM Book_history WHERE object_id = 1;

-- Всех бронирований старше определенной даты
DELETE FROM Book_history WHERE data_book < '2025-01-01';


-- Таблица занятости (из таблицы Occupancy)
-- Конкретной записи занятости
DELETE FROM Occupancy WHERE key_id = 1;

-- Всех записей занятости для конкретной аудитории
DELETE FROM Occupancy WHERE room_id = 2;

-- Всех прошедших занятий
DELETE FROM Occupancy WHERE dataa < CURRENT_DATE;


-- Отзывы (из таблицы Revievs)
-- Отзыва по ID
DELETE FROM Revievs WHERE riviev_id = 1;

-- Всех отзывов пользователя
DELETE FROM Revievs WHERE user_id = 3;

-- Всех отзывов об оборудовании
DELETE FROM Revievs WHERE object_id = 2;