import os
import re
import json
import string
import logging
from typing import Optional
from datetime import datetime

from prettytable import PrettyTable

class KeywordColorFormatter(logging.Formatter):
    """
    Класс KeywordColorFormatter предоставляет форматирование логов
    с использованием цветов для выделения уровней логирования
    (DEBUG, INFO, WARNING, ERROR, CRITICAL) или ключевых слов в сообщениях.

    Атрибуты:
        COLORS (dict): Словарь, сопоставляющий уровни логирования
        с соответствующими ANSI-кодами цвета.

        RESET (str): ANSI-код для сброса цвета.
    """

    COLORS = {
        'DEBUG': '\033[36m',     # Голубой
        'INFO': '\033[32m',      # Зеленый
        'WARNING': '\033[33m',   # Желтый
        'ERROR': '\033[31m',     # Красный
        'CRITICAL': '\033[1;31m' # Жирный красный
    }
    RESET = '\033[0m'

    def format(self, record):
        levelname_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{levelname_color}{record.levelname}{self.RESET}"
        return super().format(record)

# Настройка логера
logger = logging.getLogger("keyword_color_logger")
handler = logging.StreamHandler()
formatter = KeywordColorFormatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Создание таблицы для удобного отображения данных
table = PrettyTable()

# Именования заголовков таблицы
table.field_names = [
    "ID",
    "Title",
    "Description",
    "Category",
    "Due_date",
    "Priority",
    "Status",
]

class Task:
    """
    Класс Task представляет модель данных для задачи.
    """

    def __init__(self, id: Optional[int] = None,
                 title: str = "", description: str = "",
                 category: str = "", due_date: str = "",
                 priority: str = "", status: str = ""):
        """
        Инициализация класса Task.

        Аргументы:
            id (Optional[int]): Уникальный идентификатор задачи.
            title (str): Заголовок задачи.
            description (str): Описание задачи.
            category (str): Категория задачи.
            due_date (str): Дата выполнения задачи в формате строки.
            priority (str): Приоритет задачи.
            status (str): Статус задачи.
        """
        self.id = None
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

