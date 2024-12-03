import json
import pytest

from unittest.mock import mock_open, patch

from src.task_manager.task_manager import TaskManager

# Мок-данные для тестов
MOCK_DATA = [
    {
        "id": 1,
        "title": "Задача 1",
        "description": "Описание задачи 1",
        "category": "Работа",
        "priority": "Высокий",
        "status": "Не выполнена",
        "due_date": "2024-12-25"
    },
    {
        "id": 2,
        "title": "Задача 2",
        "description": "Описание задачи 2",
        "category": "Личное",
        "priority": "Низкий",
        "status": "Выполнена",
        "due_date": "2024-11-30"
    }
]


@pytest.fixture()
def mock_task_manager():
    """Фикстура для создания объекта TaskManager с мок-данными."""
    with patch("builtins.open",
               mock_open(read_data=json.dumps(MOCK_DATA))
               ):
        manager = TaskManager()
        manager.path = "data.json"
        manager.pretty_printed_JSON = True
        yield manager

# GETTING_TASKS


def test_getting_tasks(mock_task_manager):
    """Тест: получение всех задач без фильтров."""
    result = mock_task_manager.getting_task()
    assert isinstance(result, str)
    assert "Задача 1" in result
    assert "Задача 2" in result


def test_getting_task_by_id(mock_task_manager):
    """Тест: получение задачи по id."""
    result = mock_task_manager.getting_task(value="1", option="id")
    assert isinstance(result, str)
    assert "Задача 1" in result
    assert "Задача 2" not in result


def test_getting_task_by_category(mock_task_manager):
    """Тест: получение задачи по category."""
    result = mock_task_manager.getting_task(
        value="Работа",
        option="category"
    )
    assert isinstance(result, str)
    assert "Работа" in result
    assert "Личное" not in result


def test_getting_task_by_category_empty(mock_task_manager):
    """Тест: получение задачи по category при условии что value пустое."""
    result = mock_task_manager.getting_task(value=" ", option="category")
    assert result is False


def test_getting_task_by_priority(mock_task_manager):
    """Тест: получение задачи по priority."""
    result = mock_task_manager.getting_task(
        value="Высокий",
        option="priority"
    )
    assert isinstance(result, str)
    assert "Высокий" in result
    assert "Низкий" not in result


def test_getting_task_by_priority_empty(mock_task_manager):
    """Тест: получение задачи по priority при условии что value пустое."""
    result = mock_task_manager.getting_task(value=" ", option="priority")
    assert result is False


def test_getting_task_by_status(mock_task_manager):
    """Тест: получение задачи по status."""
    result = mock_task_manager.getting_task(
        value="Не выполнена",
        option="status"
    )
    assert isinstance(result, str)
    assert "Не выполнена" in result
    assert "Выполнена" not in result


def test_getting_task_by_status_empty(mock_task_manager):
    """Тест: получение задачи по status при условии что value пустое.."""
    result = mock_task_manager.getting_task(value=" ", option="status")
    assert result is False


def test_getting_task_due_date(mock_task_manager):
    """Тест: получение задач по просроченной дате."""
    result = mock_task_manager.getting_task(option="due_date")
    assert isinstance(result, str)
    assert "Задача 2" in result  # Дата `2024-11-30` просроченна
    assert "Задача 1" not in result


def test_getting_task_empty_option(mock_task_manager):
    """Тест: вызов функции с пустым `option`, но заполненным `value`."""
    result = mock_task_manager.getting_task(value="1", option="")
    assert result is False


def test_getting_task_empty_value_option(mock_task_manager):
    """Тест: вызов функции с пустым `value` и `option`."""
    result = mock_task_manager.getting_task(value=" ", option=" ")
    assert isinstance(result, str)


def test_getting_task_invalid_value(mock_task_manager):
    """Тест: вызов функции с пустым `value` и `option`."""
    result = mock_task_manager.getting_task(value="99", option="id")
    assert result is False

# ADD_TASK


def test_add_task_success(mock_task_manager):
    """Тест: успешное добавление задачи."""
    result = mock_task_manager.add_task(
        title="Новая задача",
        description="Описание новой задачи",
        category="Личное",
        due_date="2024-12-30",
        priority="Средний",
        status="Не выполнена"
    )
    assert result is True


def test_add_task_empty_title(mock_task_manager):
    """Тест: добавление задачи с пустым заголовком."""
    result = mock_task_manager.add_task(
        title="      ",
        description="Описание задачи",
        category="Работа",
        due_date="2024-12-30",
        priority="Средний",
        status="Не выполнена"
    )
    # Более 5-ти пробелов
    assert result is False


def test_add_task_empty_description(mock_task_manager):
    """Тест: добавление задачи с пустым описанием."""
    result = mock_task_manager.add_task(
        title="Задача",
        description="               ",
        category="Работа",
        due_date="2024-12-30",
        priority="Средний",
        status="Не выполнена"
    )
    # Более 10-ти пробелов
    assert result is False


