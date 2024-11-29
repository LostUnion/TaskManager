import os
from module_task_manager import TaskManager
import string
from datetime import datetime
import re

def add_task():
    """Добавление задачи"""

    os.system('cls') # Очистка консоли

    display_add_task = (
        "Для добавлении задачи, заполните следующие данные.\n"
    )

    print(display_add_task)

    # Валидация поля Title
    while True:
        title = str(input("Title: ")).strip()

        # Проверка на минимальную длинну title
        if not title:
            print("Поле Title не может быть пустым.")
            continue

        # Проверка на минимальную длинну title
        if len(title) < 5:
            print(f"Поле Title не может содержать в себе менее 5 символов. Минимальная длина Description - 5 символов.")
            continue

        # Проверка на первый символ в title
        if title.startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')):
            print(f"Поле Title не может начинаться с цифры.")
            continue

        # Проверка на содержание специальных символов в title
        if any(char in string.punctuation for char in title):
            print("Поле Title не должно содержать специальных символов.")
            continue
        
        break


    # Валидация поля Description
    while True:
        description = str(input("Description: "))

        # Проверка на существование значения в description
        if not description:
            print("Поле Description не может быть пустым.")
            continue

        # Проверка на минимальную длинну description
        if len(description) < 20:
            print(f"Поле Description не может содержать в себе менее 20 символов. Минимальная длина Description - 20 символов.")
            continue

        # Проверка на первый символ в description
        if description.startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')):
            print(f"Поле Description не может начинаться с цифры.")
            continue

        # Проверка на содержание специальных символов в description
        if any(char in string.punctuation for char in description):
            print("Поле Description не должно содержать специальных символов.")
            continue
        
        break

    # Валидация поля Category
    while True:
        category = str(input("Category: ")).strip()

        # Проверка на существование значения в category
        if not category:
            print("Поле Category не может быть пустым.")
            continue

        # Проверка на минимальную длинну category
        if len(category) < 5:
            print(f"Поле Category не может содержать в себе менее 5-х символов. Минимальная длина Category - 5 символов.")
            continue

        # Проверка на первый символ в category
        if category.startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')):
            print(f"Поле Category не может начинаться с цифры.")
            continue

        # Проверка на содержание специальных символов в category
        if any(char in string.punctuation for char in category):
            print("Поле Category не должно содержать специальных символов.")
            continue

        break

    # Валидация поля Due_date
    while True:
        now = datetime.today().date() # Получение текущей даты
        date_now = now.strftime("%Y-%m-%d")  # Преобразование даты в строку
        due_date = str(input("Due_date [YYYY-MM-DD]: ")).strip()

        date_pattern = r'^\d{4}-\d{2}-\d{2}$' # Паттерн даты
        

        # Проверка на существование значения в due_date
        if not due_date:
            print("Поле Due_date не может быть пустым.")
            continue

        # Проверка на корректность указанной даты
        if not re.match(date_pattern, due_date):
            print(f"{due_date} в поле Due_date указано некорректно. Пожалуйста, укажите Due_date в формате YYYY-MM-DD.")
            continue

        # Проверка на то, что указаная дата не прошедшего времени
        if date_now > due_date:
            print("Поле Due_date не может содержать дату из прошлого. Укажите будущую дату.")
            continue

        break

    # Валидация поля Priority
    while True:
        priority = str(input("Priority [Низкий\Средний\Высокий]: ")).strip()

        # Проверка на существование значения в priority
        if not priority:
            print("Поле Priority не может быть пустым.")
            continue

        # Проверка на то, что в priority содержится "Низкий", "Средний" или "Высокий"
        if priority not in ["Низкий", "Средний", "Высокий"]:
            print(f"Поле Priority не содержать в себе никакие значения кроме \"Низкий\", \"Средний\" или \"Высокий\". Значение {priority} не поддерживается.")
            continue

        break

    # Валидация поля Status
    while True:
        status = str(input("Status [Выполнена\Не выполнена]: ")).strip()

        # Проверка на существование значения в status
        if not status:
            print("Поле Status не может быть пустым.")
            continue

        # Проверка на то, что в status содержится "Выполнена" или "Не выполнена"
        if status not in ["Выполнена", "Не выполнена"]:
            print(f"Поле Status не содержать в себе никакие значения кроме \"Выполнена\" или \"Не выполнена\". Значение {priority} не поддерживается.")
            continue
            
        break

    ready_made_solution = (
        "Перед добавлением задачи проверьте правильность указаных данных.\n\n"
        f"Title: {title}\n"
        f"Description: {description}\n"
        f"Due_date: {due_date}\n"
        f"Priority: {priority}\n"
        f"Status: {status}\n\n"
        "[1] Добавить задачу\n"
        "[2] Изменить задачу\n"
        "[3] Назад"
    )

    os.system('cls')

    print(ready_made_solution)

    try:
        answer = int(input(">> "))  # Получение от пользователя номера варианта в числовом формате
    except ValueError:
        print("Неверный ввод, пожалуйста, введите число.")
        return

    match answer:
        case 1:
            table = TaskManager()
            result_category = table.add_task(
                title=title,
                description=description,
                due_date=due_date,
                priority=priority,
                status=status
                )
                
            successful_result = (
                f"{result_category}\n\n"
                "[1] Назад"
            )
            try:
                print(successful_result)
            except:
                print("При добавлении задачи произлошла ошибка")

            try:
                answer = int(input(">> "))  # Получение от пользователя номера варианта в числовом формате
            except ValueError:
                print("Неверный ввод, пожалуйста, введите число.")
                return

            match answer:
                case 1:
                    main_menu()

        case 2:
            add_task()
        case 3:
            main_menu()







