import os
import datetime
from collections import namedtuple

import psycopg2
from dotenv import load_dotenv

load_dotenv()


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

DbDateData = namedtuple(
    'DbDateData',
    'id, text, money, category, add_date'
)
DbCategoryData = namedtuple('DbCategoryData', 'money, category')


class FinanceDb:
    """Main class for using DB."""

    def connect_db(self):
        """Create connection with db."""
        conn = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB'),
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            port=os.getenv('DB_PORT'),
        )
        return conn

    def create_db(self):
        """Create tables in db."""
        db = self.connect_db()
        with db.cursor() as cursor:
            cursor.execute(open("schema.sql", "r", encoding='utf-8').read())
        db.commit()
        db.close()

    def getting_data_from_db(self, query, nmtuple=DbDateData):
        """General function for getting data from db query."""
        rows = []
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                cur.execute(*query)
                rows = cur.fetchall()
                tuple_rows = (
                    nmtuple._make(row) for row in rows
                )
                return tuple_rows
        except psycopg2.OperationalError as error:
            print('Failed to retrive data from table', error)
        return rows

    def adding_data(self, text, money, category, user_id):
        """Add data in db."""
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                get_time = datetime.datetime.now()
                cur.execute(
                    "SELECT 1 FROM users WHERE telegram_id = (%s)",
                    (user_id,)
                )
                if not cur.fetchone():
                    cur.execute(
                        "INSERT INTO users (telegram_id) VALUES (%s)",
                        (user_id,)
                    )

                cur.execute(
                    """INSERT INTO finance(text, money, category,
                    add_date, user_id)
                    values(%s , %s , %s, %s, %s)""", (
                        text, money, category, get_time, user_id
                    )
                )
                con.commit()
        except psycopg2.OperationalError as error:
            print('Failed to add data into table', error)

    def retrive_data_by_date(self, date, user_id):
        """Retrive data by date."""
        query_all_date =  """SELECT id, text, money, category,
                        add_date::timestamp
                        FROM finance
                        WHERE user_id = %s""", (user_id,)
        get_date = DATE_RANGE_CHOICES_DICT.get(date)
        if not get_date:
            return self.getting_data_from_db(query_all_date, DbDateData)
        else:
            start_date, end_date = get_date
            query_certain_date = """SELECT id, text, money, category,
            add_date::timestamp
            FROM finance
            WHERE add_date::timestamp
            BETWEEN %s AND %s AND user_id = %s""", (
                start_date.isoformat(),
                end_date.isoformat(),
                user_id
            )
            return self.getting_data_from_db(query_certain_date)

    def retrive_data_by_category(self, user_id):
        """Retrive data by category."""
        start_date, end_date = first_day_this_month, today
        query_category = """SELECT SUM(money), category
                    FROM finance
                    WHERE add_date::timestamp
                    BETWEEN %s AND %s AND user_id = %s
                    GROUP BY category;""", (
                        start_date.isoformat(),
                        end_date.isoformat(),
                        user_id,
                    )
        return self.getting_data_from_db(
            query_category,
            nmtuple=DbCategoryData
        )

    def retrive_data_by_certain_word(self, user_id, user_word):
        """Retrive data by a certain word."""
        start_date, end_date = first_day_this_month, today
        query_certain_word = """SELECT id, text, money, category,
                    add_date::timestamp
                    FROM finance
                    WHERE add_date::timestamp
                    BETWEEN %s AND %s AND user_id = %s
                    AND text ILIKE %s;""", (
                        start_date.isoformat(),
                        end_date.isoformat(),
                        user_id,
                        '%' + user_word + '%',
                    )
        return self.getting_data_from_db(query_certain_word)

    def delete_record_by_id(self, record_id, user_id):
        """Delete data by id."""
        try:
            with self.connect_db() as con:
                cur = con.cursor()
                cur.execute(
                    """SELECT 1 FROM finance
                    WHERE id = %s AND user_id = %s""",
                    (record_id, user_id)
                )
                if not cur.fetchone():
                    return False
                cur.execute(
                    """DELETE FROM finance
                    WHERE id = %s""", (record_id,))
                con.commit()
        except psycopg2.OperationalError as error:
            print('Failed to delete data from table', error)
        return True
