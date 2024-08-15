import sqlite3
import os

# Путь к базе данных SQLite
db_path = 'users.db'

# Папка для сохранения извлечённых файлов
output_folder = 'uploads'
os.makedirs(output_folder, exist_ok=True)

# Подключение к базе данных
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Извлечение данных из таблицы request
cursor.execute("SELECT file_data, file_name FROM requests")
rows = cursor.fetchall()

for row in rows:
    file_data, file_name = row

    # Путь для сохранения файла
    file_path = os.path.join(output_folder, file_name)

    # Запись данных в файл
    with open(file_path, 'wb') as file:
        file.write(file_data)

# Закрытие подключения к базе данных
conn.close()
