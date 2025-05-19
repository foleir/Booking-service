CREATE TABLE IF NOT EXISTS Rooms (
	room_id SERIAL PRIMARY KEY,
	room_name VARCHAR(255) NOT null,
    room_size VARCHAR(255) NOT null
);


CREATE TABLE IF NOT EXISTS Users (
	user_id SERIAL PRIMARY KEY,
    user_login VARCHAR(255) NOT null,
	user_pass VARCHAR(255) NOT null,
	user_name VARCHAR(255) NOT NULL,
	user_surname VARCHAR(255) NOT null,
	user_role VARCHAR(5) NOT null
);


CREATE TABLE IF NOT EXISTS Equipment (
	object_id SERIAL PRIMARY KEY,
    object_name VARCHAR(255) NOT null,
	object_series VARCHAR(255) NOT null,
	obkect_gabaritType VARCHAR(255) NOT NULL,
	object_description TEXT,
	object_photo TEXT; -- Ссылка на место в компе(хранилище фото по пути)
);


CREATE TABLE IF NOT EXISTS Revievs (
    riviev_id SERIAL PRIMARY KEY,
    object_id INTEGER NOT NULL REFERENCES Equipment(object_id),
    user_id INTEGER NOT NULL REFERENCES Users(user_id),
	reviev_text TEXT,
    UNIQUE (object_id, user_id)
);


CREATE TABLE IF NOT EXISTS Book_history (
	boking_id SERIAL PRIMARY KEY,
	object_id INTEGER NOT NULL REFERENCES Equipment(object_id),
    user_id INTEGER NOT NULL REFERENCES Users(user_id),
	room_id INTEGER NOT NULL REFERENCES Rooms(room_id),
	data_book DATE NOT NULL
	UNIQUE (object_id, user_id, room_id, data_book)
);


CREATE TABLE IF NOT EXISTS Occupancy (
    key_id SERIAL PRIMARY KEY,
    object_id INTEGER NOT NULL REFERENCES Equipment(object_id),
    user_id INTEGER NOT NULL REFERENCES Users(user_id),
    room_id INTEGER NOT NULL REFERENCES Rooms(room_id),
    dataa DATE NOT NULL,
    time_start TIMESTAMP NOT NULL,
    time_end TIMESTAMP NOT NULL,
    CONSTRAINT valid_time_range CHECK (time_end > time_start),
    UNIQUE (object_id, user_id, room_id, time_start, time_end)
);


CREATE TABLE IF NOT EXISTS Favorites (
    object_id INTEGER NOT NULL REFERENCES Equipment(object_id),
    user_id INTEGER NOT NULL REFERENCES Users(user_id),
    UNIQUE (object_id, user_id),
    PRIMARY KEY (object_id, person_id)
);