def test_add_task_empty_category(mock_task_manager):
    """Тест: добавление задачи с пустой категорией."""
    result = mock_task_manager.add_task(
        title="Задача",
        description="Описание задачи",
        category="      ",
        due_date="2024-12-30",
        priority="Средний",
        status="Не выполнена"
    )
    # Более 2-х пробелов
    assert result is False


def test_add_task_invalid_category(mock_task_manager):
    """Тест: добавление задачи с пустой категорией."""
    result = mock_task_manager.add_task(
        title="Задача",
        description="Описание задачи",
        category="Некорректная категория",
        due_date="2024-12-30",
        priority="Средний",
        status="Не выполнена"
    )
    # Доступны: "Работа", "Личное", "Обучение"
    assert result is False


def test_add_task_empty_due_date(mock_task_manager):
    """Тест: добавление задачи с недопустимой датой выполнения."""
    result = mock_task_manager.add_task(
        title="Задача",
        description="Описание задачи",
        category="Работа",
        due_date="    ",
        priority="Средний",
        status="Не выполнена"
    )
    # Более 2-х пробелов
    assert result is False


def test_add_task_invalid_due_date(mock_task_manager):
    """Тест: добавление задачи с недопустимой датой выполнения."""
    result = mock_task_manager.add_task(
        title="Задача",
        description="Описание задачи",
        category="Работа",
        due_date="Некорректная формат",
        priority="Средний",
        status="Не выполнена"
    )
    # Формат: YYYY-MM-DD
    assert result is False


def test_add_task_past_due_date(mock_task_manager):
    """Тест: добавление задачи с недопустимой датой из прошлого."""
    result = mock_task_manager.add_task(
        title="Задача",
        description="Описание задачи",
        category="Работа",
        due_date="1998-05-13",
        priority="Средний",
        status="Не выполнена"
    )
    # Доступны настоящая и будущая даты
    assert result is False


def test_add_task_empty_priority(mock_task_manager):
    """Тест: добавление задачи с пустым приоритетом задачи."""
    result = mock_task_manager.add_task(
        title="Задача",
        description="Описание задачи",
        category="Работа",
        due_date="2077-01-01",
        priority="     ",
        status="Не выполнена"
    )
    # Более 2-х пробелов
    assert result is False


def test_add_task_invalid_priority(mock_task_manager):
    """Тест: добавление задачи с некорректным приоритетом задачи."""
    result = mock_task_manager.add_task(
        title="Задача",
        description="Описание задачи",
        category="Работа",
        due_date="2077-01-01",
        priority="Некорректный приоритет",
        status="Не выполнена"
    )
    # Доступны: "Низкий", "Средний", "Высокий"
    assert result is False


def test_add_task_empty_status(mock_task_manager):
    """Тест: добавление задачи с пустым статусом."""
    result = mock_task_manager.add_task(
        title="Задача",
        description="Описание задачи",
        category="Работа",
        due_date="2077-01-01",
        priority="Низкий",
        status="     "
    )
    assert result is False


def test_add_task_invalid_status(mock_task_manager):
    """Тест: добавление задачи с некорректным статусом."""
    result = mock_task_manager.add_task(
        title="Задача",
        description="Описание задачи",
        category="Работа",
        due_date="2077-01-01",
        priority="Низкий",
        status="Некорректный статус"
    )
    # Доступны: "Выполнена", "Не выполнена"
    assert result is False

# DELETE_TASK


def test_delete_task_by_id_success(mock_task_manager):
    """Тест: успешное удаление задачи по ID."""
    with patch("builtins.open",
               mock_open(read_data=json.dumps(MOCK_DATA))
               ) as mock_file:
        result = mock_task_manager.delete_task(value="1", choice="id")

        # Проверка успешного результата
        assert result is True

        # Проверка открытия файла на запись
        mock_file.assert_called_with("data.json", "w", encoding="utf-8")

        # Проверка финальных данных, записанных в файл
        written_data = "".join(
            call.args[0] for call in mock_file().write.mock_calls
        )

        # Запись в файл
        updated_data = json.loads(written_data)

        # Проверка на кол-во оставшихся задач
        assert len(updated_data) == 1
        assert updated_data[0]["id"] == 2


def test_delete_task_by_category_success(mock_task_manager):
    """Тест: успешное удаление задач по категории."""
    with patch("builtins.open",
               mock_open(read_data=json.dumps(MOCK_DATA))
               ) as mock_file:
        result = mock_task_manager.delete_task(value="Работа",
                                               choice="category")

        # Проверка успешного результата
        assert result is True

        # Проверка открытия файла на запись
        mock_file.assert_called_with("data.json", "w", encoding="utf-8")

        # Проверка финальных данных, записанных в файл
        written_data = "".join(
            call.args[0] for call in mock_file().write.mock_calls
        )

        # Запись в файл
        updated_data = json.loads(written_data)

        # Проверка на кол-во оставшихся задач
        assert len(updated_data) == 1
        assert updated_data[0]["category"] == "Личное"


