"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
from data.data_hhru import HeadHunterAPI
from data.config import connect

list_of_vacancies = HeadHunterAPI.load_vacancies_from_json()


class DBManager:
    @staticmethod
    def filling_in_the_database():
        """Записывает все найденные вакансии в базу данных PosgreSQL"""
        conn = psycopg2.connect(host=connect()[0], database='hhru_vacancy',
                                user=connect()[2], password=connect()[3])

        try:
            with (conn):
                with conn.cursor() as cur:
                    for item in range(0, len(list_of_vacancies)):
                        cur.execute("INSERT INTO vacancy(name_vacancy, employer_name, salary_from, salary_to, "
                                    "salary_currency, schedule_name, employment_name, snippet_requirement, "
                                    "snippet_responsibility, apply_alternate_url) "
                                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                    (list_of_vacancies[item]['name'], list_of_vacancies[item]['employer']['name'],
                                     list_of_vacancies[item]['salary']['from'], list_of_vacancies[item]['salary']['to'],
                                     list_of_vacancies[item]['salary']['currency'],
                                     list_of_vacancies[item]['schedule']['name'],
                                     list_of_vacancies[item]['employment']['name'],
                                     list_of_vacancies[item]['snippet']['requirement'],
                                     list_of_vacancies[item]['snippet']['responsibility'],
                                     list_of_vacancies[item]['apply_alternate_url']))

        except psycopg2.errors.UniqueViolation as error:
            print(error)

        finally:
            conn.close()

    @staticmethod
    def get_companies_and_vacancies_count():
        """Получает список всех компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect(host=connect()[0], database='hhru_vacancy',
                                user=connect()[2], password=connect()[3])

        try:
            with (conn):
                with conn.cursor() as cur:

                    cur.execute("SELECT employer_name, COUNT(name_vacancy) FROM vacancy GROUP BY employer_name "
                                "ORDER BY COUNT(name_vacancy) DESC")

                    rows = cur.fetchall()
                    for row in rows:
                        print(row)

        except psycopg2.errors.UniqueViolation as error:
            print(error)

        finally:
            conn.close()

    @staticmethod
    def get_all_vacancies():
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на
        вакансию."""
        conn = psycopg2.connect(host=connect()[0], database='hhru_vacancy',
                                user=connect()[2], password=connect()[3])

        try:
            with (conn):
                with conn.cursor() as cur:
                    cur.execute("SELECT employer_name, name_vacancy, salary_from, salary_to, apply_alternate_url "
                                "FROM vacancy ")

                    rows = cur.fetchall()
                    for row in rows:
                        print(row)

        except psycopg2.errors.UniqueViolation as error:
            print(error)

        finally:
            conn.close()

    @staticmethod
    def get_avg_salary():
        """Получает среднюю зарплату по вакансиям."""
        conn = psycopg2.connect(host=connect()[0], database='hhru_vacancy',
                                user=connect()[2], password=connect()[3])

        try:
            with (conn):
                with conn.cursor() as cur:
                    cur.execute("SELECT AVG(salary_from), AVG(salary_to) FROM vacancy")

                    rows = cur.fetchall()
                    for row in rows:
                        print(row)

        except psycopg2.errors.UniqueViolation as error:
            print(error)

        finally:
            conn.close()

    @staticmethod
    def get_vacancies_with_higher_salary():
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = psycopg2.connect(host=connect()[0], database='hhru_vacancy',
                                user=connect()[2], password=connect()[3])

        try:
            with (conn):
                with conn.cursor() as cur:
                    cur.execute("SELECT employer_name, name_vacancy, salary_from, salary_to, apply_alternate_url "
                                "FROM vacancy WHERE salary_from > (SELECT AVG(salary_from) FROM vacancy)")

                    rows = cur.fetchall()
                    for row in rows:
                        print(row)

        except psycopg2.errors.UniqueViolation as error:
            print(error)

        finally:
            conn.close()

    @staticmethod
    def get_vacancies_with_keyword(keyword: str = 'Python'):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        conn = psycopg2.connect(host=connect()[0], database='hhru_vacancy',
                                user=connect()[2], password=connect()[3])

        try:
            with (conn):
                with conn.cursor() as cur:
                    cur.execute(f"SELECT employer_name, name_vacancy, salary_from, salary_to, apply_alternate_url "
                                f"FROM vacancy WHERE name_vacancy LIKE '%{keyword}%'")

                    rows = cur.fetchall()
                    for row in rows:
                        print(row)

        except psycopg2.errors.UniqueViolation as error:
            print(error)

        finally:
            conn.close()
