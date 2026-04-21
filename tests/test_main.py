from __future__ import annotations

from pathlib import Path

from src import main


def test_main_prints_tasks(capsys) -> None:
    demo_file = Path("demo_tasks.jsonl")
    if demo_file.exists():
        demo_file.unlink()

    main.main()

    captured = capsys.readouterr()
    output = captured.out

    assert 'file-1: {"action": "process_order", "order_id": 101}' in output
    assert 'file-2: {"action": "send_notification", "user_id": 7}' in output
    assert 'gen-1: {"action": "recalculate_stats"}' in output
    assert 'gen-2: {"action": "check_resource"}' in output
    assert 'api-1: {"action": "sync_external_data"}' in output
    assert 'api-2: {"action": "rebuild_cache"}' in output

    assert "=== Очередь задач: итераторы и генераторы ===" in output
    assert "Фильтр по статусу IN_PROGRESS:" in output
    assert "Фильтр по приоритету >= 5:" in output

    if demo_file.exists():
        demo_file.unlink()