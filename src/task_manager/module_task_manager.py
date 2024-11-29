from typing import Optional, List
import json
from prettytable import PrettyTable

table = PrettyTable()
table.field_names = ["ID", "Title", "Description", "Category", "Due_date", "Priority", "Status"]
# print(table)



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

class TaskManager():

    pretty_printed_JSON = False

    """Описание класса TaskManager"""

    def __init__(self, path: str ="data/data.json", ):
        """Инициализируем класс"""
        self.path = path

    def get_task(self, value: str = ""):
        """Получение всех текущих задач из файла data.json или получение по значению"""

        with open(self.path, "r", encoding="utf-8") as file:  # Открытие файла data.json для чтения
            data = json.load(file)  # Используем json.load для загрузки JSON из файла

        # Функция форматирования задач в пользовательский вывод
        def format_tasks(tasks):
            table.clear_rows()
            for task in tasks:
                table.add_row([task['id'], task['title'], task['description'], task['category'], task['due_date'], task['priority'], task['status']])
            return table

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
            
    def add_task(self, title: str = "", description: str = "", category: str = "", due_date: str = "", priority: str = "", status: str = "Не выполнена"):
        """Функция добавления новой задачи"""
        
        new_task = Task(
            title=title,
            description=description,
            category=category,
            due_date=due_date,
            priority=priority,
            status=status
        )

        with open(self.path, "r", encoding="utf-8") as file:
            data = json.load(file)

        new_task.id = len(data) + 1

        data.append(new_task.__dict__)

        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return f"Задача \"{title}\" добавлена с ID {new_task.id}!"
    
    def change_task(self):
        """Функция изменения задачи"""
        # Функция форматирования задач в пользовательский вывод
        def format_tasks(tasks):
            table.clear_rows()
            for task in tasks:
                table.add_row([task['id'], task['title'], task['description'], task['category'], task['due_date'], task['priority'], task['status']])
            return table

        with open(self.path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return format_tasks(data)

