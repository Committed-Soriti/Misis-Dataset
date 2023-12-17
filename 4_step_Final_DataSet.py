import pandas as pd
import re

# Чтение CSV-файла
input_csv_path = 'Data/Input.csv'
output_csv_path = 'Data/DataSet_Final.csv'

# Шаблон регулярного выражения
pattern = r"Вопрос: (.+?)\nОтвет: (.+?)(?=\n\n|$)"

# Создание пустого DataFrame для нового CSV-файла
output_columns = ['№', 'Ссылка', 'Заголовок страницы', 'Вопрос', 'Ответ']
output_table = pd.DataFrame(columns=output_columns)

# Чтение данных из исходного CSV-файла и заполнение новой таблицы
input_table = pd.read_csv(input_csv_path,sep=',', encoding='UTF32')
number = 0

for row in input_table.iterrows():

    temp_text = str(row[1]["result"])
    # Поиск совпадений
    matches = re.finditer(pattern,temp_text , re.MULTILINE | re.DOTALL)

    # Обработка совпадений
    for match in matches:
        #Получаем вопрос
        question = match.group(1)
        #Получаем ответ
        answer = match.group(2)
        link = row[1]["link"]
        title = row[1]["title"]
        number = number+1

        # Добавление данных в новую таблицу
        row_data = {'№': number,
            'Ссылка': link,
            'Заголовок страницы': title,
            'Вопрос': question,
            'Ответ': answer}
        output_table = pd.concat([ output_table, pd.DataFrame([row_data])], ignore_index=True)

# Сохранение новой таблицы в CSV-файл
output_table.to_csv(output_csv_path, index=False, encoding='UTF32')

print(f"Новый CSV-файл создан: {output_csv_path}")
