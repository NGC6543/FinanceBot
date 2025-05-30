import sqlite3
import datetime


class FinanceDb:

    def __init__(self) -> None:
        ...

    # def create_cursor(self):
    #     con = sqlite3.connect('finance.db')
    #     cur = con.cursor()
    #     return cur

    def create_table(self):
        try:
            with sqlite3.connect('finance.db') as con:
                cur = con.cursor()
                cur.execute("""CREATE TABLE IF NOT EXISTS finance (
                    id INTEGER PRIMARY KEY,
                    text text NOT NULL,
                    money REAL NOT NULL,
                    category VARCHAR(50),
                    add_date DATE
                );""")
                con.commit()
        except sqlite3.OperationalError as e:
            print('Failed to create tables:', e)

    def adding_data(self, text, money, category):
        try:
            with sqlite3.connect('finance.db') as con:
                cur = con.cursor()
                get_time = datetime.datetime.now()
                cur.execute(
                    """INSERT INTO finance(text, money, category, add_date)
                    values(?, ?, ?, ?)""", (text, money, category, get_time)
                )
                con.commit()
        except sqlite3.OperationalError as e:
            print('Failed to add data into table', e)

    def retrive_data(self):
        try:
            with sqlite3.connect('finance.db') as con:
                cur = con.cursor()
                cur.execute(
                    'SELECT text, money, category, add_date FROM finance'
                )
                rows = cur.fetchall()
                return rows
        except sqlite3.OperationalError as e:
            print('Failed to retrive data from table', e)
