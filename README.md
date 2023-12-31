# Документация по созданию датасета на основе данных с сайта НИТУ МИСиС

## Введение


Эта документация предоставляет инструкции по созданию датасета на основе данных, полученных с сайта НИТУ МИСиС. Процесс включает в себя сбор html-разметок и текстовых данных с веб-страниц университета, подготовку и очистку данных, а также формирование csv-файла - итого датасета, который содержит в себе вопросы и ответы об универе.

## Шаги по созданию датасета

### 1. Определение списка страниц
- Возьмите главную страницу сайта университета в МИСиС https://misis.ru/
- С использованием генераторов карт сайтов определите список страниц, с которыми предстоит работать.
Пример одного из множества генераторов: https://misis.ru/

### 2. Парсинг страниц и сохранение данных
- Запустите скрипт "Html_Txt_Extraction" для получения и парсинга html-разметок по страницам из списка.
- Скрипт создаёт две папки: "htmls" - с файлами разметок, и "txts" - с текстовыми данными, полученными в результате парсинга файлов первой папки.

### 3. Подготовка данных - First Stage
- Запустите скрипт "1_stage_Prepare_Data" для очистки данных. Скрипт убирает табуляцию, повторяющие блоки с сайта и т.д.
- В результате будут созданы обновленные txt-файлы с очищенными данными в папке "Data/htmls_and_txts/txts_clean".

### 4. Создание csv-файла - Second Stage
- Запустите скрипт "2_step_Create_Input_Data" для создание csv-файла Input.csv.
Каждая строка представляет собой запрос к модели GPT. Если текст превышает ограниченное количество токенов (4000), предусмотрено разделение на чанки.

### 5. Запросы ChatGPT

#### Описание

Данный скрипт предназначен для использования ChatGPT с целью создания вопросов на основе текста, полученного из датасета. В результате каждого запроса ожидается получение ответа, который структурированно предоставит информацию, соответствующую содержанию страницы.

#### 5.1 Запуск скрипта через API
- Запустите скрипт 3_step_GPT_Request.
- Скрипт обращается к чату с приведенным промптом:
```python
"Представь, что ты специалист в области data science. Ты получаешь сырой текст"
+ str(row[1]["text"]) +
"и тебе необходимо на основе информации придумать вопросы, на который содержимое страницы может дать краткий, чётко структурированный ответ. Пришли мне выход в формате ""Вопрос:.... Ответ:..."
```
- После каждого запроса обновляются данные в csv.
- Скрипт проверяет, что результат ответа, который должен был записать ChatGPT, не пустой, и не обрабатывает его повторно.
- Обратите внимание на ограничения: при слишком больших запросах возможна ошибка. Существует лимит на количество запросов в час (приблизительно +- 200).

**Важно**

Скрипт может потребовать нескольких запусков для обработки всех данных. Он автоматически проверяет, был ли получен ответ от ChatGPT, и избегает повторной обработки уже обработанных данных.

#### 5.2 Запросы ChatGPT через интерфейс (Альтернативный шаг)
Если API не работает, то можно запустить программного робота, который будет взаиможействовать с ChatGPT через интрефейс
- Скачайте приложение PIX RPA.
- Откройте Google Chrome.
- Запустите скрипт GPT_interface.

Для использования этого подхода требуется лицензия PIX RPA.

### 6. Сбор датасета вопросы-ответы

После полной обработки файла Input, когда для каждой строки были созданы ответы и вопросы, необходимо выполнить парсинг результатов. Для этого используется скрипт 4_step_Final_DataSet. В результате выполнения скрипта будет сформирован файл 4_step_Final_DataSet.

- Запустите скрипт 4_step_Final_DataSet.
- По завершению выполнения скрипта будет создан файл 4_step_Final_DataSet.
- В этом файле будут содержаться окончательные результаты, включая сопоставление вопросов и ответов для каждой строки данных.

Убедитесь, что все предыдущие шаги были успешно выполнены перед запуском этого скрипта. В противном случае результаты могут быть неполными или содержать ошибки.

## Завершение
После завершения этих шагов у вас будет подготовленный датасет, который можно использовать для обучения моделей
![image](https://github.com/Committed-Soriti/Misis-Dataset/assets/128974407/641c1794-6de4-455f-85db-c89fbaf9ae9c)

Ссылка на датасет от 07.12.2023 - https://disk.yandex.ru/d/EPx28qzdIillHg

