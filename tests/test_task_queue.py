from __future__ import annotations

from collections.abc import Iterator

import pytest

from src.models import Task, TaskStatus
from src.task_queue import TaskQueue


def test_queue_iterates_in_insertion_order() -> None:
    queue = TaskQueue([
        Task(id="t-1", priority=3),
        Task(id="t-2", priority=8),
        Task(id="t-3", priority=5),
    ])

    assert [task.id for task in queue] == ["t-1", "t-2", "t-3"]


def test_queue_supports_multiple_passes() -> None:
    queue = TaskQueue([
        Task(id="t-1"),
        Task(id="t-2"),
    ])

    first_pass = [task.id for task in queue]
    second_pass = [task.id for task in queue]

    assert first_pass == ["t-1", "t-2"]
    assert second_pass == ["t-1", "t-2"]


def test_empty_queue_iteration() -> None:
    queue = TaskQueue()
    assert list(queue) == []


def test_add_task_to_queue() -> None:
    queue = TaskQueue()
    queue.add(Task(id="t-1"))

    assert [task.id for task in queue] == ["t-1"]


def test_extend_queue() -> None:
    queue = TaskQueue([Task(id="t-1")])
    queue.extend([Task(id="t-2"), Task(id="t-3")])

    assert [task.id for task in queue] == ["t-1", "t-2", "t-3"]


def test_len_returns_number_of_tasks() -> None:
    queue = TaskQueue([Task(id="t-1"), Task(id="t-2")])
    assert len(queue) == 2


def test_filter_returns_iterator_not_list() -> None:
    queue = TaskQueue([Task(id="t-1"), Task(id="t-2")])

    result = queue.filter(lambda task: task.id == "t-1")

    assert isinstance(result, Iterator)
    assert not isinstance(result, list)


def test_filter_by_status_returns_matching_tasks() -> None:
    task1 = Task(id="t-1")
    task2 = Task(id="t-2")
    task3 = Task(id="t-3")

    task2.start()
    task3.start()
    task3.complete()

    queue = TaskQueue([task1, task2, task3])

    pending_ids = [task.id for task in queue.filter_by_status(TaskStatus.PENDING)]
    in_progress_ids = [task.id for task in queue.filter_by_status(TaskStatus.IN_PROGRESS)]
    done_ids = [task.id for task in queue.filter_by_status(TaskStatus.DONE)]

    assert pending_ids == ["t-1"]
    assert in_progress_ids == ["t-2"]
    assert done_ids == ["t-3"]


def test_filter_by_priority_min_only() -> None:
    queue = TaskQueue([
        Task(id="t-1", priority=2),
        Task(id="t-2", priority=5),
        Task(id="t-3", priority=9),
    ])

    result = [task.id for task in queue.filter_by_priority(min_priority=5)]

    assert result == ["t-2", "t-3"]


def test_filter_by_priority_range() -> None:
    queue = TaskQueue([
        Task(id="t-1", priority=2),
        Task(id="t-2", priority=5),
        Task(id="t-3", priority=9),
    ])

    result = [task.id for task in queue.filter_by_priority(min_priority=3, max_priority=8)]

    assert result == ["t-2"]


def test_iterator_raises_stop_iteration() -> None:
    queue = TaskQueue([Task(id="t-1")])
    iterator = iter(queue)

    assert next(iterator).id == "t-1"

    with pytest.raises(StopIteration):
        next(iterator)


def test_queue_compatible_with_standard_python_constructs() -> None:
    queue = TaskQueue([
        Task(id="t-1", priority=3),
        Task(id="t-2", priority=7),
    ])

    assert list(queue) == [Task(id="t-1", priority=3), Task(id="t-2", priority=7)]
    assert sum(task.priority for task in queue) == 10