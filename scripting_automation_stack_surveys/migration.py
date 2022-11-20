from abc import ABC, abstractmethod
import psycopg2
import os


DB_NAME = os.environ.get('DATABASE_NAME')
DB_PASS = os.environ.get('DATABASE_PASSWORD')


class Migration(ABC):
    def __init__(self):
        self.conn = self.connect_db()

    def connect_db(self):
        return psycopg2.connect(
            user=DB_NAME,
            password=DB_PASS,
            host="localhost",
            port="5432",
            database="stack_db"
        )

    def get_data(self, query):
        data = []
        # connect to postgresql
        try:
            self.conn.autocommit = True

            cursor = self.conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
        except (psycopg2.Error):
            print('error getting data')
            return psycopg2.Error
        finally:
            # close conn
            if self.conn:
                cursor.close()
                self.conn.close()
        return data

    @abstractmethod
    def get_ocurrencies(data, have_worked_with, wanna_work_with, dreaded_count):
        pass

    @abstractmethod
    def execute_insert_query(data, question_id, year):
        pass

    @abstractmethod
    def insert_into_db(question_id, from_year, to_year):
        pass
