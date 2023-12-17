import os
import pandas as pd
import re

def get_file_list(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def create_empty_table(headers):
    return pd.DataFrame(columns=headers)

def split_text(text, chunk_size):
    parts = []

    for i in range(0, len(text), chunk_size):
        length = min(chunk_size, len(text) - i)
        parts.append(text[i:i + length])

    return parts

def fill_table_with_data(table, directory_txt, file_list_txt, directory_html, file_list_html):
    for file in file_list_txt:
        # Получаем имя файла без расширения и заменяем "_clean" на пустую строку
        file_base_name = os.path.splitext(os.path.basename(file))[0].replace('_clean', '')
        # Ищем файл с совпадающим именем (без расширения) в списке html_files
        matching_html_file = next((html_file for html_file in file_list_html if os.path.splitext(html_file)[0] == file_base_name), None)
        if matching_html_file:
            # Получаем полный путь к найденному HTML файлу
            full_html_path = os.path.join(directory_html, matching_html_file)
            #Считываем HTML файл
            with open(full_html_path, 'r', encoding='utf-8') as f:
                html_text = f.read()
                try:
                    #Получаем ссылку страницы
                    link_value = re.search(r'rel="canonical" href="(.*?)"><link', html_text).group(1).replace("rel=""canonical"" href=","").replace("><link","")
                    #Получаем заголовок страницы
                    title_value = re.search(r'<title>(.*?)<\/title>', html_text).group(1).replace("<title>","").replace("</title>","")
                except Exception as e:
                    link_value = ""
                    title_value = ""

        else:
            print('HTML файл не найден')
            link_value = ""
            title_value = ""
        file_path = os.path.join(directory_txt, file)


        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            # Получаем имя файла без расширения, удаляем "website_" и "_clean.txt", чтобы получить номер
            file_number = os.path.splitext(os.path.basename(file_path))[0].replace("website_", "").replace("_clean", "")
            #У ChatGPT есть органичение на колиечство символов в запроск + надо учесть символы в самомо Промпте
            chunk_size = 4000
            result_parts = split_text(text, chunk_size)
            #Цикл по всем частам текста
            for index,part in enumerate(result_parts):
                #Если по 1 файлу несколько частей, то указываем номер части
                if len(result_parts) > 1:
                    file_number_temp = f"{file_number}_{index + 1}"
                else:
                    file_number_temp = file_number
                # Добавляем строку с текстом в таблицу
                row_data = {'number': file_number_temp, 'link': link_value, 'title': title_value, 'text': text,'result':""}
                table = pd.concat([table, pd.DataFrame([row_data])], ignore_index=True)
    return table

directory_txt = 'Data/htmls_and_txts/txts_clean'
directory_html = 'Data/htmls_and_txts/htmls'
headers = ['number', 'link', 'title', 'text','result']

# Создаем пустую таблицу
table = create_empty_table(headers)

#Получаем список файлов и сортируем по возрастанию индекса
file_list_txt = sorted(get_file_list(directory_txt), key=lambda x: int(os.path.splitext(x.replace("website_", "").replace("_clean.txt", ""))[0]))
file_list_html = get_file_list(directory_html)

# Заполняем таблицу данными из файлов
table = fill_table_with_data(table, directory_txt, file_list_txt, directory_html, file_list_html)

# Указываем путь к файлу CSV
csv_path = 'Data/Input.csv'

print("Файлы в первой директории:", file_list_txt)
print("Файлы во второй директории:", file_list_html)


# Записываем таблицу в CSV файл
table.to_csv(csv_path, index=False, encoding='UTF32')
