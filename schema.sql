CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE
);

CREATE TABLE IF NOT EXISTS finance (
                    id SERIAL PRIMARY KEY,
                    text text NOT NULL,
                    money REAL NOT NULL,
                    category VARCHAR(50),
                    add_date DATE,
                    user_id BIGINT,
                    FOREIGN KEY(user_id) REFERENCES users(telegram_id));
