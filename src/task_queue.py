from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator

from src.models import Task, TaskStatus


class TaskQueue:
    """Пользовательская коллекция задач с поддержкой повторной итерации и ленивых фильтров"""

    def __init__(self, tasks: Iterable[Task] = ()) -> None:
        self._tasks: list[Task] = list(tasks)

    def add(self, task: Task) -> None:
        """Добавить задачу в очередь"""
        self._tasks.append(task)

    def extend(self, tasks: Iterable[Task]) -> None:
        """Добавить несколько задач в очередь"""
        self._tasks.extend(tasks)

    def __iter__(self) -> Iterator[Task]:
        """Повторяемый итератор по задачам очереди."""
        for task in self._tasks:
            yield task

    def __len__(self) -> int:
        return len(self._tasks)

    def __repr__(self) -> str:
        return f"TaskQueue(size={len(self._tasks)})"

    def filter(self, predicate: Callable[[Task], bool]) -> Iterator[Task]:
        """Ленивый фильтр по произвольному условию"""
        for task in self._tasks:
            if predicate(task):
                yield task

    def filter_by_status(self, status: TaskStatus) -> Iterator[Task]:
        """Лениво отфильтровать задачи по статусу"""
        yield from self.filter(lambda task: task.status == status)

    def filter_by_priority(
        self,
        min_priority: int | None = None,
        max_priority: int | None = None,
    ) -> Iterator[Task]:
        """Отфильтровать задачи по диапазону приоритета"""
        for task in self._tasks:
            if min_priority is not None and task.priority < min_priority:
                continue
            if max_priority is not None and task.priority > max_priority:
                continue
            yield task