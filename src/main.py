from typing import Optional, List
import json

class Task:
    """Описание класса Task"""

    def __init__(self, id: Optional[int] = None, title: str = "", description: str = "", category: str = "", due_date: str = "", priority: str = "", status: str = "Не выполнена"):
        self.id = None
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

class TaskManager:

    pretty_printed_JSON = False

    """Описание класса TaskManager"""

    def __init__(self, path: str ="data.json", ):
        """Инициализируем класс"""
        self.path = path

    def get_task(self, value: str = ""):
        """Получение всех текущих задач из файла data.json или получение по значению"""

        with open(self.path, "r", encoding="utf-8") as file:  # Открытие файла data.json для чтения
            data = json.load(file)  # Используем json.load для загрузки JSON из файла

        # Функция форматирования задач в пользовательский вывод
        def format_tasks(tasks):
            formatting_data = ""
            for task in tasks:
                formatting_data += (
                    f"ID задания: {task['id']}\n"
                    f"Название: {task['title']}\n"
                    f"Описание: {task['description']}\n"
                    f"Категория: {task['category']}\n"
                    f"Срок выполнения: {task['due_date']}\n"
                    f"Приоритет: {task['priority']}\n"
                    f"Статус задачи: {task['status']}\n\n"
                )
            return formatting_data.strip()

        if value:
            new_data = [task for task in data if task['category'] == value]
            if new_data:
                if self.pretty_printed_JSON:
                    return json.dumps(new_data, indent=4, ensure_ascii=False)
                else:
                    return format_tasks(new_data)
            else:
                return f"Значение \"{value}\" не было найдено в файле."
        else:
            if self.pretty_printed_JSON:
                return json.dumps(data, indent=4, ensure_ascii=False)
            else:
                return format_tasks(data)

            
task = TaskManager()
t = task.get_task()
print(t)
