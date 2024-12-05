import os
from time import sleep

from task_manager.task_manager import TaskManager


def delete(value):
    tab = TaskManager()
    tasks = tab.getting_task()

    match value:
        case "id":
            while True:
                os.system("cls")
                delete_text = (
                    f"{tasks}\n\n"
                    "Введите ID задачи, которую необходимо удалить.\n\n"
                    "[0] Назад\n"
                )

                try:
                    print(delete_text)
                    user_input_delete = int(input(">> "))
                except ValueError:
                    print(
                        "Введите номер варианта в числовом формате\n"
                        "В данном разделе меню, текст не поддерживается."
                    )
                    sleep(2)
                    delete(value)

                if user_input_delete == 0:
                    delete_task()

                if tab.data_validation(column="id",
                                       value=str(user_input_delete),
                                       intention="delete"):
                    if tab.delete_task(value=str(user_input_delete),
                                       choice="id"):
                        sleep(2)
                        delete_task()
                else:
                    sleep(2)
                    delete(value)

        case "category":
            while True:
                os.system("cls")
                delete_text = (
                    f"{tasks}\n\n"
                    "Введите категорию задач для удаления.\n\n"
                    "[0] Назад\n"
                )

                print(delete_text)
                user_input_delete = str(input(">> "))

                if user_input_delete == "0":
                    delete_task()

                if tab.data_validation(column="category",
                                       value=str(user_input_delete),
                                       intention="delete"):
                    if tab.delete_task(value=str(user_input_delete),
                                       choice="category"):
                        sleep(2)
                        delete_task()
                else:
                    sleep(2)
                    delete(value)


def delete_task():
    tab = TaskManager()
    tasks = tab.getting_task()

    while True:
        os.system("cls")
        delete_task_text = (
            f"{tasks}\n\n"
            "Выберите способ удаления задачи:\n"
            "По идентификатору (ID) — будет удалена одна задача.\n"
            "По категории — будут удалены все задачи, принадлежащие\n"
            "выбранной категории.\n\n"
            "[1] Удалить по ID\n"
            "[2] Удалить по категории\n"
            "[0] Назад\n"
        )

        try:
            print(delete_task_text)
            user_input_delete_task = int(input(">> "))
        except ValueError:
            print(
                "Введите номер варианта в числовом формате\n"
                "В данном разделе меню, текст не поддерживается."
            )
            sleep(2)
            change_task()

        if user_input_delete_task == 0:
            main_menu()

        match user_input_delete_task:
            case 1:
                delete("id")
            case 2:
                delete("category")


