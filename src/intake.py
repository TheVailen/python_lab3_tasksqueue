from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Optional

from src.models import Task
from src.contracts import TaskSource


class TaskIntake:
    """Подсистема приёма задач из разных источников."""

    def __init__(self, sources: Optional[Sequence[TaskSource]] = None) -> None:
        self._sources: list[TaskSource] = []
        for source in sources or []:
            self.add_source(source)

    def add_source(self, source: TaskSource) -> None:
        """Добавить источник после runtime-проверки контракта."""
        if not isinstance(source, TaskSource):
            raise TypeError("Object does not satisfy TaskSource protocol")
        self._sources.append(source)

    def iter_tasks(self) -> Iterable[Task]:
        """Итерировать задачи из всех подключённых источников."""
        for source in self._sources:
            yield from source.get_tasks()