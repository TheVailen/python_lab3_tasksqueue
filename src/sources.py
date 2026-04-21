from __future__ import annotations

import json
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.models import Task


@dataclass(frozen=True)
class JsonlFileSource:
    """Источник задач из JSONL-файла."""

    path: Path
    name: str = "file-jsonl"

    def get_tasks(self) -> Iterable[Task]:
        with self.path.open("r", encoding="utf-8") as file:
            for line_no, raw_line in enumerate(file, start=1):
                line = raw_line.strip()
                if not line:
                    continue

                try:
                    data = json.loads(line)
                except json.JSONDecodeError as error:
                    raise ValueError(
                        f"Invalid JSON in {self.path} at line {line_no}: {error.msg}"
                    ) from error

                if not isinstance(data, dict):
                    raise ValueError(
                        f"Task in {self.path} at line {line_no} must be a JSON object"
                    )

                if "id" not in data or "payload" not in data:
                    raise ValueError(
                        f"Task in {self.path} at line {line_no} must contain id and payload"
                    )

                yield Task(id=str(data["id"]), payload=data["payload"])


TaskProducer = Callable[[], Iterable[Task]]


@dataclass(frozen=True)
class GeneratorSource:
    """Источник задач, которые генерируются программно."""

    producer: TaskProducer
    name: str = "generator"

    def get_tasks(self) -> Iterable[Task]:
        return self.producer()


@dataclass(frozen=True)
class ApiStubSource:
    """Источник задач из API-заглушки."""

    response: list[dict[str, Any]] = field(default_factory=list)
    name: str = "api-stub"

    def get_tasks(self) -> Iterable[Task]:
        for index, item in enumerate(self.response, start=1):
            if not isinstance(item, dict):
                raise ValueError(f"API item #{index} must be an object")

            if "payload" not in item:
                raise ValueError(f"API item #{index} must contain payload")

            task_id = str(item.get("id", f"api-{index}"))
            yield Task(id=task_id, payload=item["payload"])