def test_delete_task_empty_parametr(mock_task_manager):
    """Тест: удаление задачи с пустыми параметрами."""
    result = mock_task_manager.delete_task(value="   ", choice="   ")
    assert result is False


def test_delete_task_empty_parametr_id(mock_task_manager):
    """Тест: удаление задачи с пустым параметром value."""
    result = mock_task_manager.delete_task(value="   ", choice="id")
    assert result is False


def test_delete_task_empty_parametr_choice(mock_task_manager):
    """Тест: удаление задачи с пустым параметром choice."""
    result = mock_task_manager.delete_task(value="1", choice="    ")
    assert result is False


def test_delete_task_invalid_id(mock_task_manager):
    """Тест: удаление задачи с некорректным параметром id."""
    result = mock_task_manager.delete_task(
        value="Некорректное значение",      # Допускаются только цифры
        choice="id"
    )
    assert result is False


def test_delete_task_empty_invalid_choice(mock_task_manager):
    """Тест: удаление задачи с некорректным параметром choice."""
    result = mock_task_manager.delete_task(
        value="1",
        choice="Некорректное значение"      # Доступны: "id", "category"
    )
    assert result is False


def test_delete_task_out_id(mock_task_manager):
    """Тест: удаление задачи с несуществующим id."""
    result = mock_task_manager.delete_task(value="99", choice="id")
    assert result is False


def test_delete_task_invalid_category(mock_task_manager):
    """Тест: удаление задачи с некорректной категорией."""
    result = mock_task_manager.delete_task(value="Некорректная категория",
                                           choice="category")
    assert result is False


def test_delete_task_out_category(mock_task_manager):
    """Тест: удаление задачи с отсутствующей доступной категорией."""
    result = mock_task_manager.delete_task(value="Обучение",
                                           choice="category")
    assert result is False

# CHANGE_TASK


def test_change_title_task_success(mock_task_manager):
    """Тест: успешное изменение заголовка задачи."""
    with patch("builtins.open",
               mock_open(read_data=json.dumps(MOCK_DATA))
               ) as mock_file:
        result = mock_task_manager.change_task(_id=1, column="title",
                                               value="Новая задача")

        # Проверка успешного результата
        assert result is True

        # Проверка открытия файла на запись
        mock_file.assert_called_with("data.json", "w", encoding="utf-8")

        # Проверка финальных данных, записанных в файл
        written_data = "".join(
            call.args[0] for call in mock_file().write.mock_calls
        )

        # Запись в файл
        updated_data = json.loads(written_data)

        # Проверка что задача обновлена
        assert updated_data[0]["title"] == "Новая задача"
        assert updated_data[1]["title"] == "Задача 2"


def test_change_description_task_success(mock_task_manager):
    """Тест: успешное изменение описания задачи."""
    with patch("builtins.open",
               mock_open(read_data=json.dumps(MOCK_DATA))
               ) as mock_file:
        result = mock_task_manager.change_task(_id=1, column="description",
                                               value="Новое Описание")

        # Проверка успешного результата
        assert result is True

        # Проверка открытия файла на запись
        mock_file.assert_called_with("data.json", "w", encoding="utf-8")

        # Проверка финальных данных, записанных в файл
        written_data = "".join(
            call.args[0] for call in mock_file().write.mock_calls
        )

        # Запись в файл
        updated_data = json.loads(written_data)

        # Проверка что задача обновлена
        assert updated_data[0]["description"] == "Новое Описание"
        assert updated_data[1]["description"] == "Описание задачи 2"


def test_change_category_task_success(mock_task_manager):
    """Тест: успешное изменение категории задачи."""
    with patch("builtins.open",
               mock_open(read_data=json.dumps(MOCK_DATA))
               ) as mock_file:
        result = mock_task_manager.change_task(_id=1,
                                               column="category",
                                               value="Обучение")

        # Проверка успешного результата
        assert result is True

        # Проверка открытия файла на запись
        mock_file.assert_called_with("data.json", "w", encoding="utf-8")

        # Проверка финальных данных, записанных в файл
        written_data = "".join(
            call.args[0] for call in mock_file().write.mock_calls
        )

        # Запись в файл
        updated_data = json.loads(written_data)

        # Проверка что задача обновлена
        assert updated_data[0]["category"] == "Обучение"
        assert updated_data[1]["category"] == "Личное"


