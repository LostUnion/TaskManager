import re
import json
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
        'DEBUG': '\033[36m',        # Голубой
        'INFO': '\033[32m',         # Зеленый
        'WARNING': '\033[33m',      # Желтый
        'ERROR': '\033[31m',        # Красный
        'CRITICAL': '\033[1;31m'    # Жирный красный
    }
    RESET = '\033[0m'

    def format(self, record):
        levelname_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{levelname_color}{record.levelname}{self.RESET}"
        return super().format(record)


# Настройка логера
logger = logging.getLogger("keyword_color_logger")
handler = logging.StreamHandler()
formatter = KeywordColorFormatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
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

    def __init__(self, path: str = "src/task_manager/data/data.json"):
        """Инициализация класса"""
        self.path = path

    def format_tasks_table(self, tasks: list):
        """
        Форматирование задач в таблицу
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
        """
        Получает задачи из файла `data.json` на основе указанных фильтров.

        Эта функция фильтрует задачи по указанным полям и возвращает только те,
        которые соответствуют заданным параметрам. В случае ошибок валидации
        или отсутствия подходящих задач, возвращается `False`
        и выводится сообщение об ошибке.

        Аргументы:
            value (str): Значение для поиска.
                         Может быть пустым, если нужно вернуть все задачи.
            option (str): Поле для фильтрации задач. Должно быть одним из:
                - "id": Идентификатор задачи (целое число).
                - "category": Категория задачи.
                - "priority": Приоритет задачи (строка, одно из:
                              "Высокий", "Средний", "Низкий").
                - "status": Статус задачи (строка, одно из:
                            "Выполнена", "Не выполнена").
                - "keywords": Ключевые слова для поиска в полях задачи
                             (например, "title", "description").
                - "due_date": Дата завершения задачи.
                        Используется для поиска просроченных задач.

        Возвращает:
            list: Список задач, соответствующих фильтрам.
                  Если задач не найдено, возвращает `False`.
        """

        try:
            # Открытие файла data.json в режиме чтения и кодировкой UTF-8.
            with open(self.path, "r", encoding="UTF-8") as file:
                data = json.load(file)

            if option == "due_date":
                value = "Просрочено"

            # Проверка, что если поле value пустое, а option указано,
            # возникает ошибка.
            if value.strip() == "" and option.strip() != "":
                logger.error(
                    "При указании значения в поле \"option\" "
                    "необходимо указать искомое значение в поле \"value\""
                )
                return False

            # Проверка, что если value есть, а option пустое, возникает ошибка.
            if value.strip() != "" and option.strip() == "":
                logger.error(
                    "При указании значения в поле \"value\" необходимо "
                    "указать значение в поле \"option\""
                )
                return False

            # Проверка, если value и option пустые, возвращаются все данные.
            if value.strip() == "":
                if self.pretty_printed_JSON:
                    return json.dumps(data, indent=4, ensure_ascii=False)
                else:
                    return self.format_tasks_table(data)

            if value.strip() != "" and option not in ["id", "category",
                                                      "priority", "status",
                                                      "keywords", "due_date"]:
                logger.error(
                    "Аргумент \"option\" должен принимать одно из допустимых "
                    "значений: \"id\", \"category\", \"priority\", "
                    "\"status\", \"keywords\", \"due_date\""
                )
                return False

            if option == "category" and value not in ["Работа",
                                                      "Личное",
                                                      "Обучение"]:
                logger.error(
                    "Аргумент \"value\" должен принимать одно из допустимых "
                    "значений: \"Работа\", \"Личное\" или \"Обучение\""
                )
                return False

            if option == "status" and value not in ["Выполнена",
                                                    "Не выполнена"]:
                logger.error(
                    "Аргумент \"value\" должен принимать одно из допустимых "
                    "значений: \"Выполнена\" или \"Не выполнена\""
                )
                return False

            if option == "priority" and value not in ["Высокий",
                                                      "Средний",
                                                      "Низкий"]:
                logger.error(
                    "Аргумент \"value\" должен принимать одно из допустимых "
                    "значений: \"Высокий\", \"Средний\" или \"Низкий\""
                )
                return False

            # Проверка, если значение есть, а option одно из допустимых
            # значений, затем выполняется валидация для указанного поля.
            if value and option in ["id", "category", "priority", "status"]:
                if option == "id":
                    value = int(value)
                if not self.data_validation(value=value,
                                            column=str(option),
                                            intention="search"):
                    logger.error(f"Валидация для \"{option}\" не прошла.")
                    return False

                # Фильтрация задач, добавление задачи,
                # где значение поля option равно value.
                new_data = [task for task in data if task[option] == value]

                # Если new_data не пусто, выводим данные в формате
                # JSON или таблицы, если данных нет, возвращаем False.
                if new_data:
                    if self.pretty_printed_JSON:
                        return json.dumps(new_data,
                                          indent=4,
                                          ensure_ascii=False)
                    else:
                        return self.format_tasks_table(new_data)
                else:
                    logger.warning(
                        f"Значение \"{value}\" не было найдено в файле."
                    )
                    return False

            # Проверка, если option == "keywords"
            # для поиска по ключевым словам.
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

                # Если new_data не пусто, выводим данные в формате
                # JSON или таблицы, если данных нет, возвращаем False.
                if new_data:
                    if self.pretty_printed_JSON:
                        return json.dumps(new_data,
                                          indent=4,
                                          ensure_ascii=False)
                    else:
                        return self.format_tasks_table(new_data)
                else:
                    logger.warning(
                        f"Ключевого слова \"{value}\" "
                        "не было найдено в таблице."
                    )
                    return False

            # Проверка, если option == "due_date" для поиска
            # по просроченной дате.
            if option == "due_date":
                # Получение нынешнего времени.
                now = datetime.today().date()

                # Добавление задач при условии что нынешняя дата
                # больше или равна дате, указанной в задаче.
                new_data = [
                    task for task in data
                    if now.strftime("%Y-%m-%d") >= task["due_date"]
                ]

                # Если new_data не пусто, выводим данные в формате JSON
                # или таблицы, если данных нет, возвращаем False.
                if new_data:
                    if self.pretty_printed_JSON:
                        return json.dumps(new_data,
                                          indent=4,
                                          ensure_ascii=False)
                    else:
                        return self.format_tasks_table(new_data)
                else:
                    logger.warning(
                        "Просроченных заданий не было найдено в таблице."
                    )
                    return False

        except Exception as err:
            logger.critical(
                f"Произошла ошибка в функции \"getting_task\": {err}"
            )
            return False

    def data_validation(self, column: str = "", value: str = "",
                        new_value: str = "", intention: str = ""):
        """
        Функция валидации данных при добавлении или изменении задачи.

        Проверяет значения для различных полей задачи на соответствие
        типам данных, ограничениям по длине, допустимым значениям
        и формату даты.

        Аргументы:
            column (str): Имя столбца, которое проверяется.
            value (str): Значение, которое проверяется.
            new_value (str): Новое значение, если задача изменяется.
            intention (str): Намерение (add/change/delete)
            search_option (str): Опция для поиска (id, keywords, category,
                                 status)

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

            if intention == "delete":
                if column == "category" and len(value.strip()) < 1:
                    logger.error("Поле \"category\" не может быть пустым.")
                    return False

                if column == "category" and value not in ["Работа",
                                                          "Личное",
                                                          "Обучение"]:
                    logger.error(
                        "Поле \"category\" должно принимать одно из "
                        "допустимых значений: \"Работа\", \"Личное\" "
                        "или \"Обучение\""
                    )
                    return False

            # Проверка, если намерение change или add
            if intention == "change" or intention == "add":
                # Проверка на длинну value если column == "title"
                if column == "title" and len(new_value.strip()) < 5:
                    logger.error(
                        "Поле \"title\" не может быть меньше 5 символов."
                    )
                    return False

                # Проверка на длинну value если column == "description"
                if column == "description" and len(new_value.strip()) < 10:
                    logger.error(
                        "Поле \"description\" не может быть меньше "
                        "10 символов."
                    )
                    return False

                # Проверка на длинну value если column == column == "category"
                if column == "category" and len(new_value.strip()) < 2:
                    logger.error(
                        "Поле \"category\" не может быть меньше 2 символов."
                    )
                    return False

                # Проверка на отсутствие значения для priority
                if column == "priority" and len(new_value.strip()) < 1:
                    logger.error("Поле \"priority\" не может быть пустым.")
                    return False

                valid_prior_value = ["Низкий", "Средний", "Высокий"]
                if column == "priority" and new_value not in valid_prior_value:
                    logger.error(
                        "Поле \"priority\" должно быть одним из значений: "
                        "\"Низкий\", \"Средний\", \"Высокий\"."
                    )
                    return False

                # Проверка на допустимые значения для category
                if column == "category" and new_value not in ["Работа",
                                                              "Личное",
                                                              "Обучение"]:
                    logger.error(
                        "Поле \"category\" должно принимать одно из "
                        "допустимых значений: \"Работа\", \"Личное\" или "
                        "\"Обучение\""
                    )
                    return False

                # Проверка на отсутствие значения для status
                if column == "status" and len(new_value.strip()) < 1:
                    logger.error("Поле \"status\" не может быть пустым.")
                    return False

                # Проверка на допустимые значения для status
                if column == "status" and new_value not in ["Выполнена",
                                                            "Не выполнена"]:
                    logger.error(
                        "Поле \"status\" должно быть одним из значений: "
                        "\"Выполнена\", \"Не выполнена\"."
                    )
                    return False

                # Проверка на отсутствие значения для due_date
                if column == "due_date" and new_value.strip() == "":
                    logger.error(
                            "Значение в поле \"due_date\" не должно "
                            "быть пустым. Ожидается формат YYYY-MM-DD."
                        )
                    return False

                # Проверка формата даты
                if column == "due_date":
                    # Шаблон даты
                    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
                    if not re.match(date_pattern, new_value.strip()):
                        logger.error(
                            "Значение в поле \"due_date\" указано "
                            "некорректно. Ожидается формат YYYY-MM-DD."
                        )
                        return False

                    # Проверка на будущую дату
                    now = datetime.today().date()
                    if now.strftime("%Y-%m-%d") > new_value.strip():
                        logger.error(
                            "Поле \"due_date\" не может содержать дату "
                            "из прошлого."
                        )
                        return False

                # Проверка на допустимые значения для column
                # если intention == "search"
                valid_col_search = ["id", "title", "description",
                                    "category", "due_date", "priority",
                                    "status"]
                if intention == "search" and column not in valid_col_search:
                    logger.error(
                        "Неверное значение для \"column\". "
                        "Допустимые значения: "
                        f"{', '.join(valid_col_search)}."
                    )
                    return False

                # Проверка на повторяющиеся значения, если намерение change
                if value == new_value:
                    logger.error(
                        f"Значение поля \"{column}\" не может быть "
                        f"изменено с \"{value}\" на \"{new_value}\", "
                        "поскольку значения одинаковые."
                    )
                    return False

        except Exception as err:
            logger.critical(
                f"Произошла ошибка в функции \"{__name__}\": {err}"
            )
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
                new_value=title,
                intention="add"
            ):
                return False

            # Валидация description
            if not self.data_validation(
                column="description",
                new_value=description,
                intention="add"
            ):
                return False

            # Валидация category
            if not self.data_validation(
                column="category",
                new_value=category,
                intention="add"
            ):
                return False

            # Валидация due_date
            if not self.data_validation(
                column="due_date",
                new_value=due_date,
                intention="add"
            ):
                return False

            # Валидация priority
            if not self.data_validation(
                column="priority",
                new_value=priority,
                intention="add"
            ):
                return False

            # Валидация status
            if not self.data_validation(
                column="status",
                new_value=status,
                intention="add"
            ):
                return False

            # Создание и инициализация нового объекта Task
            # при успешной проверке
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

            # Подсчет текущих задач в переменной data и
            # присвоение уникального ID
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
            logger.critical(
                f"Произошла ошибка в функции \"{__name__}\": {err}"
            )
            return False

        logger.info(
            f"Задача \"{new_task.title}\" успешно добавлена "
            f"в таблицу с ID: {new_task.id}."
            )
        return True

    def delete_task(self, value: str = "", choice: str = ""):
        """
        Функция для удаления задачи из системы по заданному параметру.

        Она выполняет валидацию параметров задачи, затем открывает файл данных
        (data.json), удаляет задачу, если она найдена, и сохраняет обновленные
        данные обратно в файл.
        Если задача не найдена или произошла ошибка, возвращает False.

        Аргументы:
            value (str): Значение параметра, по которому будет производиться
                         удаление задачи. Например, это может быть id задачи.
            choice (str): Параметр, по которому будет осуществляться удаления.
                          Допустимые значения: "id" или "category"

        Возвращает:
            bool: True, если задача успешно удалена, иначе False.
        """

        self.task_found = False

        # Проверка на заполненные значения в value и choice
        if value.strip() == "" or choice.strip() == "":
            logger.error(
                "Значения в аргументах value и choice "
                "не должны быть пустыми."
            )
            return False

        if choice == "id":
            try:
                value = int(value)
            except Exception as err:
                logger.error(
                    "Некорректное значение параметра value "
                    f"при использовании id: {err}."
                )
                return False

        # Проверка на допустимые значения для choice
        if choice not in ["id", "category"]:
            logger.error(
                "Значения в аргументе choice должны быть включать "
                "в себя только \"id\" или \"category\""
            )
            return False

        try:
            # Валидация value и choice
            if not self.data_validation(
                column=choice,
                value=value,
                intention="delete"
            ):
                return False

            new_data = []

            # Открытие файла data.json в режиме чтения и кодировкой UTF-8.
            with open(self.path, "r", encoding="UTF-8") as file:
                data = json.load(file)

            if choice == "category":
                for task in data:
                    if task["category"] == value:
                        self.task_found = True
                        logger.info(
                            f"Задача \"{task['title']}\" с "
                            f"ID {task['id']}, с категорией "
                            f"\"{value}\" была успешно удалена."
                        )
                        continue

                    new_data.append(task)

                if not self.task_found:
                    logger.warning(
                        f"Задачи с категорией \"{value}\" не найдены."
                    )
                    return False

                # Запись измененных данных в файл
                with open(self.path, "w", encoding="utf-8") as file:
                    json.dump(new_data, file, indent=4, ensure_ascii=False)

                return True

            if choice == "id":
                value = int(value)
                for task in data:
                    if task["id"] == value:
                        self.task_found = True
                        logger.info(
                            f"Задача \"{task['title']}\" с "
                            f"ID {task['id']} была успешно удалена."
                        )
                        continue

                    new_data.append(task)

                if not self.task_found:
                    logger.warning(f"Задача с ID {value} не найдена.")
                    return False

                # Запись измененных данных в файл
                with open(self.path, "w", encoding="utf-8") as file:
                    json.dump(new_data, file, indent=4, ensure_ascii=False)

                return True

        except Exception as err:
            logger.critical(
                f"Произошла ошибка в функции \"delete_task\": {err}"
            )
            return False

    def change_task(self, _id: Optional[int] = None,
                    column: str = "", value: str = ""):
        """
        Функция для изменения существующей задачи в системе.

        Она проверяет параметры изменения задачи с помощью валидации,
        затем обновляет нужное поле задачи и сохраняет изменения в
        файл данных (data.json). Каждый параметр задачи проверяется
        на допустимость значений.

        Аргументы:
            _id (int): Уникальный идентификатор задачи, которую нужно изменить.
            column (str): Название поля задачи, которое требуется изменить.
            value (str): Новое значение для указанного поля.

        Возвращает:
            bool: True, если задача успешно изменена, иначе False.
        """

        self.task_found = False
        column = str(column)
        value = str(value)

        _id = str(_id)
        if _id is None or _id.strip() == "":
            logger.error(
                "Аргумент _id должен быть обязательно заполнен."
            )
            return False

        # Проверка _id на значение
        if type(_id) is str:
            try:
                _id = int(_id)
            except Exception as err:
                logger.error(
                    f"Некорректное значение _id: {err}"
                )
                return False

        if _id and column == "" or not column.strip():
            logger.error(
                "Аргументы column должен быть обязательно заполнен."
            )
            return False

        if _id and value == "" or not value.strip():
            logger.error(
                "Аргументы value должен быть обязательно заполнен."
            )
            return False

        valid_columns = ["title", "description", "category",
                         "due_date", "priority", "status"]
        if column not in valid_columns:
            logger.error(
                "Аргумент column может включать в себя только "
                "следующие значения: \"title\", \"description\", "
                "\"category\", \"due_date\", \"priority\", \"status\""
            )
            return False

        try:
            new_data = []

            # Открытие файла data.json в режиме чтения и кодировкой UTF-8.
            with open(self.path, "r", encoding="UTF-8") as file:
                data = json.load(file)

            for task in data:
                if task["id"] == _id:
                    self.task_found = True  # Задача найдена

                    # Валидация нового значения
                    if not self.data_validation(
                        column=column,
                        value=task[column],
                        new_value=value,
                        intention="change",
                    ):
                        return False

                    # Перезаписываем значение
                    task[column] = value

                # Добавление задачи в новый список (независимо,
                # была ли она изменена)
                new_data.append(task)

            # Если задача не была найдена
            if not self.task_found:
                logger.warning(f"Задачи с ID {_id} не было найдено.")
                return False

            # Запись измененных данных обратно в файл
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(new_data, file, indent=4, ensure_ascii=False)

            logger.info(
                f"Значение в задаче с ID {_id} в поле \"{column}\" "
                f"было изменено на \"{value}\"."
            )
            return True

        except Exception as err:
            logger.critical(
                f"Произошла ошибка в функции \"change_task\": {err}"
            )
            return False