def change(value, option):
    tab = TaskManager()
    task = tab.getting_task(value=str(value), option="id")

    match option:
        case "title":
            while True:
                os.system("cls")
                change_text = (
                    f"{task}\n\n"
                    "Заголовок задачи дожен быть не менее 5 символов.\n"
                    "Он должен быть информативным, чтобы вам было по-\n"
                    "нятно, о чем идет речь и он не должен повторяться.\n\n"
                    "[0] Отмена\n"
                )

                print(change_text)
                user_input_change = input("Новый заголовок: ")

                if user_input_change == "0":
                    change_task_sett(value)

                if tab.data_validation(column="title",
                                       value=user_input_change,
                                       intention="change",
                                       _id=value):
                    if tab.change_task(_id=value,
                                       column="title",
                                       value=str(user_input_change)):
                        sleep(2)
                        change_task_sett(value)

                else:
                    sleep(2)
                    change(value, option)

        case "description":
            while True:
                os.system("cls")
                change_text = (
                    f"{task}\n\n"
                    "Описание задачи дожно быть не менее 10 символов.\n"
                    "Оно должно четко и подробно объяснять суть зада-\n"
                    "чи. А также иметь достаточно информации для кор-\n"
                    "ректного выполнения и не должно повторяться.\n\n"
                    "[0] Отмена\n"
                )

                print(change_text)
                user_input_change = input("Новое описание: ")

                if user_input_change == "0":
                    change_task_sett(value)

                if tab.data_validation(column="description",
                                       value=user_input_change,
                                       intention="change",
                                       _id=value):
                    if tab.change_task(_id=value,
                                       column="description",
                                       value=str(user_input_change)):
                        sleep(2)
                        change_task_sett(value)

                else:
                    sleep(2)
                    change(value, option)

        case "category":
            while True:
                os.system("cls")
                change_text = (
                    f"{task}\n\n"
                    "Категория, необходима для четкого распределения \n"
                    "задачи. Категория может включать в себя только \n"
                    "одно из значений:\n\n"
                    "Личное - задачи связанные с повседневной жизнью.\n"
                    "Например: Поход в кино, прогулка, приготовить "
                    "ужин.\n\n"
                    "Обучение - задачи связанные с получения новых знаний\n"
                    "навыков, умений, опыта.\nНапример: Прохождение курса\n"
                    "по веб-разработке, посещение семинара по финансовой \n"
                    "грамотности.\n\n"
                    "Работа - задачи связанные с рабочей деятельностью.\n"
                    "Например: составление еженедельного отчета или де-\n"
                    "ловая встреча.\n\n"
                    "Новое значение категории не должно повторяться.\n\n"
                    "[0] Отмена\n"
                )

                print(change_text)
                user_input_change = input("Новая категория: ")

                if user_input_change == "0":
                    change_task_sett(value)

                if tab.data_validation(column="category",
                                       value=user_input_change,
                                       intention="change",
                                       _id=value):
                    if tab.change_task(_id=value,
                                       column="category",
                                       value=str(user_input_change)):
                        sleep(2)
                        change_task_sett(value)

                else:
                    sleep(2)
                    change(value, option)

        case "due_date":
            while True:
                os.system("cls")
                change_text = (
                    f"{task}\n\n"
                    "Сроки задачи, необходимы для контроля прогресса выпол-\n"
                    "нения задач, а также планирования и распределения ресу-\n"
                    "рсов. Необходимо указать дату в формате YYYY-MM-DD, да-\n"
                    "та должна быть больше или равна сегодняшнему дню.\n\n"
                    "[0] Отмена\n"
                )

                print(change_text)
                user_input_change = input("Новый срок задачи: ")

                if user_input_change == "0":
                    change_task_sett(value)

                if tab.data_validation(column="due_date",
                                       value=user_input_change,
                                       intention="change",
                                       _id=value):
                    if tab.change_task(_id=value,
                                       column="due_date",
                                       value=str(user_input_change)):
                        sleep(2)
                        change_task_sett(value)

                else:
                    sleep(2)
                    change(value, option)

        case "priority":
            while True:
                os.system("cls")
                change_text = (
                    f"{task}\n\n"
                    "Приоритет задачи необходим для определения её значи-\n"
                    "мости и срочности относительно других задач. Он по-\n"
                    "могает фокусироваться на важных задачах, эффективно \n"
                    "распределять время и ресурсы.\n\n"
                    "Принимается одно из 3-х значений:\n\n"
                    "Низкий - низкий приоритет задачи нужен для обозначе-\n"
                    "ния мелких, бытовых задач.\n"
                    "Напиример: записаться на курсы, оплатить интернет.\n\n"
                    "Средний - средний приоритет задачи нужен для обозна-\n"
                    "чения более серьезных задач.\n"
                    "Например: запись к врачу, застраховать автомобиль.\n\n"
                    "Высокий - высокий приоритет задачи нужен для обозна-\n"
                    "чения задач с наивысшим приоритетом.\n"
                    "Например: составить сводный отчет по продажам за ме-\n"
                    "сяц.\n\n"
                    "[0] Отмена\n"
                )

                print(change_text)
                user_input_change = input("Новый приоритет: ")

                if user_input_change == "0":
                    change_task_sett(value)

                if tab.data_validation(column="priority",
                                       value=user_input_change,
                                       intention="change",
                                       _id=value):
                    if tab.change_task(_id=value,
                                       column="priority",
                                       value=str(user_input_change)):
                        sleep(2)
                        change_task_sett(value)

                else:
                    sleep(2)
                    change(value, option)

        case "status":
            while True:
                os.system("cls")
                change_text = (
                    f"{task}\n\n"
                    "Статус задачи позволяет понять, завершена ли задача \n"
                    "или требует внимания. Если задача помечена как \"Не \n"
                    "выполнена\" её нужно завершить до установленного срока.\n"
                    "Статус может включать в себя только одно из значений:\n\n"
                    "Выполнена - задача которая завершена, что не имеет смы-\n"
                    "сла при создании задачи.\n\n"
                    "Не выполнена - задача которая находится в работе или ра\n"
                    "-бота над которой планируется.\n\n"
                    "[0] Отмена\n"
                )

                print(change_text)
                user_input_change = input("Новый статус: ")

                if user_input_change == "0":
                    change_task_sett(value)

                if tab.data_validation(column="status",
                                       value=user_input_change,
                                       intention="change",
                                       _id=value):
                    if tab.change_task(_id=value,
                                       column="status",
                                       value=str(user_input_change)):
                        sleep(2)
                        change_task_sett(value)

                else:
                    sleep(2)
                    change(value, option)