class TaskManager():
    """Описание класса TaskManager"""

    # Вывод в формате "pretty print json" вместо таблицы.
    pretty_printed_JSON = False

    def __init__(self, path: str = "data/data.json"):
        """Инициализация класса"""
        self.path = path

    def format_tasks_table(self, tasks: list):
        """
        Формирует таблицу с задачами.

        Эта функция очищает таблицу и добавляет в неё строки с данными
        о задачах.

        Аргументы:
            tasks (list): Список задач, каждая из которых представлена как словарь
                          с ключами 'id', 'title', 'description', 'category', 
                          'due_date', 'priority', и 'status'.

        Возвращает:
            table: Обновлённая таблица с данными о задачах.
        """

        # Очистка всех строк из table.
        table.clear_rows()

        # Добавление задач в table через цикл.
        for task in tasks:
            table.add_row(
                [
                    task['id'],
                    task['title'],
                    task['description'],
                    task['category'],
                    task['due_date'],
                    task['priority'],
                    task['status']
                ]
            )
    
        return table

    def getting_task(self, value: str = "", option: str = ""):

        try:

            # Открытие файла data.json в режиме чтения и кодировкой UTF-8.
            with open(self.path, "r", encoding="UTF-8") as file:
                data = json.load(file)

            # Проверка, что если поле value пустое, а option указано, возникает ошибка.
            if value == "" and option:
                logger.error(
                    "При указании значения в поле \"option\" необходимо указать искомое значение "
                    "в поле \"value\""
                )
                return False
        
            # Проверка, что если value есть, а option пустое, возникает ошибка.
            if value and option == "":
                logger.error(
                    "При указании значения в поле \"value\" необходимо указать значение "
                    "в поле \"option\""
                )
                return False
        
            # Проверка, что если value и option пустые, возвращаются все данные.
            if value == "":
                if self.pretty_printed_JSON:
                    return json.dumps(data, indent=4, ensure_ascii=False)
                else:
                    return self.format_tasks_table(data)
            
            # Проверка, если значение есть, а option одно из допустимых значений,
            # затем выполняется валидация для указанного поля.
            if value and option in ["id", "category", "priority", "status"]:
                if not self.data_validation(value=value, column=str(option), intention="search"):
                    logger.error(f"Валидация для \"{option}\" не прошла.")
                    return False
            
                # Фильтрация задач, добавление задачи, где значение поля option равно value.
                new_data = [task for task in data if task[option] == value]

                # Если new_data не пусто, выводим данные в формате JSON или таблицы, 
                # если данных нет, возвращаем False.
                if new_data:
                    if self.pretty_printed_JSON:
                        return json.dumps(new_data, indent=4, ensure_ascii=False)
                    else:
                        return self.format_tasks_table(new_data)
                else:
                    logger.warning(f"Значение \"{value}\" не было найдено в файле.")
                    return False
        
            # Проверка, если option == "keywords" для поиска по ключевым словам.
            if option == "keywords":
                new_data = []
                for task in data:
                    if any(
                        value.lower() in str(task[field]).lower()
                        for field in ["title", "description", "category",
                                      "due_date", "priority", "status"]
                    ):
                        # Избежание дублирования
                        if task not in new_data:
                            new_data.append(task)
            
                # Если new_data не пусто, выводим данные в формате JSON или таблицы, 
                # если данных нет, возвращаем False.
                if new_data:
                    if self.pretty_printed_JSON:
                        return json.dumps(new_data, indent=4, ensure_ascii=False)
                    else:
                        return self.format_tasks_table(new_data)
                else:
                    logger.warning(f"Ключевого слова \"{value}\" не было найдено в таблице.")
                    return False
        
            # Проверка, если option == "due_date" для поиска по просроченной дате.
            if option == "due_date":
                # Получение нынешнего времени.
                now = datetime.today().date()

                # Добавление задач при условии что нынешняя дата больше или равна дате, 
                # указанной в задаче.
                new_data = [
                    task for task in data
                    if now.strftime("%Y-%m-%d") >= task["due_date"]
                ]

                # Если new_data не пусто, выводим данные в формате JSON или таблицы, 
                # если данных нет, возвращаем False.
                if new_data:
                    if self.pretty_printed_JSON:
                        return json.dumps(new_data, indent=4, ensure_ascii=False)
                    else:
                        return self.format_tasks_table(new_data)
                else:
                    logger.warning(f"Просроченных заданий не было найдено в таблице.")
                    return False
                
        except Exception as err:
            logger.critical(f"Произошла ошибка в функции \"{__name__}\": {err}")
            return False
    
            
    def data_validation(self, column: str = "", value: str = "", 
                        new_value: str = "", intention: str = "",
                        search_option: str = ""):
        """
        Функция валидации данных при добавлении или изменении задачи.

        Проверяет значения для различных полей задачи на соответствие типам данных,
        ограничениям по длине, допустимым значениям и формату даты.

        Аргументы:
            column (str): Имя столбца, которое проверяется.
            value (str): Значение, которое проверяется.
            new_value (str): Новое значение, если задача изменяется.
            intention (str): Намерение (add\change\delete)
            search_option (str): Опция для поиска (id, keywords, category, status)

        Возвращает:
            bool: True, если валидация прошла успешно, иначе False.
        """

        try:
            # Валидация intention на входящие значения
            if intention not in ["add", "change", "delete", "search"]:
                logger.error(
                    "Значение \"intention\" должно быть одним из значений: "
                    "\"add\", \"change\", \"delete\" или \"search\"."
                )
                return False
            
            # Валидация search_option, если это поиск
            if intention == "search":
                valid_search_options = ["id", "keywords", "category", "status"]
                if search_option and search_option not in valid_search_options:
                    logger.error(
                        "Значение в поле \"search_option\" должно быть одно из: "
                        f"{', '.join(valid_search_options)}."
                    )
                    return False
                
            # Проверка на пустые строки
            if intention != "search" and (
                not column.strip() or
                (isinstance(value, str) and not value.strip()) or
                not intention.strip()):
                logger.error(
                    "Значения \"column\", \"value\" и \"intention\" не могут быть пустыми."
                )
                return False
            
            # Валидация column, если это удаление
            if intention == "delete":
                if column not in ["id", "category"]:
                    logger.error(
                        "Значение \"column\" должно быть одним из значений: \"id\" или \"category\"."
                    )
                    return False

            # Проверка значения id на int или str
            if column == "id":
                # Проверка, что значение является числом (int) или строкой с цифрами
                if not (isinstance(value, int) or
                        (isinstance(value, str) and value.strip().isdigit())):
                    logger.error(
                        "Значение для \"id\" должно быть целым числом или строкой, содержащей только цифры."
                    )
                    return False
                
                # Если id типа (str), преобразование в число
                if isinstance(value, str):
                    value = int(value)
            
            # Валидация value, если это column == "priority"
            if column == "priority":
                if value not in ["Высокий", "Средний", "Низкий"]:
                    logger.error(
                        "При использовании опции \"priority\" в value должны передаваться "
                        "только значения \"Высокий\", \"Средний\" или \"Низкий\". "
                        f"Значение \"{value}\" не поддерживается."
                    )
                    return False
            
            # Валидация value, если это column == "status"
            if column == "status":
                if value not in ["Выполнена", "Не выполнена"]:
                    logger.error(
                        "При использовании опции \"status\" в value должны передаваться "
                        "только значения \"Выполнена\" или \"Не выполнена\". "
                        f"Значение \"{value}\" не поддерживается."
                    )
                    return False
                
            # Проверка на одинаковые значения value и new_value, 
            # если intention == "change"
            if intention == "change" and value == new_value:
                logger.error(
                    f"Значение \"{column}\" не может быть изменено с {value} на {new_value}, "
                    "поскольку значения одинаковые."
                )
                return False
            
            # Проверка входящих данных если намениние add или change
            if intention == "add" or intention == "change":
                # Проверка на цифры в начале строки если это не дата
                if value[0].isdigit() and column != "due_date":
                    logger.error(f"Значение \"{column}\" не может начинаться с цифры.")
                    return False
                
                # Проверка на специальные символы (кроме "due_date" и "description")
                if any(
                    char in string.punctuation for char in value
                    ) and column not in ["due_date", "description"]:
                    logger.error(
                        f"Значение \"{column}\" не должно содержать специальных символов."
                    )
                    return False
                
                # Проверка на допустимые значения для column
                valid_columns = ["title", "description", "category",
                                 "due_date", "priority", "status"]
                if column not in valid_columns:
                    logger.error(
                        "Неверное значение для \"column\". Допустимые значения:"
                        f"{', '.join(valid_columns)}."
                    )
                    return False
                
                # Проверка на длинну value если column == "title"
                if column == "title" and len(value) < 5:
                    logger.error("Поле \"title\" не может быть меньше 5 символов.")
                    return False
                
                # Проверка на длинну value если column == "description"
                if column == "description" and len(value) < 10:
                    logger.error("Поле \"description\" не может быть меньше 20 символов.")
                    return False
                
                # Проверка на длинну value если column == column == "category"
                if column == "category" and len(value) < 2:
                    logger.error("Поле \"category\" не может быть меньше 2 символов.")
                    return False
                
                # Проверка на допустимые значения для priority
                valid_priority_value = ["Низкий", "Средний", "Высокий"]
                if column == "priority" and value not in valid_priority_value:
                    logger.error(
                        "Поле \"priority\" должно быть одним из значений: "
                        "\"Низкий\", \"Средний\", \"Высокий\"."
                    )
                    return False
                
                # Проверка на допустимые значения для status
                if column == "status" and value not in ["Выполнена", "Не выполнена"]:
                    logger.error(
                        "Поле \"status\" должно быть одним из значений: "
                        "\"Выполнена\", \"Не выполнена\"."
                    )
                    return False
                
                # Проверка формата даты
                if column == "due_date":
                    # Шаблон даты
                    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
                    if not re.match(date_pattern, value.strip()):
                        logger.error(
                            f"{value} в поле \"due_date\" указано некорректно. "
                            "Ожидается формат YYYY-MM-DD."
                        )
                        return False
                    
                    # Проверка на будущую дату
                    now = datetime.today().date()
                    if now.strftime("%Y-%m-%d") > value.strip():
                        logger.error("Поле \"due_date\" не может содержать дату из прошлого.")
                        return False
                
                # Проверка на допустимые значения для column если intention == "search"
                valid_columns_search = ["id", "title", "description",
                                        "category", "due_date", "priority",
                                        "status"]
                if intention == "search" and column not in valid_columns_search:
                    logger.error(
                        "Неверное значение для \"column\". Допустимые значения: "
                        f"{', '.join(valid_columns_search)}."
                    )
                    return False

        except Exception as err:
            logger.critical(f"Произошла ошибка в функции \"{__name__}\": {err}")
            return False
        
        return True
    
    def add_task(self, title: str = "", description: str = "",
                 category: str = "", due_date: str = "",
                 priority: str = "", status: str = ""):
        
        """
        Функция для добавления новой задачи в систему.

        Она проверяет параметры задачи с помощью валидации, затем создает новый 
        объект задачи и добавляет его в файл данных (data.json). Каждое поле 
        задачи проходит проверку на соответствие допустимым значениям.

        Аргументы:
            title (str): Заголовок задачи.
            description (str): Описание задачи.
            category (str): Категория задачи.
            due_date (str): Дата выполнения задачи в формате YYYY-MM-DD.
            priority (str): Приоритет задачи ("Низкий", "Средний", "Высокий").
            status (str): Статус задачи ("Выполнена" или "Не выполнена").

        Возвращает:
            bool: True, если задача успешно добавлена, иначе False.
        """

        try:
            # Валидация title
            if not self.data_validation(
                column="title",
                value=title,
                intention="add"
                ):
                return False
            
            # Валидация description
            if not self.data_validation(
                column="description",
                value=description,
                intention="add"
                ):
                return False
            
            # Валидация category
            if not self.data_validation(
                column="category",
                value=category,
                intention="add"
                ):
                return False
            
            # Валидация due_date
            if not self.data_validation(
                column="due_date",
                value=due_date,
                intention="add"
                ):
                return False
            
            # Валидация priority
            if not self.data_validation(
                column="priority",
                value=priority,
                intention="add"
                ):
                return False
            
            # Валидация status
            if not self.data_validation(
                column="status",
                value=status,
                intention="add"
                ):
                return False
            
            # Создание и инициализация нового объекта Task при успешной проверке
            new_task = Task(
                title=title,
                description=description,
                category=category,
                due_date=due_date,
                priority=priority,
                status=status
            )

            # Открытие файла data.json в режиме чтения и кодировкой UTF-8.
            with open(self.path, "r", encoding="UTF-8") as file:
                data = json.load(file)

            # Подсчет текущих задач в переменной data и присвоение уникального ID
            self.last_id = max(task["id"] for task in data)
            # Увеличение last_id на 1
            new_task.id = self.last_id + 1
            # Обновление last_id для будущего использования
            self.last_id += 1

            # Добавление новой задачи в data
            data.append(new_task.__dict__)

            # Открытие файла data.json в режиме записи и перезапись файла 
            # содержимым объекта data в формате JSON
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

        except Exception as err:
            logger.critical(f"Произошла ошибка в функции \"{__name__}\": {err}")
            return False
        
        return True
    
    def delete_task(self, value: str = "", choice: str = "id"):
        """
        Функция для удаления задачи из системы по заданному параметру.

        Она выполняет валидацию параметров задачи, затем открывает файл данных (data.json),
        удаляет задачу, если она найдена, и сохраняет обновленные данные обратно в файл. 
        Если задача не найдена или произошла ошибка, возвращает False.

        Аргументы:
            value (str): Значение параметра, по которому будет производиться удаление задачи. 
                         Например, это может быть id задачи.
            choice (str): Параметр, по которому будет осуществляться поиск задачи для удаления. 
                          Допустимые значения: "id", "category", "priority", "status".
                          По умолчанию используется "id".

        Возвращает:
            bool: True, если задача успешно удалена, иначе False.
        """

        self.task_found = False

        try:
            # Валидация value и choice
            if not self.data_validation(
                column=choice,
                value=value,
                intention="delete"
                ):
                return False
            
            # Открытие файла data.json в режиме чтения и кодировкой UTF-8.
            with open(self.path, "r", encoding="UTF-8") as file:
                data = json.load(file)

            new_data = [task for task in data if task[f"{choice}"] == value]
            
            # Сравнение данных из new_data и data по длинне
            if len(new_data) == len(data):
                return False

            # Запись измененных данных в файл
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(new_data, file, indent=4, ensure_ascii=False)

            # Если new_data не пусто, выводим данные в формате JSON или таблицы, 
            # если данных нет, возвращаем False.
            if new_data:
                if self.pretty_printed_JSON:
                    return json.dumps(new_data, indent=4, ensure_ascii=False)
                else:
                    return self.format_tasks_table(new_data)
            else:
                logger.warning(f"Значение \"{value}\" не было найдено в файле.")
                return False

        except Exception as err:
            logger.critical(f"Произошла ошибка в функции \"{__name__}\": {err}")
            return False
        
    def change_task(self, _id: int, column: str = "", value: str = ""):
        """
        Функция для изменения существующей задачи в системе.

        Она проверяет параметры изменения задачи с помощью валидации, затем 
        обновляет нужное поле задачи и сохраняет изменения в файл данных (data.json). 
        Каждый параметр задачи проверяется на допустимость значений.

        Аргументы:
            _id (int): Уникальный идентификатор задачи, которую нужно изменить.
            column (str): Название поля задачи, которое требуется изменить.
            value (str): Новое значение для указанного поля.

        Возвращает:
            bool: True, если задача успешно изменена, иначе False.
        """

        self.task_found = False

        try:
            new_data = []

            # Открытие файла data.json в режиме чтения и кодировкой UTF-8.
            with open(self.path, "r", encoding="UTF-8") as file:
                data = json.load(file)
            
            for task in data:
                if task["id"] == _id:
                    self.task_found == True

                    # Валидация new_value на наличие в задаче с указанным id
                    if not self.data_validation(
                        column=f"{column}",
                        value=task[f"{column}"],
                        new_value=value,
                        search_option="change"
                        ):
                        return False
                    
                    # Перезапись значения
                    task[f"{column}"] = value
                    # Добавление перезаписанного значения в new_data
                    new_data.append(task)
                
                else:
                    logger.info(f"Задачи с ID {_id} не было найдено.")
                    return False
                
            # Запись измененных данных в файл
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            # Если new_data не пусто, выводим данные в формате JSON или таблицы, 
            # если данных нет, возвращаем False.
            if new_data:
                logger.info(
                    f"Значение в задаче с ID {_id} в поле \"{column}\", "
                    f"было изменено на \"{value}\"."
                    )
                return True
            else:
                logger.info(f"Задача не была изменена.")
                return False
            
        except Exception as err:
            logger.critical(f"Произошла ошибка в функции \"{__name__}\": {err}")
            return False