import sqlite3
import datetime
from collections import namedtuple


today = datetime.date.today()
first_day_this_month = today.replace(day=1)
first_day_last_month = (
    first_day_this_month - datetime.timedelta(days=1)
).replace(day=1)
last_day_last_month = first_day_this_month - datetime.timedelta(days=1)

DATE_RANGE_CHOICES_DICT = {
    'За сегодня': (today, today),
    'За этот месяц': (first_day_this_month, today),
    'За прошлый месяц': (first_day_last_month, last_day_last_month),
    'За всё время': None,
}

DB_DATE_DATA = namedtuple('DB_DATE_DATA', 'text, money, category, add_date')
DB_CATEGORY_DATA = namedtuple('DB_CATEGORY_DATA', 'money, category')


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
            print('Failed to create table:', e)

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

    def retrive_data_by_date(self, date):
        rows = []
        try:
            with sqlite3.connect('finance.db') as con:
                cur = con.cursor()
                get_date = DATE_RANGE_CHOICES_DICT.get(date)
                if not get_date:
                    cur.execute(
                        'SELECT text, money, category, add_date FROM finance'
                    )
                    rows = cur.fetchall()
                else:
                    start_date, end_date = get_date
                    cur.execute(
                        """SELECT text, money, category, add_date
                        FROM finance
                        WHERE date(add_date)
                        BETWEEN ? AND ?""", (
                            start_date.isoformat(), end_date.isoformat()
                        )
                    )
                    rows = cur.fetchall()
                tuple_rows = (DB_DATE_DATA._make(row) for row in rows)
                return tuple_rows
        except sqlite3.OperationalError as e:
            print('Failed to retrive data from table', e)
        return rows

    def retrive_data_by_category(self):
        rows = []
        try:
            with sqlite3.connect('finance.db') as con:
                cur = con.cursor()
                start_date, end_date = first_day_this_month, today
                cur.execute(
                    """SELECT SUM(money), category
                    FROM finance
                    WHERE date(add_date)
                    BETWEEN ? AND ?
                    GROUP BY category;""", (
                        start_date.isoformat(), end_date.isoformat()
                    )
                )
                rows = cur.fetchall()
                tuple_rows = (
                    DB_CATEGORY_DATA._make(row) for row in rows
                )
                return tuple_rows
        except sqlite3.OperationalError as e:
            print('Failed to retrive data from table', e)
        return rows
