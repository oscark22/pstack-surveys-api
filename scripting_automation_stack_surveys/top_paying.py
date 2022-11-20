from collections import defaultdict
from operator import truediv
import psycopg2

from migration import Migration


class TopPayingMigration(Migration):
    def connect_db(self):
        return super().connect_db()
    
    def get_data(self, query):
        return super().get_data(query)

    def get_ocurrencies(self, data, have_worked_with):
        for tuple in data:
            for item in tuple[0]:
                have_worked_with[item] += 1

    def execute_insert_query(self, data, question_id, year):
        have_worked_with = defaultdict(int)
        self.getocurrencies(have_worked_with)

        try:
            conn = self.connect_db()
            conn.autocommit = True

            cursor = conn.cursor()
            cursor.execute('INSERT INTO public.year ()')

            pass
        except (psycopg2.Error):
            pass

    def insert_into_db(self, question_id, from_year, to_year):
        return super().insert_into_db(from_year, to_year)


if __name__ == '__main__':
    pass
