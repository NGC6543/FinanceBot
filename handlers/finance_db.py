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

DB_DATE_DATA = namedtuple(
    'DB_DATE_DATA',
    'id, text, money, category, add_date'
)
DB_CATEGORY_DATA = namedtuple('DB_CATEGORY_DATA', 'money, category')


class FinanceDb:

    def connect_db(self):
        """Function for creating connection with db."""
        conn = sqlite3.connect('finance.db')
        return conn

    def create_db(self):
        """Function for creating tables in db."""
        db = self.connect_db()
        with open('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        db.close()

    def adding_data(self, text, money, category, user_id):
        """Function for adding data in db."""
        try:
            with sqlite3.connect('finance.db') as con:
                cur = con.cursor()
                get_time = datetime.datetime.now()
                cur.execute(
                    "SELECT 1 FROM user WHERE telegram_id = ?", (user_id,)
                )
                if not cur.fetchone():
                    cur.execute(
                        "INSERT INTO user (telegram_id) VALUES (?)", (user_id,)
                    )

                cur.execute(
                    """INSERT INTO finance(text, money, category,
                    add_date, user_id)
                    values(?, ?, ?, ?, ?)""", (
                        text, money, category, get_time, user_id
                    )
                )
                con.commit()
        except sqlite3.OperationalError as e:
            print('Failed to add data into table', e)

    def retrive_data_by_date(self, date, user_id):
        """Function for retrieving data by date."""
        rows = []
        try:
            with sqlite3.connect('finance.db') as con:
                cur = con.cursor()
                get_date = DATE_RANGE_CHOICES_DICT.get(date)
                if not get_date:
                    cur.execute(
                        """SELECT id, text, money, category, datetime(add_date)
                        FROM finance
                        WHERE user_id = (?)""", (user_id,)
                    )
                    rows = cur.fetchall()
                else:
                    start_date, end_date = get_date
                    cur.execute(
                        """SELECT id, text, money, category, datetime(add_date)
                        FROM finance
                        WHERE date(add_date)
                        BETWEEN ? AND ? AND user_id = (?)""", (
                            start_date.isoformat(),
                            end_date.isoformat(),
                            user_id
                        )
                    )
                    rows = cur.fetchall()
                tuple_rows = (DB_DATE_DATA._make(row) for row in rows)
                return tuple_rows
        except sqlite3.OperationalError as e:
            print('Failed to retrive data from table', e)
        return rows

    def retrive_data_by_category(self, user_id):
        """Function for retrieving data by category."""
        rows = []
        try:
            with sqlite3.connect('finance.db') as con:
                cur = con.cursor()
                start_date, end_date = first_day_this_month, today
                cur.execute(
                    """SELECT SUM(money), category
                    FROM finance
                    WHERE date(add_date)
                    BETWEEN ? AND ? AND user_id = (?)
                    GROUP BY category;""", (
                        start_date.isoformat(),
                        end_date.isoformat(),
                        user_id,
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

    def delete_record_by_id(self, record_id, user_id):
        """Function for deleting data by id."""
        try:
            with sqlite3.connect('finance.db') as con:
                cur = con.cursor()
                check_record = cur.execute(
                    """SELECT 1 FROM finance
                    WHERE id = (?) AND user_id = (?)""",
                    (record_id, user_id)
                )
                if not check_record.fetchone():
                    return False
                cur.execute(
                    """DELETE FROM finance
                    WHERE id = (?)""", (record_id,))
                con.commit()
        except sqlite3.OperationalError as e:
            print('Failed to delete data from table', e)
        return True
