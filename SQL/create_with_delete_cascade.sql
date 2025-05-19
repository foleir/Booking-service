CREATE TABLE IF NOT EXISTS Rooms (
    room_id SERIAL PRIMARY KEY,
    room_name VARCHAR(255) NOT NULL,
    room_size VARCHAR(255) NOT NULL
);


CREATE TABLE IF NOT EXISTS Users (
    user_id SERIAL PRIMARY KEY,
    user_login VARCHAR(255) NOT NULL,
    user_pass VARCHAR(255) NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    user_surname VARCHAR(255) NOT NULL,
    user_role VARCHAR(5) NOT NULL
);


CREATE TABLE IF NOT EXISTS Equipment (
    object_id SERIAL PRIMARY KEY,
    object_name VARCHAR(255) NOT NULL,
    object_series VARCHAR(255) NOT NULL,
    obkect_gabaritType VARCHAR(255) NOT NULL,
    object_description TEXT,
    object_photo TEXT
);


CREATE TABLE IF NOT EXISTS Revievs (
    riviev_id SERIAL PRIMARY KEY,
    object_id INTEGER NOT NULL REFERENCES Equipment(object_id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES Users(user_id) ON DELETE CASCADE,
    reviev_text TEXT,
    UNIQUE (object_id, user_id)
);


CREATE TABLE IF NOT EXISTS Book_history (
    boking_id SERIAL PRIMARY KEY,
    object_id INTEGER NOT NULL REFERENCES Equipment(object_id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES Users(user_id) ON DELETE CASCADE,
    room_id INTEGER NOT NULL REFERENCES Rooms(room_id) ON DELETE CASCADE,
    data_book DATE NOT NULL,
    UNIQUE (object_id, user_id, room_id, data_book)
);


CREATE TABLE IF NOT EXISTS Occupancy (
    key_id SERIAL PRIMARY KEY,
    object_id INTEGER NOT NULL REFERENCES Equipment(object_id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES Users(user_id) ON DELETE CASCADE,
    room_id INTEGER NOT NULL REFERENCES Rooms(room_id) ON DELETE CASCADE,
    dataa DATE NOT NULL,
    time_start TIMESTAMP NOT NULL,
    time_end TIMESTAMP NOT NULL,
    CONSTRAINT valid_time_range CHECK (time_end > time_start),
    UNIQUE (object_id, user_id, room_id, time_start, time_end)
);


CREATE TABLE IF NOT EXISTS Favorites (
    object_id INTEGER NOT NULL REFERENCES Equipment(object_id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES Users(user_id) ON DELETE CASCADE,
    UNIQUE (object_id, user_id),
    PRIMARY KEY (object_id, user_id)
);





-- Еще можно добавить 2 таблицы(Но хз, надо ли)
-- -- Логирование действий пользователей
-- CREATE TABLE Audit_log (
--     log_id SERIAL PRIMARY KEY,
--     user_id INTEGER REFERENCES Users(user_id),
--     action_time TIMESTAMP DEFAULT NOW(),
--     action_type VARCHAR(50),
--     description TEXT
-- );

-- -- Уведомления для пользователей
-- CREATE TABLE Notifications (
--     notification_id SERIAL PRIMARY KEY,
--     user_id INTEGER REFERENCES Users(user_id) ON DELETE CASCADE,
--     message TEXT NOT NULL,
--     is_read BOOLEAN DEFAULT FALSE,
--     created_at TIMESTAMP DEFAULT NOW()
-- );