import re
import json
import logging
from typing import Optional
from datetime import datetime
import traceback

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
logger.disabled = True

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
                message_error = (
                    "При указании значения в поле \"option\" "
                    "необходимо указать искомое значение в поле \"value\""
                )

                logger.error(message_error)
                print(message_error)
                return False

            # Проверка, что если value есть, а option пустое, возникает ошибка.
            if value.strip() != "" and option.strip() == "":
                message_error = (
                    "При указании значения в поле \"value\" необходимо "
                    "указать значение в поле \"option\""
                )
                logger.error(message_error)
                print(message_error)
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
                message_error = (
                    "Аргумент \"option\" должен принимать одно из допустимых "
                    "значений: \"id\", \"category\", \"priority\", "
                    "\"status\", \"keywords\", \"due_date\""
                )

                logger.error(message_error)
                print(message_error)
                return False

            if option == "category" and value not in ["Работа",
                                                      "Личное",
                                                      "Обучение"]:
                message_error = (
                    "Аргумент \"value\" должен принимать одно из допустимых "
                    "значений: \"Работа\", \"Личное\" или \"Обучение\""
                )
                logger.error(message_error)
                print(message_error)
                return False

            if option == "status" and value not in ["Выполнена",
                                                    "Не выполнена"]:
                message_error = (
                    "Аргумент \"value\" должен принимать одно из допустимых "
                    "значений: \"Выполнена\" или \"Не выполнена\""
                )
                logger.error(message_error)
                print(message_error)
                return False

            if option == "priority" and value not in ["Высокий",
                                                      "Средний",
                                                      "Низкий"]:

                message_error = (
                    "Аргумент \"value\" должен принимать одно из допустимых "
                    "значений: \"Высокий\", \"Средний\" или \"Низкий\""
                )
                logger.error(message_error)
                print(message_error)
                return False

            # Проверка, если значение есть, а option одно из допустимых
            # значений, затем выполняется валидация для указанного поля.
            if value and option in ["id", "category", "priority", "status"]:
                if option == "id":
                    value = int(value)
                if not self.data_validation(value=value,
                                            column=str(option),
                                            intention="search"):
                    message_error = (
                        f"Валидация для \"{option}\" не прошла."
                    )
                    logger.error(message_error)
                    print(message_error)
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
                    message_warning = (
                        f"Значение \"{value}\" не было найдено в файле."
                    )
                    user_message_warning = (
                        f"Такого значения как \"{value}\" не было найдено"
                        " в вашей таблице."
                    )

                    logger.warning(message_warning)
                    print(message_warning)
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
                    message_warning = (
                        f"Ключевого слова \"{value}\" "
                        "не было найдено в таблице."
                    )
                    user_message_warning = (
                        f"Ключевого слова \"{value}\" "
                        "не было найдено в вашей таблице."
                    )
                    logger.warning(message_warning)
                    print(user_message_warning)
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
                    message_error = (
                        "Просроченных заданий не было найдено в таблице."
                    )
                    user_message_error = (
                        "В вашей таблице нет просроченных заданий."
                    )
                    logger.warning(message_error)
                    print(user_message_error)
                    return False

        except Exception as err:
            tb = traceback.format_exc()
            message_critical = (
                f"Произошла ошибка в функции \"getting_task\":{tb}: {err}"
            )
            user_message_critical = (
                "Произошли непредвиденные неполадки в программе."
            )
            logger.critical(message_critical)
            print(user_message_critical)
            return False

    def data_validation(self, column: str = "",
                        value: str = "", intention: str = "",
                        _id: Optional[int] = None):
        """
        Функция валидации данных при добавлении или изменении задачи.

        Проверяет значения для различных полей задачи на соответствие
        типам данных, ограничениям по длине, допустимым значениям
        и формату даты.

        Аргументы:
            column (str): Имя столбца, которое проверяется.
            value (str): Значение, которое проверяется.
            new_value (str): Новое значение, если задача изменяется.
            intention (str): Намерение (add/change/delete/search)

        Возвращает:
            bool: True, если валидация прошла успешно, иначе False.
        """

        try:
            # Валидация intention на входящие значения
            if intention not in ["add", "change", "delete", "search"]:
                message_error = (
                    "Значение \"intention\" должно быть одним из значений: "
                    "\"add\", \"change\", \"delete\" или \"search\"."
                )
                logger.error(message_error)
                print(message_error)
                return False

            if intention == "delete":
                if column == "category" and len(value.strip()) < 1:
                    message_error = (
                        "Поле \"category\" не может быть пустым."
                    )
                    user_message_error = (
                        "Категория задачи должна быть пустой."
                    )
                    logger.error(message_error)
                    print(user_message_error)
                    return False

                if column == "category" and value not in ["Работа",
                                                          "Личное",
                                                          "Обучение"]:
                    message_error = (
                        "Поле \"category\" должно принимать одно из "
                        "допустимых значений: \"Работа\", \"Личное\" "
                        "или \"Обучение\""
                    )
                    user_message_error = (
                        "Категория задачи должна быть только \"Работа\""
                        ", \"Личное\" или \"Обучение\"."
                    )
                    logger.error(message_error)
                    print(user_message_error)
                    return False

            # Проверка, если намерение change или add
            if intention in ("change", "add", "search"):
                # Проверка на длинну value если column == "title"
                if column == "title" and len(value.strip()) < 5:
                    message_error = (
                        "Поле \"title\" не может быть меньше 5 символов."
                    )
                    user_message_error = (
                        "Заголовок не может быть менее 5 символов."
                    )
                    logger.error(message_error)
                    print(user_message_error)
                    return False

                # Проверка на длинну value если column == "description"
                if column == "description" and len(value.strip()) < 10:
                    message_error = (
                        "Поле \"description\" не может быть меньше "
                        "10 символов."
                    )
                    user_message_error = (
                        "Описание не может быть менее 10 символов."
                    )
                    logger.error(message_error)
                    print(user_message_error)
                    return False

                # Проверка на длинну value если column == column == "category"
                if column == "category" and len(value.strip()) < 1:
                    message_error = (
                        "Поле \"category\" не может быть меньше пустым."
                    )
                    user_message_error = (
                        "Категория не может быть пустой."
                    )
                    logger.error(message_error)
                    print(user_message_error)
                    return False

                # Проверка на отсутствие значения для priority
                if column == "priority" and len(value.strip()) < 1:
                    message_error = (
                        "Поле \"priority\" не может быть пустым."
                    )
                    user_message_error = (
                        "Приоритет задачи не может быть пустым."
                    )
                    logger.error(message_error)
                    print(message_error)
                    return False

                valid_prior_value = ["Низкий", "Средний", "Высокий"]
                if column == "priority" and value not in valid_prior_value:
                    message_error = (
                        "Поле \"priority\" должно быть одним из значений: "
                        "\"Низкий\", \"Средний\", \"Высокий\"."
                    )
                    user_message_error = (
                        "Приоритет задачи должен включать в себя одно из зна"
                        "чений \"Низкий\", \"Средний\" или \"Высокий\"."
                    )
                    logger.error(message_error)
                    print(user_message_error)
                    return False

                # Проверка на допустимые значения для category
                if column == "category" and value not in ["Работа",
                                                          "Личное",
                                                          "Обучение"]:
                    message_error = (
                        "Поле \"category\" должно принимать одно из "
                        "допустимых значений: \"Работа\", \"Личное\" или "
                        "\"Обучение\""
                    )
                    user_message_error = (
                        "Категория задачи должна быть указана в качестве "
                        "одного из допустимых значений:\n\"Работа\", \"Ли"
                        "чное\" или \"Обучение\""
                    )
                    logger.error(message_error)
                    print(user_message_error)
                    return False

                # Проверка на отсутствие значения для status
                if column == "status" and len(value.strip()) < 1:
                    value = "Не выполнена"

                # Проверка на допустимые значения для status
                if column == "status" and value not in ["Выполнена",
                                                        "Не выполнена"]:
                    message_error = (
                        "Поле \"status\" должно быть одним из значений: "
                        "\"Выполнена\", \"Не выполнена\"."
                    )
                    user_message_error = (
                        "Статус задачи принимает только значения: "
                        "\"Выполнена\" или \"Не выполнена\"."
                    )
                    logger.error(message_error)
                    print(user_message_error)
                    return False

                # Проверка на отсутствие значения для due_date
                if column == "due_date" and value.strip() == "":
                    message_error = (
                        "Значение в поле \"due_date\" не должно "
                        "быть пустым. Ожидается формат YYYY-MM-DD."
                    )
                    user_message_error = (
                        "Не может быть задачи без сроков выполнения.\n"
                        "Ожидается формат YYYY-MM-DD."
                    )
                    logger.error(message_error)
                    print(user_message_error)
                    return False

                # Проверка формата даты
                if column == "due_date":
                    # Шаблон даты
                    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
                    if not re.match(date_pattern, value.strip()):
                        message_error = (
                            "Значение в поле \"due_date\" указано "
                            "некорректно. Ожидается формат YYYY-MM-DD."
                        )
                        user_message_error = (
                            "Дату необходимо указывать так:\n"
                            "Год-месяц-день в формате YYYY-MM-DD\n"
                            "Укажите дату в корректном формате."
                        )
                        logger.error(message_error)
                        print(user_message_error)
                        return False

                    # Проверка на будущую дату
                    now = datetime.today().date()
                    if now.strftime("%Y-%m-%d") > value.strip():
                        message_error = (
                            "Поле \"due_date\" не может содержать дату "
                            "из прошлого."
                        )
                        user_message_error = (
                            "Невозможно запланировать задачу на дату, которая"
                            " уже прошла.\nПожалуйста, укажите дату в предела"
                            "х месяца или года, при условии,\nчто ее еще не "
                            "было."
                        )
                        logger.error(message_error)
                        print(user_message_error)
                        return False

                # Проверка на допустимые значения для column
                # если intention == "search"
                valid_col_search = ["id", "title", "description",
                                    "category", "due_date", "priority",
                                    "status"]
                if intention == "search" and column not in valid_col_search:
                    message_error = (
                        "Неверное значение для \"column\". "
                        "Допустимые значения: "
                        f"{', '.join(valid_col_search)}."
                    )
                    logger.error(message_error)
                    print(message_error)
                    return False

                # Открытие файла data.json в режиме чтения и кодировкой UTF-8.
                with open(self.path, "r", encoding="UTF-8") as file:
                    data = json.load(file)

                # Проверка на повторяющиеся значения, если намерение change
                if intention == "change":
                    if _id is None:
                        message_error = (
                            "Необходимо указать ID"
                        )
                        logger.error(message_error)
                        print(message_error)
                        return False

                    for task in data:
                        if task.get("id") == int(_id):
                            if task.get(column) == value:
                                message_error = (
                                    f"Значение поля \"{column}\" не может"
                                    f" быть изменено с \"{task.get(column)}"
                                    f"\" на \"{value}\", поскольку значения"
                                    " одинаковые."
                                )
                                user_message_error = (
                                    "Значение, которое вы хотите изменить,"
                                    f" уже является \"{value}\".\nПожалуйс"
                                    "та, укажите новое значение."
                                )
                                logger.error(message_error)
                                print(user_message_error)
                                return False

        except Exception as err:
            tb = traceback.format_exc()
            message_critical = (
                f"Произошла ошибка в функции \"data_validation\":{tb}: {err}"
            )
            user_message_critical = (
                "Произошли непредвиденные неполадки в программе."
            )
            logger.critical(message_critical)
            print(user_message_critical)
            return False

        return True

    def add_task(self, title: str = "", description: str = "",
                 category: str = "", due_date: str = "",
                 priority: str = "", status: str = "Не выполено"):

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
                          По умолчанию "Не выполнена"

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
            tb = traceback.format_exc()
            message_critical = (
                f"Произошла ошибка в функции \"{__name__}\":{tb} {err}"
            )
            user_message_critical = (
                "Произошли непредвиденные неполадки в программе."
            )
            logger.critical(message_critical)
            print(user_message_critical)
            return False

        message_success = (
            f"Задача \"{new_task.title}\" успешно добавлена "
            f"в таблицу с ID: {new_task.id}."
        )
        logger.info(message_success)
        print(message_success)
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
            message_error = (
                "Значения в аргументах value и choice "
                "не должны быть пустыми."
            )
            logger.error(message_error)
            print(message_error)
            return False

        if choice == "id":
            try:
                value = int(value)
            except Exception as err:
                message_error = (
                    "Некорректное значение параметра value "
                    f"при использовании id: {err}."
                )
                logger.error(message_error)
                print(message_error)
                return False

            # Проверка на допустимые значения для choice
        if choice not in ["id", "category"]:
            message_error = (
                "Значения в аргументе choice должны быть включать "
                "в себя только \"id\" или \"category\""
            )
            logger.error(message_error)
            print(message_error)
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
                        message_ = (
                            f"Задача \"{task['title']}\" с "
                            f"ID {task['id']}, с категорией "
                            f"\"{value}\" была успешно удалена."
                        )
                        logger.info(message_)
                        print(message_)
                        continue

                    new_data.append(task)

                if not self.task_found:
                    message_ = (
                        f"Задачи с категорией \"{value}\" не найдены."
                    )
                    user_message_ = (
                        "В Вашей таблице не найдены задачи с категор"
                        f"ией \"{value}\""
                    )
                    logger.warning(message_)
                    print(user_message_)
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
                        message_ = (
                            f"Задача \"{task['title']}\" с "
                            f"ID {task['id']} была успешно удалена."
                        )
                        logger.info(message_)
                        print(message_)
                        continue

                    new_data.append(task)

                if not self.task_found:
                    message_ = (
                        f"Задача с ID {value} не найдена."
                    )
                    user_message_ = (
                        f"В Вашей таблице нет задачи с ID \"{value}\""
                    )
                    logger.warning(message_)
                    print(user_message_)
                    return False

                # Запись измененных данных в файл
                with open(self.path, "w", encoding="utf-8") as file:
                    json.dump(new_data, file, indent=4, ensure_ascii=False)

                return True

        except Exception as err:
            tb = traceback.format_exc()
            message_critical = (
                f"Произошла ошибка в функции \"delete_task\":{tb} {err}"
            )
            user_message_critical = (
                "Произошли непредвиденные неполадки в программе."
            )
            logger.critical(message_critical)
            print(user_message_critical)
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
            message_error = (
                "Аргумент _id должен быть обязательно заполнен."
            )
            logger.error(message_error)
            print(message_error)
            return False

        # Проверка _id на значение
        if type(_id) is str:
            try:
                _id = int(_id)
            except Exception as err:
                message_error = (
                    f"Некорректное значение _id: {err}"
                )
                logger.error(message_error)
                print(message_error)
                return False

        if _id and column == "" or not column.strip():
            message_error = (
                "Аргументы column должен быть обязательно заполнен."
            )
            logger.error(message_error)
            print(message_error)
            return False

        if _id and value == "" or not value.strip():
            message_error = (
                "Аргументы value должен быть обязательно заполнен."
            )
            logger.error(message_error)
            print(message_error)
            return False

        valid_columns = ["title", "description", "category",
                         "due_date", "priority", "status"]
        if column not in valid_columns:
            message_error = (
                "Аргумент column может включать в себя только "
                "следующие значения: \"title\", \"description\", "
                "\"category\", \"due_date\", \"priority\", \"status\""
            )
            logger.error(message_error)
            print(message_error)
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
                        value=value,
                        intention="change",
                        _id=_id
                    ):
                        return False

                    # Перезаписываем значение
                    task[column] = value

                # Добавление задачи в новый список (независимо,
                # была ли она изменена)
                new_data.append(task)

            # Если задача не была найдена
            if not self.task_found:
                message_warning = (
                    f"Задачи с ID {_id} не было найдено."
                )
                user_message_warning = (
                    f"Не удалось найти задачу с ID {_id}."
                    "Пожалуйста, проверьте, верно ли вы у"
                    "казали искомое значение."
                )
                logger.warning(message_warning)
                print(user_message_warning)
                return False

            # Запись измененных данных обратно в файл
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(new_data, file, indent=4, ensure_ascii=False)

            message_success = (
                f"Значение в задаче с ID {_id} в поле \"{column}\" "
                f"было изменено на \"{value}\"."
            )
            user_message_success = (
                f"Готово! Значение в задаче с ID {_id} "
                f"было изменено на \"{value}\"."
            )
            logger.info(message_success)
            print(user_message_success)
            return True

        except Exception as err:
            tb = traceback.format_exc()
            message_critical = (
                f"Произошла ошибка в функции \"change_task\":{tb} {err}"
            )
            user_message_critical = (
                "Произошли непредвиденные неполадки в программе."
            )
            logger.critical(message_critical)
            print(user_message_critical)
            return False
