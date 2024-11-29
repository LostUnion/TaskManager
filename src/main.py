from typing import Optional, List
import json
import argparse

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
    """Описание класса TaskManager"""

    pretty_printed_JSON = True

    def __init__(self, path: str ="data.json", ):
        """Инициализируем класс"""
        self.path = path

    def get_all_tasks(self):
        """Получение всех текущих задач из файла data.json."""
    
        with open(self.path, "r", encoding="utf-8") as file:  # Открытие файла data.json для чтения
            data = json.load(file)  # Используем json.load для загрузки JSON из файла

            if self.pretty_printed_JSON:  # Вывод в формате pretty-printed JSON, если pretty_printed_JSON = True
                print(json.dumps(data, indent=4, ensure_ascii=False))
            else:  # Вывод в пользовательском формате, если pretty_printed_JSON = False
                for index, task in enumerate(data):
                    formatting_data = (
                        f"ID задания: {task['id']}\n"
                        f"Название: {task['title']}\n"
                        f"Описание: {task['description']}\n"
                        f"Категория: {task['category']}\n"
                        f"Срок выполнения: {task['due_date']}\n"
                        f"Приоритет: {task['priority']}\n"
                        f"Статус задачи: {task['status']}\n"
                    )
                    print(formatting_data)

task = TaskManager()
task.get_all_tasks()
