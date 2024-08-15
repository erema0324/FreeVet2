import sqlite3
from sql import init_db


def drop_all_table(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Получаем список всех пользовательских таблиц, исключая системные
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = c.fetchall()

    # Удаляем все пользовательские таблицы
    for table_name in tables:
        c.execute(f"DROP TABLE IF EXISTS {table_name[0]}")

    conn.commit()
    conn.close()
    init_db()


drop_all_table('users.db')  # Замените на имя вашей базы данных

