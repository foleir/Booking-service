-- 1. Проверка при регистрации (существует ли пользователь)
SELECT user_id FROM Users 
WHERE user_login = 'login';
-- Если запрос вернул результат, значит пользователь уже существует


-- 2. Проверка при входе (аутентификация)
SELECT user_id, user_name, user_surname, user_role 
FROM Users 
WHERE user_login = 'biba' AND user_pass = 'boba';
-- Если запрос вернул результат - аутентификация успешна


-- 3. Получение избранного оборудования пользователя
SELECT e.object_id, e.object_name, e.object_photo
FROM Favorites f
JOIN Equipment e ON f.object_id = e.object_id
WHERE f.user_id = введите_user_id;


-- 4. История бронирования пользователя
SELECT 
    u.user_name, 
    u.user_surname,
    e.object_name,
    e.object_series,
    e.object_photo,
    r.room_name,
    bh.data_book
FROM Book_history bh
JOIN Users u ON bh.user_id = u.user_id
JOIN Equipment e ON bh.object_id = e.object_id
JOIN Rooms r ON bh.room_id = r.room_id
WHERE bh.user_id = введите_user_id
ORDER BY bh.data_book DESC;


-- 5. Проверка занятости оборудования/аудитории
    -- 5.1. Проверка доступности (свободно/занято)
SELECT 
    CASE 
        WHEN EXISTS (
            SELECT 1 FROM Occupancy 
            WHERE object_id = введите_object_id 
            AND room_id = введите_room_id
            AND dataa = 'введите_дату'
            AND time_start <= 'введите_время_окончания'
            AND time_end >= 'введите_время_начала'
        ) THEN 'Занято'
        ELSE 'Свободно'
    END AS availability_status;

    -- 5.2. Показать занятое время для объекта/аудитории
SELECT 
    o.time_start, 
    o.time_end,
    u.user_name,
    u.user_surname
FROM Occupancy o
JOIN Users u ON o.user_id = u.user_id
WHERE o.object_id = введите_object_id 
AND o.room_id = введите_room_id
AND o.dataa = 'введите_дату'
ORDER BY o.time_start;

    -- 5.3 Расширенная проверка занятости с временными интервалами:
-- Проверка доступности с учетом времени
SELECT 
    o.time_start, 
    o.time_end,
    e.object_name,
    r.room_name,
    u.user_name || ' ' || u.user_surname AS booked_by
FROM Occupancy o
JOIN Equipment e ON o.object_id = e.object_id
JOIN Rooms r ON o.room_id = r.room_id
JOIN Users u ON o.user_id = u.user_id
WHERE o.room_id = 1
AND o.dataa = '2025-05-15'
AND o.time_start <= '2025-05-15 14:00:00'
AND o.time_end >= '2025-05-15 13:00:00'
ORDER BY o.time_start;


-- 6. Получение отзывов об оборудовании
SELECT 
    e.object_name,
    u.user_id,
    u.user_name,
    u.user_surname,
    r.reviev_text
FROM Revievs r
JOIN Equipment e ON r.object_id = e.object_id
JOIN Users u ON r.user_id = u.user_id
WHERE r.object_id = введите_object_id
ORDER BY r.riviev_id DESC;


-- 7. Дополнительные запросы
    -- Проверка уровня прав пользователя
SELECT user_role FROM Users WHERE user_id = '<user_id>';


    -- Получение списка всех аудиторий
SELECT room_id, room_name, room_size FROM Rooms ORDER BY room_name;

    -- Получение списка всего оборудования
SELECT object_id, object_name, object_series FROM Equipment ORDER BY object_name;

    -- Проверка является ли пользователь преподавателем
SELECT CASE WHEN user_role = 'B' THEN TRUE ELSE FALSE END AS is_teacher
FROM Users WHERE user_id = '<user_id>';

    -- Проверка является ли пользователь администратором
SELECT CASE WHEN user_role = 'C' THEN TRUE ELSE FALSE END AS is_admin
FROM Users WHERE user_id = '<user_id>';

    -- Поиск свободных аудиторий на конкретную дату и время:
SELECT r.room_id, r.room_name
FROM Rooms r
WHERE NOT EXISTS (
    SELECT 1 FROM Occupancy o
    WHERE o.room_id = r.room_id
    AND o.dataa = '2025-05-15'
    AND o.time_start <= '2025-05-15 15:00:00'
    AND o.time_end >= '2025-05-15 14:00:00'
);

    -- Статистика использования оборудования:
SELECT 
    e.object_name,
    COUNT(b.object_id) AS booking_count,
    AVG(r.rating) AS average_rating
FROM Equipment e
LEFT JOIN Book_history b ON e.object_id = b.object_id
LEFT JOIN (
    SELECT object_id, COUNT(*) as rating 
    FROM Revievs 
    GROUP BY object_id
) r ON e.object_id = r.object_id
GROUP BY e.object_name
ORDER BY booking_count DESC;


    -- Хеширование паролей: Используйте pgcrypto для хранения паролей(ДикПик добавил, мб пригодиться)
CREATE EXTENSION pgcrypto;
INSERT INTO Users (user_login, user_pass) 
VALUES ('user1', crypt('password123', gen_salt('bf')));