from abc import ABC, abstractmethod
import psycopg2
import os


DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')


class Migration(ABC):
    def __init__(self):
        self.conn = self.connect_db()
        self.conn.autocommit = True
        
    def connect_db(self):
        return psycopg2.connect(
            user=DB_USER,
            password=DB_PASS,
            host="localhost",
            port="5432",
            database="stack-db"
        )

    def get_data(self, query):
        data = []
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
        except (psycopg2.Error):
            print('error getting data')
            return psycopg2.Error
        finally:
            cursor.close()
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