def change_task_sett(value):
    tab = TaskManager()

    while True:
        os.system("cls")
        task = tab.getting_task(value=str(value), option="id")
        change_task_sett_text = (
            f"{task}\n\n"
            f"Выберите, редактируемый раздел:\n\n"
            f"[1] Заголовок\n"
            f"[2] Описание\n"
            f"[3] Категория\n"
            f"[4] Сроки задачи\n"
            f"[5] Приоритет\n"
            f"[6] Статус\n"
            f"[0] Назад\n"
        )

        try:
            print(change_task_sett_text)
            user_input_change_task_sett = int(input(">> "))
        except ValueError:
            print(
                "Введите номер варианта в числовом формате\n"
                "В данном разделе меню, текст не поддерживается."
            )
            sleep(2)
            change_task_sett(value)

        if user_input_change_task_sett == 0:
            change_task()

        match user_input_change_task_sett:
            case 1:
                change(value, option="title")
            case 2:
                change(value, option="description")
            case 3:
                change(value, option="category")
            case 4:
                change(value, option="due_date")
            case 5:
                change(value, option="priority")
            case 6:
                change(value, option="status")


def change_task():
    tab = TaskManager()

    while True:
        os.system("cls")
        change_task_text = (
            f"{tab.getting_task()}\n\n"
            "Укажите идентификатор (ID) задачи, которую требуется "
            "отредактировать.\n\n"
            "[0] Назад\n"
        )

        try:
            print(change_task_text)
            user_input_change_task = int(input(">> "))
        except ValueError:
            print(
                "Введите номер варианта в числовом формате\n"
                "В данном разделе меню, текст не поддерживается."
            )
            sleep(2)
            change_task()

        if user_input_change_task == 0:
            main_menu()

        if tab.getting_task(value=str(user_input_change_task), option="id"):
            change_task_sett(user_input_change_task)
        else:
            sleep(2)
            change_task()


def add_new_task(*args):
    tab = TaskManager()

    title = args[0]
    description = args[1]
    category = args[2]
    due_date = args[3]
    priority = args[4]
    status = args[5]

    while True:
        os.system("cls")
        result_task_text = (
            "Содать новую задачу?\n\n"
            f"Заголовок: {title}\n"
            f"Описание: {description}\n"
            f"Категория: {category}\n"
            f"Сроки задачи: {due_date}\n"
            f"Приоритет: {priority}\n"
            f"Статус: {status}\n\n"
            "[1] Создать задачу\n"
            "[0] Отмена\n"
        )

        try:
            print(result_task_text)
            user_input_final = int(input(">> "))
        except ValueError:
            print(
                "Введите номер варианта в числовом формате\n"
                "В данном разделе меню, текст не поддерживается."
            )
            sleep(2)
            add_new_task(title, description, category,
                         due_date, priority, status)

        match user_input_final:
            case 1:
                tab.add_task(
                    title=title,
                    description=description,
                    category=category,
                    due_date=due_date,
                    priority=priority,
                    status=status
                )
                sleep(2)
                main_menu()
            case 0:
                main_menu()


