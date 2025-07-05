CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER
);

CREATE TABLE IF NOT EXISTS finance (
                    id INTEGER PRIMARY KEY,
                    text text NOT NULL,
                    money REAL NOT NULL,
                    category VARCHAR(50),
                    add_date DATE,
                    user_id INTEGER,
                    FOREIGN KEY(user_id) REFERENCES user(telegram_id));
