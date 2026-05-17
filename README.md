
# Лабораторная работа №3: Очередь задач — итераторы и генераторы

**Цель**: Освоить реализацию пользовательских коллекций, протокола итерации и ленивой обработки данных с помощью генераторов

**Описание**: В этом проекте на базе предыдущих лабораторных работ реализована очередь задач `TaskQueue`, поддерживающая повторную итерацию, ленивую фильтрацию по статусу и приоритету, а также совместимость c конструкциями Python. В проекте сохранена  модель `Task` с инкапсуляцией и валидацией, а также источники задач и подсистема приёма задач

## 1) Установка проекта локально

```
git clone https://github.com/TheVailen/python_lab3_tasksqueue
cd python_lab3_tasksqueue
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) Что добавлено и изменено

| Категория                      | Функции/Классы                                                  |
| :----------------------------- | :-------------------------------------------------------------- |
| **Пользовательская коллекция** | `TaskQueue`                                                     |
| **Итерация**                   | `__iter__`, поддержка повторного обхода                         |
| **Операции очереди**           | `add`, `extend`, `__len__`, `__repr__`                          |
| **Ленивые фильтры**            | `filter`, `filter_by_status`, `filter_by_priority`              |
| **Генераторы**                 | использование `yield` в очереди и источниках                    |
| **Модель задачи**              | `Task`, `TaskStatus`, вычисляемые свойства и защита инвариантов |
| **Источники задач**            | `JsonlFileSource`, `GeneratorSource`, `ApiStubSource`           |
| **Подсистема приёма**          | `TaskIntake`                                                    |
| **Тестирование**               | `test_task_queue.py`, а также тесты модели, источников и intake |

### Архитектурные решения

**Пользовательская коллекция `TaskQueue`:**

* `TaskQueue` хранит задачи и предоставляет повторяемый интерфейс итерации
* очередь совместима со стандартными конструкциями Python: `for`, `list`, `sum`, генераторные выражения
* очередь может быть повторно пройдена несколько раз без потери данных

**Протокол итерации:**

* метод `__iter__` возвращает итератор по задачам очереди
* корректно обрабатывается завершение итерации через `StopIteration`
* поведение очереди соответствует ожидаемому поведению коллекций Python

**Ленивые фильтры через генераторы:**

* `filter`, `filter_by_status` и `filter_by_priority` не создают промежуточные списки
* элементы выдаются по мере запроса
* это позволяет эффективнее работать с большими объёмами задач

**Переиспользование предыдущих лабораторных работ:**

* модель `Task` из лабы 2 используется как элемент очереди
* источники задач и `TaskIntake` из лабы 1/2 могут быть использованы для наполнения очереди
* архитектура остаётся расширяемой: можно добавлять новые источники и новые способы фильтрации без изменения существующего кода

## 3) Запуск программы

```bash
python -m src.main
```

### Вывод

```text
=== Источники задач ===
file-1: {"action": "process_order", "order_id": 101}
file-2: {"action": "send_notification", "user_id": 7}
gen-1: {"action": "recalculate_stats"}
gen-2: {"action": "check_resource"}
api-1: {"action": "sync_external_data"}
api-2: {"action": "rebuild_cache"}

=== Модель Task: дескрипторы и @property ===
Создана: Task(id='demo-1', priority=7, status='pending', is_ready=True)
is_ready=True, is_active=False, is_finished=False
label (non-data descriptor): task:demo-1
После start(): status=in_progress, is_active=True
После complete(): status=done, is_finished=True

Non-data descriptor до перекрытия: task:demo-2
Non-data descriptor после перекрытия: custom-label

=== Очередь задач: итераторы и генераторы ===
Все задачи в очереди:
q-1: priority=3, status=pending
q-2: priority=9, status=pending
q-3: priority=6, status=in_progress
Повторный обход очереди:
q-1
q-2
q-3
Фильтр по статусу IN_PROGRESS:
q-3
Фильтр по приоритету >= 5:
q-2
q-3

=== Исключения при нарушении инвариантов ===
InvalidTaskIdError: id должен быть непустой строкой, получено ''
InvalidPriorityError: Приоритет должен быть от 1 до 10, получено 99
InvalidStatusTransitionError: Нельзя перейти из 'pending' в 'done'
```

## 4) Тесты

```bash
python -m pytest -v
```

### Тесты с процентом покрытия

```bash
python -m pytest --cov=src --cov-report=term-missing
```

### Проверка только очереди задач

```bash
python -m pytest tests/test_task_queue.py -v
```

## 5) Запуск в Docker

```bash
docker build -t python_lab3_tasksqueue .
docker run --rm python_lab3_tasksqueue
docker run --rm python_lab3_tasksqueue python -m pytest tests -v
```

### Тесты с покрытием в Docker

```bash
docker run --rm python_lab3_tasksqueue python -m pytest --cov=src --cov-report=term-missing
```

## 6) Структура проекта

```text
python_lab3/
├── src/
│   ├── contracts.py
│   ├── descriptors.py
│   ├── exceptions.py
│   ├── intake.py
│   ├── main.py
│   ├── models.py
│   ├── sources.py
│   └── task_queue.py
├── tests/
│   ├── test_intake.py
│   ├── test_main.py
│   ├── test_models.py
│   ├── test_sources.py
│   └── test_task_queue.py
├── Dockerfile
└── requirements.txt
```

## 7) Чему я научился

* Реализовал пользовательскую коллекцию `TaskQueue`, совместимую со стандартными механизмами итерации Python
* Разобрался с протоколом итерации: `__iter__`, `iter()`, `next()` и `StopIteration`
* Научился проектировать повторно итерируемые коллекции
* Реализовал ленивую фильтрацию задач через генераторы без создания лишних промежуточных структур данных
* Научился использовать генераторы для более эффективной обработки больших объёмов данных
* Переиспользовал модель `Task`, построенную в предыдущей лабораторной работе, как основу для новой коллекции
* Связал вместе источники задач, подсистему приёма и очередь задач в единую расширяемую архитектуру
* Закрепил навыки тестирования пользовательских коллекций, итераторов и генераторных функций