def output_by_category(value):
    """Вывод таблицы с задачами где value=category"""

    os.system('cls')

    table = TaskManager()
    result_category = table.get_task(value)

    display_output_by_category = (
        f"Таблица со всеми задачами с категорией {value}\n"
        f"{result_category}\n"
        "[1] Назад"
    )

    print(display_output_by_category)

    try:
        answer = int(input(">> "))  # Получение от пользователя номера варианта в числовом формате
    except ValueError:
        print("Неверный ввод, пожалуйста, введите число.")
        return

    match answer:
        case 1:
            main_menu()


def search_by_category():
    """Форма ввода категории, задачи по которой нужно вывести"""

    os.system('cls')

    display_search_by_category = (
        "Пожалуйста, введите категорию, задачи которой нужно найти.\n"
    )

    print(display_search_by_category)

    answer = input(">> ")  # Получение от пользователя категории в строковом формате
    output_by_category(answer)


def view_task_all():
    """Вывод всех задач"""

    os.system('cls')

    table = TaskManager()
    result = table.get_task()
    print(
        "Таблица со всеми задачами\n"
        f"{result}\n"
        "[1] Назад"
    )

    try:
        answer = int(input(">> "))  # Получение от пользователя номера варианта в числовом формате
    except ValueError:
        print("Неверный ввод, пожалуйста, введите число.")
        return

    match answer:
        case 1:
            main_menu()


def view_tasks():
    """Раздел меню с выбором отображения задач"""

    os.system('cls')

    print(
        "Как вы хотите отобразить задачи.\n\n"
        "[1] Вывести все задачи\n"
        "[2] Найти и вывести по категории\n"
        "[3] Назад"
    )

    try:
        answer = int(input(">> "))  # Получение от пользователя номера варианта в числовом формате
    except ValueError:
        print("Неверный ввод, пожалуйста, введите число.")
        return

    match answer:
        case 1:
            view_task_all()
        case 2:
            search_by_category()
        case 3:
            main_menu()


def main_menu():
    """Раздел главного меню"""

    os.system('cls')

    print(
        "TaskManager - консольное приложение для управления задачами.\n\n"
        "[1] Просмотр задач\n"
        "[2] Добавление задачи\n"
        "[3] Изменение задачи\n"
        "[4] Удаление задачи\n"
        "[5] Поиск задач\n"
        "[6] Выйти\n"
    )

    try:
        answer = int(input(">> "))
    except ValueError:
        print("Неверный ввод, пожалуйста, введите число.")
        return

    match answer:
        case 1:
            view_tasks()
        case 2:
            add_task()


if __name__ == "__main__":
    main_menu()