def create_task():
    tab = TaskManager()

    new_task_title = ""
    new_task_description = ""
    new_task_category = ""
    new_task_due_date = ""
    new_task_priority = ""
    new_task_status = "Не выполнена"

    # Раздел заголовка
    while True:
        os.system("cls")
        create_task_title_text = (
            "Заголовок.\n\n"
            "Заголовок задачи дожен быть не менее 5 символов.\n"
            "Он должен быть информативным, чтобы вам было по-\n"
            "нятно, о чем идет речь.\n\n"
            "[0] Отмена\n"
        )

        print(create_task_title_text)
        ui_title = str(input("Заголовок: "))

        if ui_title == "0":
            main_menu()

        if tab.data_validation(column="title",
                               value=str(ui_title),
                               intention="add"
                               ):
            new_task_title = new_task_title + ui_title
            break
        else:
            sleep(2)

    # Раздел описания
    while True:
        os.system("cls")
        create_task_description_text = (
            "Описание.\n\n"
            "Описание задачи дожно быть не менее 10 символов.\n"
            "Оно должно четко и подробно объяснять суть зада-\n"
            "чи. А также иметь достаточно информации для кор-\n"
            "ректного выполнения.\n\n"
            "[0] Отмена\n"
        )

        print(create_task_description_text)
        ui_description = str(input("Описание: "))

        if ui_description == "0":
            main_menu()

        if tab.data_validation(column="description",
                               value=str(ui_description),
                               intention="add"
                               ):
            new_task_description = new_task_description + ui_description
            break
        else:
            sleep(2)

    # Раздел категории
    while True:
        os.system("cls")
        create_task_category_text = (
            "Категория.\n\n"
            "Категория, необходима для четкого распределения \n"
            "задачи. Категория может включать в себя только \n"
            "одно из значений:\n\n"
            "Личное - задачи связанные с повседневной жизнью.\n"
            "Например: Поход в кино, прогулка, приготовить "
            "ужин.\n\n"
            "Обучение - задачи связанные с получения новых знаний\n"
            "навыков, умений, опыта.\nНапример: Прохождение курса\n"
            "по веб-разработке, посещение семинара по финансовой \n"
            "грамотности.\n\n"
            "Работа - задачи связанные с рабочей деятельностью.\n"
            "Например: составление еженедельного отчета или де-\n"
            "ловая встреча.\n\n"
            "[0] Отмена\n"
        )

        print(create_task_category_text)
        ui_category = str(input("Категория: "))

        if ui_category == "0":
            main_menu()

        if tab.data_validation(column="category",
                               value=str(ui_category),
                               intention="add"
                               ):
            new_task_category = new_task_category + ui_category
            break
        else:
            sleep(4)

    # Раздел даты
    while True:
        os.system("cls")
        create_task_due_date_text = (
            "Сроки задачи.\n\n"
            "Сроки задачи, необходимы для контроля прогресса выпол-\n"
            "нения задач, а также планирования и распределения ресу-\n"
            "рсов. Необходимо указать дату в формате YYYY-MM-DD, да-\n"
            "та должна быть больше или равна сегодняшнему дню.\n\n"
            "[0] Отмена\n"
        )

        print(create_task_due_date_text)
        ui_due_date = str(input("Сроки задачи: "))

        if ui_due_date == "0":
            main_menu()

        if tab.data_validation(column="due_date",
                               value=str(ui_due_date),
                               intention="add"
                               ):
            new_task_due_date = new_task_due_date + ui_due_date
            break
        else:
            sleep(5)

    # Раздел приоритета
    while True:
        os.system("cls")
        create_task_priority_text = (
            "Приоритет.\n\n"
            "Приоритет задачи необходим для определения её значи-\n"
            "мости и срочности относительно других задач. Он по-\n"
            "могает фокусироваться на важных задачах, эффективно \n"
            "распределять время и ресурсы.\n\n"
            "Принимается одно из 3-х значений:\n\n"
            "Низкий - низкий приоритет задачи нужен для обозначе-\n"
            "ния мелких, бытовых задач.\n"
            "Напиример: записаться на курсы, оплатить интернет.\n\n"
            "Средний - средний приоритет задачи нужен для обозна-\n"
            "чения более серьезных задач.\n"
            "Например: запись к врачу, застраховать автомобиль.\n\n"
            "Высокий - высокий приоритет задачи нужен для обозна-\n"
            "чения задач с наивысшим приоритетом.\n"
            "Например: составить сводный отчет по продажам за ме-\n"
            "сяц.\n\n"
            "[0] Отмена\n"
        )

        print(create_task_priority_text)
        user_input_priority = str(input("Приоритет: "))

        if user_input_priority == "0":
            main_menu()

        if tab.data_validation(column="priority",
                               value=str(user_input_priority),
                               intention="add"
                               ):
            new_task_priority = new_task_priority + user_input_priority
            break
        else:
            sleep(5)

    # Раздел статуса
    while True:
        os.system("cls")
        create_task_status_text = (
            "Статус задачи.\n\n"
            "Статус задачи позволяет понять, завершена ли задача \n"
            "или требует внимания. Если задача помечена как \"Не \n"
            "выполнена\" её нужно завершить до установленного срока.\n"
            "Статус может включать в себя только одно из значений:\n\n"
            "Выполнена - задача которая завершена, что не имеет смы-\n"
            "сла при создании задачи.\n\n"
            "Не выполнена - задача которая находится в работе или ра-\n"
            "бота над которой планируется.\n\n"
            "[0] Отмена\n"
        )

        print(create_task_status_text)
        user_input_status = str(input("Статус [Не выполнена]: "))

        if user_input_status == "0":
            main_menu()

        if tab.data_validation(column="status",
                               value=str(user_input_status),
                               intention="add"
                               ):
            new_task_status = new_task_status + user_input_status
            break
        else:
            sleep(5)

    # Добавление задачи в таблицу
    add_new_task(
        new_task_title,
        new_task_description,
        new_task_category,
        new_task_due_date,
        new_task_priority,
        new_task_status
    )


