from collections import defaultdict
import psycopg2

from migration import Migration


class MostLovedMigration(Migration):
    def __init__(self):
        super().__init__()

    def connect_db(self):
        return super().connect_db()

    def get_data(self, query):
        return super().get_data(query)

    def get_ocurrencies(self, data, have_worked_with, wanna_work_with, dreaded_count):
        for tuple in data:
            # wanna work with (2nd row)
            seen = set()
            if tuple[1][0] != 'NA':
                for item in tuple[1]:
                    item = item.lower()
                    seen.add(item)
                    wanna_work_with[item] += 1
            
            # have worked with (1st row)
            if tuple[0][0] != 'NA':
                for item in tuple[0]:
                    item = item.lower()
                    have_worked_with[item] += 1
                    if item not in seen:
                        dreaded_count[item] += 1
                    else:
                        seen.remove(item)

    def execute_insert_query(self, data, question_id, year):
        have_worked_with = defaultdict(int)
        wanna_work_with = defaultdict(int)
        dreaded_count = defaultdict(int)

        self.get_ocurrencies(data, have_worked_with, wanna_work_with, dreaded_count)

        try:
            cursor = self.conn.cursor()
            
            cursor.execute("INSERT INTO public.year (question_id, year) \
                VALUES (%s, %s) RETURNING id", (question_id, year))
            year_id = cursor.fetchone()[0]

            for item in have_worked_with:
                total = have_worked_with[item]
                loved = total - dreaded_count[item]
                cursor.execute("INSERT INTO public.answer (year_id, name, total_responses, num_responses) \
                    VALUES (%s, %s, %s, %s)", (year_id, item, total, loved))
            print('Done 👍')
        except (psycopg2.Error):
            print('error executing the insert query')
            return psycopg2.Error
        finally:
            cursor.close()

    def insert_into_db(self, question_id, from_year, to_year, nameCol2021_1, nameCol2021_2, nameCol2020_1, nameCol2020_2):
        for year in range(from_year, to_year+1):
            data = []
            if year <= 2020:
                data = self.get_data(f"SELECT string_to_array({nameCol2020_1}, ';') AS w1, string_to_array({nameCol2020_2}, ';') AS w2 FROM surveys.survey{year}")
            else:
                data = self.get_data(f"SELECT string_to_array({nameCol2021_1}, ';') AS w1, string_to_array({nameCol2021_2}, ';') AS w2 FROM surveys.survey{year}")

            self.execute_insert_query(data, question_id, year)


if __name__ == '__main__':
    m = MostLovedMigration()
    # m.insert_into_db(6, 2018, 2022, 'DatabaseHaveWorkedWith', 'DatabaseWantToWorkWith', 'databaseworkedwith', 'databasedesirenextyear')