def test_change_due_date_task_success(mock_task_manager):
    """Тест: успешное изменение сроков задачи."""
    with patch("builtins.open",
               mock_open(read_data=json.dumps(MOCK_DATA))
               ) as mock_file:
        result = mock_task_manager.change_task(_id=1,
                                               column="due_date",
                                               value="2077-01-01")

        # Проверка успешного результата
        assert result is True

        # Проверка открытия файла на запись
        mock_file.assert_called_with("data.json", "w", encoding="utf-8")

        # Проверка финальных данных, записанных в файл
        written_data = "".join(
            call.args[0] for call in mock_file().write.mock_calls
        )

        # Запись в файл
        updated_data = json.loads(written_data)

        # Проверка что задача обновлена
        assert updated_data[0]["due_date"] == "2077-01-01"
        assert updated_data[1]["due_date"] == "2024-11-30"


def test_change_priority_task_success(mock_task_manager):
    """Тест: успешное изменение приоритета задачи."""
    with patch("builtins.open",
               mock_open(read_data=json.dumps(MOCK_DATA))
               ) as mock_file:
        result = mock_task_manager.change_task(_id=1,
                                               column="priority",
                                               value="Средний")

        # Проверка успешного результата
        assert result is True

        # Проверка открытия файла на запись
        mock_file.assert_called_with("data.json", "w", encoding="utf-8")

        # Проверка финальных данных, записанных в файл
        written_data = "".join(
            call.args[0] for call in mock_file().write.mock_calls
        )

        # Запись в файл
        updated_data = json.loads(written_data)

        # Проверка что задача обновлена
        assert updated_data[0]["priority"] == "Средний"
        assert updated_data[1]["priority"] == "Низкий"


def test_change_status_task_success(mock_task_manager):
    """Тест: успешное изменение статуса задачи."""
    with patch("builtins.open",
               mock_open(read_data=json.dumps(MOCK_DATA))
               ) as mock_file:
        result = mock_task_manager.change_task(_id=1,
                                               column="status",
                                               value="Выполнена")

        # Проверка успешного результата
        assert result is True

        # Проверка открытия файла на запись
        mock_file.assert_called_with("data.json", "w", encoding="utf-8")

        # Проверка финальных данных, записанных в файл
        written_data = "".join(
            call.args[0] for call in mock_file().write.mock_calls
        )

        # Запись в файл
        updated_data = json.loads(written_data)

        # Проверка что задача обновлена
        assert updated_data[0]["status"] == "Выполнена"
        assert updated_data[1]["status"] == "Выполнена"


def test_change_status_task_empty_id(mock_task_manager):
    """Тест: изменение задачи при пустом id."""
    with patch("builtins.open",
               mock_open(read_data=json.dumps(MOCK_DATA))
               ):
        result = mock_task_manager.change_task(_id="   ",
                                               column="status",
                                               value="Выполнена")

        # Проверка что валидация не прошла
        assert result is False


def test_change_status_task_invalid_id(mock_task_manager):
    """Тест: изменение задачи при некорректном id."""
    with patch("builtins.open",
               mock_open(read_data=json.dumps(MOCK_DATA))
               ):
        result = mock_task_manager.change_task(_id="Некорректноe значение",
                                               column="status",
                                               value="Выполнена")

        # Проверка что валидация не прошла
        assert result is False


def test_change_status_task_empty_column(mock_task_manager):
    """Тест: изменение задачи при пустом параметре column."""
    with patch("builtins.open",
               mock_open(read_data=json.dumps(MOCK_DATA))
               ):
        result = mock_task_manager.change_task(_id="1",
                                               column="  ",
                                               value="Выполнена")

        # Проверка что валидация не прошла
        assert result is False


def test_change_status_task_invalid_column(mock_task_manager):
    """Тест: изменение задачи при некорректном параметре column."""
    with patch("builtins.open",
               mock_open(read_data=json.dumps(MOCK_DATA))
               ):
        result = mock_task_manager.change_task(_id="1",
                                               column="Некорректноe значение",
                                               value="Выполнена")
        # Доступны: "title", "description", "category",
        # "due_date", "priority", "status"

        # Проверка что валидация не прошла
        assert result is False


def test_change_status_task_empty_value(mock_task_manager):
    """Тест: изменение задачи при пустом параметре value."""
    with patch("builtins.open",
               mock_open(read_data=json.dumps(MOCK_DATA))
               ):
        result = mock_task_manager.change_task(_id="1",
                                               column="status",
                                               value="   ")

        # Проверка что валидация не прошла
        assert result is False


def test_change_status_task_doubles(mock_task_manager):
    """Тест: изменение задачи при повторяющихся значениях."""
    with patch("builtins.open",
               mock_open(read_data=json.dumps(MOCK_DATA))
               ):
        result = mock_task_manager.change_task(_id="1",
                                               column="status",
                                               value="Не выполнена")

        # Проверка что валидация не прошла
        assert result is False