def get_task(option: str = "", value: str = ""):
    tab = TaskManager()

    match option:
        # Вернет все таблицу
        case "":
            return tab.getting_task()

        # Вернет только одну задачу по id
        case "id":
            if tab.data_validation(column="id",
                                   value=value,
                                   intention="search"):
                return tab.getting_task(value=str(value), option="id")

        case "category":
            if tab.data_validation(column="category",
                                   value=value,
                                   intention="search"):
                return tab.getting_task(value=str(value), option="category")

        # Вернет все задачи по статусу
        case "status":
            if tab.data_validation(column="status",
                                   value=value,
                                   intention="search"):
                return tab.getting_task(value=value, option="status")

        # Вернет все задачи по приоритету
        case "priority":
            if tab.data_validation(column="priority",
                                   value=value,
                                   intention="search"):
                return tab.getting_task(value=value, option="priority")

        # Вернет все задачи по ключевым словам
        case "keywords":
            return tab.getting_task(value=value, option="keywords")

        # Вернет все просроченные задачи
        case "due_date":
            return tab.getting_task(option="due_date")


def view_task_by_id():
    while True:
        os.system("cls")
        view_task_by_id_text = (
            f"{get_task()}\n\n"
            "Введите ID задачи, которую нужно найти.\n\n"
            "[0] Назад\n"
        )

        try:
            print(view_task_by_id_text)
            ui_view_task_by_id = int(input(">> "))
        except ValueError:
            print(
                "Введите номер варианта в числовом формате. В\n"
                "данном разделе меню, текст не поддерживается."
            )
            sleep(2)
            view_task_by_id()

        match ui_view_task_by_id:
            case 0:
                viewing_tasks()
            case _:
                os.system("cls")
                res = get_task(option="id",
                               value=ui_view_task_by_id)

                if res is True:
                    ans = (
                        f"{res}\n\n"
                        f"[0] Назад\n"
                    )
                else:
                    ans = (
                        f"{get_task()}\n\n"
                    )
                    sleep(2)
                    view_task_by_id()
                while True:
                    try:
                        os.system("cls")
                        print(ans)
                        int(input(">> "))
                        break
                    except ValueError:
                        print(
                            "Введите номер варианта в числовом формате. В\n"
                            "данном разделе меню, текст не поддерживается."
                        )
                        sleep(2)


