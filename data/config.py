import psycopg2
import os


def connect():
    param = []
    path = os.path.join(os.path.dirname(__file__), 'database')

    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            param.append(line.rstrip('\n'))

    host = param[0][5:]
    database = param[1][9:]
    user = param[2][5:]
    password = param[3][9:]

    param = [host, database, user, password]

    return param


def create_base():
    conn = psycopg2.connect(host=connect()[0], database=connect()[1], user=connect()[2], password=connect()[3])
    cursor = conn.cursor()

    conn.autocommit = True

    try:
        cursor.execute("CREATE DATABASE hhru_vacancy")
        print("База данных успешно создана.\n")

        conn = psycopg2.connect(host=connect()[0], database="hhru_vacancy", user=connect()[2], password=connect()[3])

        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                        CREATE TABLE vacancy 
                        (
                            vacancy_id SERIAL,
                            name_vacancy varchar(100) NOT NULL,
                            employer_name varchar(100) NOT NULL,
                            salary_from int,
                            salary_to int,
                            salary_currency varchar(50),
                            schedule_name varchar(50),
                            employment_name varchar(50),
                            snippet_requirement text,
                            snippet_responsibility text,
                            apply_alternate_url text
                        )
                        """)

                print("Таблица успешно создана.")

        cursor.close()
        conn.close()

    except psycopg2.errors.DuplicateDatabase:
        print("База данных уже существует.")

    finally:
        cursor.close()
        conn.close()
