from dotenv import load_dotenv
import psycopg2
import sys
import os

load_dotenv()


class Database():
    def __init__(self) -> None:
        self.conn = self.connect_db()

    def connect_db(self):
        try:
            conn = psycopg2.connect(
                user= os.environ.get("DATABASE_USER"),
                password= os.environ.get("DATABASE_PASSWORD"),
                host= os.environ.get("DATABASE_HOST"),
                port= os.environ.get("DATABASE_PORT"),
                database= os.environ.get("DATABASE_NAME")
            )
            conn.autocommit = True
        except (psycopg2.OperationalError) as e:
            print("could not connect to db")
            sys.exit(1)
        return conn

    def read_question_data(self, question_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, year, total_responses FROM public.year WHERE question_id = %s", (question_id,))

            data_by_year = {}
            years = cursor.fetchall()

            # Put the data in a dict w/year by key.
            for id, year, total_responses in years:
                cursor.execute("SELECT name, num_responses, total_responses FROM public.answer WHERE year_id = %s", (id,))
                data_by_year[year] = {
                    'all_responses': total_responses,
                    'data': {}
                }
                for name, num_responses, total_responses in cursor.fetchall():
                    data_by_year[year]['data'][name] = {
                        'num_responses': num_responses,
                        'total_responses': total_responses
                    }
            return data_by_year
        except (psycopg2.OperationalError) as e:
            print("could not fetch data from db")
            sys.exit(1)
        finally:
            cursor.close()

    def read_question_data_with_limit(self, question_id, limit):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, year, total_responses FROM public.year WHERE question_id = %s", (question_id,))

            data_by_year = {}
            years = cursor.fetchall()

            # Put the data in a dict w/year by key.
            for id, year, total_responses in years:
                cursor.execute("SELECT name, num_responses, total_responses FROM public.answer WHERE year_id=%s ORDER \
                    BY num_responses::decimal/total_responses DESC LIMIT %s", (id, limit))
                data_by_year[year] = {
                    'all_responses': total_responses,
                    'data': {}
                }
                for name, num_responses, total_responses in cursor.fetchall():
                    data_by_year[year]['data'][name] = {
                        'num_responses': num_responses,
                        'total_responses': total_responses
                    }
            return data_by_year
        except (psycopg2.OperationalError) as e:
            print("could not fetch data from db")
            sys.exit(1)
        finally:
            cursor.close()

    def read_comments_data(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT text FROM comments.comment")
            return cursor.fetchall()
        except (psycopg2.OperationalError) as e:
            print("could not fetch data from db")
            sys.exit(1)
        finally:
            cursor.close()

    def read_recent_comments(self, limit):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM comments.comment ORDER BY creation DESC LIMIT %s", (limit,))
            return cursor.fetchall()
        except (psycopg2.OperationalError) as e:
            print("could not fetch data from db")
            sys.exit(1)
        finally:
            cursor.close()

    def create_new_comment(self, user_id, text):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO comments.comment (user_id, text, creation, last_modification) VALUES (%s, %s, NOW(), NOW())", (user_id, text))
            return "Data inserted successfully"
        except (psycopg2.OperationalError) as e:
            print("could not create comment successfully")
            sys.exit(1)
        finally:
            cursor.close()

    def update_comment(self, comment_id, text):
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE comments.comment SET text=%s, last_modification=NOW() WHERE id=%s", (text, comment_id))
            return "Comment updated successfully"
        except (psycopg2.OperationalError) as e:
            print("could not update comment successfully")
            sys.exit(1)
        finally:
            cursor.close()

    def delete_comment(self, comment_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM comments.comment WHERE id=%s", (comment_id,))
            return "Comment deleted successfully"
        except (psycopg2.OperationalError) as e:
            print("could not delete comment from db")
            sys.exit(1)
        finally:
            cursor.close()


if __name__ == '__main__':
    db = Database()
    # print(db.fetch_question_data_with_limit(6, 10))