def view_task_by_category():
    while True:
        os.system("cls")
        view_task_by_category_text = (
            f"{get_task()}\n\n"
            "Введите категорию задач, которые нужно найти.\n\n"
            "[0] Назад\n"
        )

        print(view_task_by_category_text)
        ui_view_task_by_category = str(input(">> "))

        match ui_view_task_by_category:
            case "0":
                viewing_tasks()
            case _:
                os.system("cls")
                res = get_task(option="category",
                               value=ui_view_task_by_category)
                if res:
                    ans = (
                        f"{res}\n\n"
                        f"[0] Назад\n"
                    )
                else:
                    ans = (
                        f"{get_task()}\n\n"
                    )
                    sleep(2)
                    view_task_by_category()

                while True:
                    try:
                        os.system("cls")
                        print(ans)
                        int(input(">> "))
                        break
                    except ValueError:
                        print(
                            "Введите номер варианта в числовом формате. В\n"
                            "данном разделе меню, текст не поддерживается."
                        )
                        sleep(2)


def view_task_by_status():
    while True:
        os.system("cls")
        view_task_by_status_text = (
            f"{get_task()}\n\n"
            "Введите статус задач, которые нужно найти.\n\n"
            "[0] Назад\n"
        )

        print(view_task_by_status_text)
        ui_view_task_by_status = str(input(">> "))

        match ui_view_task_by_status:
            case "0":
                viewing_tasks()
            case _:
                os.system("cls")
                res = get_task(option="status",
                               value=ui_view_task_by_status)
                if res:
                    ans = (
                        f"{res}\n\n"
                        f"[0] Назад\n"
                    )
                else:
                    ans = (
                        f"{get_task()}\n\n"
                    )
                    sleep(2)
                    view_task_by_status()

                while True:
                    try:
                        os.system("cls")
                        print(ans)
                        int(input(">> "))
                        break
                    except ValueError:
                        print(
                            "Введите номер варианта в числовом формате. В\n"
                            "данном разделе меню, текст не поддерживается."
                        )
                        sleep(2)


def view_task_by_priority():
    while True:
        os.system("cls")
        view_task_by_priority_text = (
            f"{get_task()}\n\n"
            "Введите приоритет задач, которые нужно найти.\n\n"
            "[0] Назад\n"
        )

        print(view_task_by_priority_text)
        ui_view_task_by_priority = str(input(">> "))

        match ui_view_task_by_priority:
            case "0":
                viewing_tasks()
            case _:
                os.system("cls")
                res = get_task(option="priority",
                               value=ui_view_task_by_priority)
                if res:
                    ans = (
                        f"{res}\n\n"
                        f"[0] Назад\n"
                    )
                else:
                    ans = (
                        f"{get_task()}\n\n"
                    )
                    sleep(2)
                    view_task_by_priority()

                while True:
                    try:
                        os.system("cls")
                        print(ans)
                        int(input(">> "))
                        break
                    except ValueError:
                        print(
                            "Введите номер варианта в числовом формате. В\n"
                            "данном разделе меню, текст не поддерживается."
                        )
                        sleep(2)


def view_task_by_keywords():
    while True:
        os.system("cls")
        view_task_by_keywords_text = (
            f"{get_task()}\n\n"
            "Введите ключевое слово, по которому нужно найти задачи\n\n"
            "[0] Назад\n"
        )

        print(view_task_by_keywords_text)
        ui_view_task_by_keywords = str(input(">> "))

        match ui_view_task_by_keywords:
            case "0":
                viewing_tasks()
            case _:
                os.system("cls")
                res = get_task(option="keywords",
                               value=ui_view_task_by_keywords)
                if res:
                    ans = (
                        f"{res}\n\n"
                        f"[0] Назад\n"
                    )
                else:
                    ans = (
                        f"{get_task()}\n\n"
                    )
                    sleep(2)
                    view_task_by_keywords()

                while True:
                    try:
                        os.system("cls")
                        print(ans)
                        int(input(">> "))
                        break
                    except ValueError:
                        print(
                            "Введите номер варианта в числовом формате. В\n"
                            "данном разделе меню, текст не поддерживается."
                        )
                        sleep(2)


