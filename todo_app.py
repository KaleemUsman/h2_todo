#!/usr/bin/env python3
"""
Phase I: Basic Todo Console Application

This is the implementation of Phase I for the "Evolution of Todo" project.
A simple in-memory Python console application for single-user task management.

Features:
- Add Task
- View Task List
- Update Task
- Delete Task
- Mark Task Complete/Incomplete

All functionality is in-memory only with no persistence.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass(frozen=True)
class Task:
    """Immutable task data structure."""
    id: int
    title: str
    completed: bool = False
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            object.__setattr__(self, 'created_at', datetime.utcnow())


class TaskManager:
    """Manages in-memory task storage and operations."""

    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id = 1

    def add_task(self, title: str) -> Task:
        """Add a new task and return it."""
        task = Task(id=self._next_id, title=title.strip())
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks."""
        return self._tasks.copy()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Find task by ID."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, new_title: str) -> bool:
        """Update task title. Returns True if successful."""
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                updated_task = Task(
                    id=task.id,
                    title=new_title.strip(),
                    completed=task.completed,
                    created_at=task.created_at
                )
                self._tasks[i] = updated_task
                return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """Delete task by ID. Returns True if successful."""
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                self._tasks.pop(i)
                return True
        return False

    def toggle_task_status(self, task_id: int) -> bool:
        """Toggle task completion status. Returns True if successful."""
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                updated_task = Task(
                    id=task.id,
                    title=task.title,
                    completed=not task.completed,
                    created_at=task.created_at
                )
                self._tasks[i] = updated_task
                return True
        return False


class CLIInterface:
    """Handles user interface and input/output operations."""

    def display_main_menu(self) -> None:
        """Display the main menu."""
        print("\n=== Todo Application ===")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Toggle Task Status")
        print("6. Exit")

    def get_menu_choice(self) -> str:
        """Get menu choice from user."""
        try:
            choice = input("Choose an option (1-6): ").strip()
            return choice
        except (KeyboardInterrupt, EOFError):
            return '6'  # Exit on Ctrl+C or EOF

    def get_task_title(self, prompt: str) -> str:
        """Get task title from user with validation."""
        while True:
            try:
                title = input(prompt).strip()
                if not title:
                    print("Task title cannot be empty.")
                    continue
                if len(title) > 100:
                    print("Task title must be 100 characters or less.")
                    continue
                return title
            except (KeyboardInterrupt, EOFError):
                raise  # Let main handle exit

    def get_task_id(self, prompt: str) -> int:
        """Get task ID from user with validation."""
        while True:
            try:
                id_str = input(prompt).strip()
                if not id_str:
                    print("Task ID cannot be empty.")
                    continue
                try:
                    task_id = int(id_str)
                    if task_id <= 0:
                        print("Task ID must be a positive number.")
                        continue
                    return task_id
                except ValueError:
                    print("Task ID must be a number.")
                    continue
            except (KeyboardInterrupt, EOFError):
                raise  # Let main handle exit

    def display_tasks(self, tasks: List[Task]) -> None:
        """Display all tasks."""
        if not tasks:
            print("No tasks found.")
            return

        print("\n=== Your Tasks ===")
        for task in tasks:
            status = "Complete" if task.completed else "Incomplete"
            created_str = task.created_at.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{task.id}. {task.title} ({status}) - Created: {created_str}")
        print(f"\nTotal tasks: {len(tasks)}")

    def display_message(self, message: str) -> None:
        """Display a success message."""
        print(message)

    def display_error(self, error: str) -> None:
        """Display an error message."""
        print(f"Error: {error}")


def main():
    """Main application entry point."""
    task_manager = TaskManager()
    cli = CLIInterface()

    print("Welcome to the Todo Application!")

    try:
        while True:
            cli.display_main_menu()
            choice = cli.get_menu_choice()

            if choice == '1':  # Add Task
                try:
                    title = cli.get_task_title("Enter task title: ")
                    task = task_manager.add_task(title)
                    cli.display_message(f"Task added successfully! (ID: {task.id})")
                except (KeyboardInterrupt, EOFError):
                    cli.display_message("Operation cancelled.")
                    continue

            elif choice == '2':  # View Tasks
                tasks = task_manager.get_all_tasks()
                cli.display_tasks(tasks)

            elif choice == '3':  # Update Task
                tasks = task_manager.get_all_tasks()
                if not tasks:
                    cli.display_error("No tasks available.")
                    continue

                try:
                    task_id = cli.get_task_id("Enter task ID to update: ")
                    task = task_manager.get_task_by_id(task_id)
                    if not task:
                        cli.display_error(f"Task with ID {task_id} not found.")
                        continue

                    new_title = cli.get_task_title("Enter new title: ")
                    if task_manager.update_task(task_id, new_title):
                        cli.display_message("Task updated successfully!")
                    else:
                        cli.display_error(f"Task with ID {task_id} not found.")
                except (KeyboardInterrupt, EOFError):
                    cli.display_message("Operation cancelled.")
                    continue

            elif choice == '4':  # Delete Task
                tasks = task_manager.get_all_tasks()
                if not tasks:
                    cli.display_error("No tasks available.")
                    continue

                try:
                    task_id = cli.get_task_id("Enter task ID to delete: ")
                    if task_manager.delete_task(task_id):
                        cli.display_message("Task deleted successfully!")
                    else:
                        cli.display_error(f"Task with ID {task_id} not found.")
                except (KeyboardInterrupt, EOFError):
                    cli.display_message("Operation cancelled.")
                    continue

            elif choice == '5':  # Toggle Task Status
                tasks = task_manager.get_all_tasks()
                if not tasks:
                    cli.display_error("No tasks available.")
                    continue

                try:
                    task_id = cli.get_task_id("Enter task ID to toggle: ")
                    if task_manager.toggle_task_status(task_id):
                        task = task_manager.get_task_by_id(task_id)
                        status = "Complete" if task.completed else "Incomplete"
                        cli.display_message(f"Task status toggled successfully! (Now: {status})")
                    else:
                        cli.display_error(f"Task with ID {task_id} not found.")
                except (KeyboardInterrupt, EOFError):
                    cli.display_message("Operation cancelled.")
                    continue

            elif choice == '6':  # Exit
                break

            else:
                cli.display_error("Invalid choice. Please enter 1-6.")

    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
        return

    print("Goodbye!")


if __name__ == "__main__":
    main()