#!/usr/bin/env python3
"""
Simple test script for Phase I Todo Application
Tests basic functionality without interactive input
"""

from todo_app import Task, TaskManager, CLIInterface

def test_task_creation():
    """Test Task dataclass creation"""
    task = Task(id=1, title="Test Task")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.completed == False
    assert task.created_at is not None
    print("✓ Task creation test passed")

def test_task_manager():
    """Test TaskManager basic operations"""
    tm = TaskManager()

    # Test add
    task = tm.add_task("Test Task")
    assert task.id == 1
    assert task.title == "Test Task"
    assert len(tm.get_all_tasks()) == 1

    # Test get by id
    found = tm.get_task_by_id(1)
    assert found is not None
    assert found.id == 1

    # Test update
    success = tm.update_task(1, "Updated Task")
    assert success == True
    updated = tm.get_task_by_id(1)
    assert updated.title == "Updated Task"

    # Test toggle
    success = tm.toggle_task_status(1)
    assert success == True
    toggled = tm.get_task_by_id(1)
    assert toggled.completed == True

    # Test delete
    success = tm.delete_task(1)
    assert success == True
    assert len(tm.get_all_tasks()) == 0

    print("✓ TaskManager tests passed")

def test_cli_interface():
    """Test CLIInterface basic methods"""
    cli = CLIInterface()

    # Test display methods don't crash
    cli.display_main_menu()
    cli.display_tasks([])
    cli.display_message("Test")
    cli.display_error("Test error")

    print("✓ CLIInterface basic tests passed")

if __name__ == "__main__":
    print("Running Phase I validation tests...")
    test_task_creation()
    test_task_manager()
    test_cli_interface()
    print("All tests passed! ✓")