def view_task_by_due_date():
    while True:
        os.system("cls")
        view_task_by_due_date_text = (
            f"{get_task(option='due_date')}\n\n"
            "Задачи с истекшим сроком выволнения.\n\n"
            "[0] Назад\n"
        )
        try:
            print(view_task_by_due_date_text)
            ui_view_task_by_due_date = int(input(">> "))
        except ValueError:
            print(
                "Введите номер варианта в числовом формате. В\n"
                "данном разделе меню, текст не поддерживается."
            )
            sleep(2)
            view_task_by_due_date()

        match ui_view_task_by_due_date:
            case 0:
                viewing_tasks()


def viewing_tasks():
    while True:
        os.system("cls")
        viewing_tasks_text = (
            f"{get_task()}\n\n"
            "Вы можете найти интересующие вас задачи, воспользов"
            "авшись поиском по:"
            "Идентификатору (ID) — будет найдена одна задача.\n\n"
            "По категории — будут найдены все задачи, принадлежа"
            "щие\nвыбранной категории.\n\n"
            "По статусу — будут найдены все задачи, принадлежащие "
            "вы-\nбранному статусу.\n\n"
            "По приоритету — будут найдены все задачи, принадлежа"
            "щие\nвыбранному приоритету.\n\n"
            "По ключевым словам — будут найдены все задачи, в кот"
            "орых\nесть указанное слово.\n\n"
            "По просроченной дате — будут сразу выведены все зада"
            "чи с\nистекшим сроком выполнения\n\n"
            "[1] Найти по ID\n"
            "[2] Найти по категории\n"
            "[3] Найти по статусу\n"
            "[4] Найти по приоритету\n"
            "[5] Найти по ключевым словам\n"
            "[6] Найти по истекшему сроку\n"
            "[0] Назад\n"
        )

        try:
            print(viewing_tasks_text)
            ui_viewing_tasks = int(input(">> "))
        except ValueError:
            print(
                "Введите номер варианта в числовом формате. В\n"
                "данном разделе меню, текст не поддерживается."
            )
            sleep(2)
            viewing_tasks()

        if ui_viewing_tasks == 0:
            main_menu()

        match ui_viewing_tasks:
            case 1:
                view_task_by_id()
            case 2:
                view_task_by_category()
            case 3:
                view_task_by_status()
            case 4:
                view_task_by_priority()
            case 5:
                view_task_by_keywords()
            case 6:
                view_task_by_due_date()


def main_menu():
    while True:
        os.system("cls")
        main_menu_text = (
            "TaskManager — это модуль для создания, управления\n"
            "и отслеживания задач. Он предоставляет функциона-\n"
            "льность для работы с задачами в формате JSON, по-\n"
            "зволяя организовывать вашу работу или личные дела.\n\n"
            "Управление:\n"
            "[1] Просмотр задач\n"
            "[2] Создание задач\n"
            "[3] Изменение задач\n"
            "[4] Удаление задач\n"
            "[0] Выход\n"
        )

        try:
            print(main_menu_text)
            user_input_main_menu = int(input(">> "))
        except ValueError:
            print(
                "Введите номер варианта в числовом формате. В\n"
                "данном разделе меню, текст не поддерживается."
            )
            sleep(2)
            main_menu()

        match user_input_main_menu:
            case 1:
                viewing_tasks()
            case 2:
                create_task()
            case 3:
                change_task()
                pass
            case 4:
                delete_task()
                pass
            case 0:
                print("Goodbuy!")
                quit()


def main():
    main_menu()


if __name__ == "__main__":
    main()
