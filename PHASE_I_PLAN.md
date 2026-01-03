# Phase I Technical Plan: Basic Todo Console Application

## Overview

This technical plan outlines the implementation approach for Phase I of the "Evolution of Todo" project. The plan is derived directly from the Phase I specification and adheres to the global Constitution's principles of spec-driven development, clean architecture, and technology constraints.

## 1. High-Level Application Structure

The application shall be implemented as a single Python program (`todo_app.py`) with the following architectural components:

### Main Components
- **Task Model**: Immutable data class representing task entities
- **Task Manager**: Class handling in-memory task storage and operations
- **CLI Interface**: Class managing user interaction and menu display
- **Main Application**: Entry point coordinating between components

### File Structure
```
todo_app.py
├── Task (dataclass)
├── TaskManager (class)
├── CLIInterface (class)
└── main() function
```

### Execution Flow
1. Application starts with `main()` function
2. Initialize TaskManager and CLIInterface instances
3. Enter main menu loop
4. Process user selections until exit
5. Clean shutdown

## 2. In-Memory Data Structures

### Task Storage
- **Primary Storage**: Python `list` to maintain task order and allow indexed access
- **Type**: `List[Task]` where Task is a dataclass
- **Initialization**: Empty list at application start

### Task Model Implementation
```python
@dataclass(frozen=True)
class Task:
    id: int
    title: str
    completed: bool = False
    created_at: datetime
```

### Data Operations
- **Add**: Append new Task to list
- **View**: Iterate through list for display
- **Update**: Find task by ID, create new Task with updated fields
- **Delete**: Remove task from list by index
- **Toggle**: Find task by ID, create new Task with inverted completed status

## 3. Task Identification Strategy

### ID Generation
- **Strategy**: Auto-incrementing integer starting from 1
- **Implementation**: Track next available ID in TaskManager
- **Uniqueness**: Guaranteed within single application session
- **Type**: Positive integer (int)

### ID Management
- **Storage**: Instance variable in TaskManager (`self._next_id`)
- **Initialization**: Set to 1 at TaskManager creation
- **Increment**: After successful task creation
- **Validation**: Check existence before update/delete/toggle operations

### ID Lookup
- **Method**: Linear search through task list by ID
- **Performance**: Acceptable for Phase I scale (no performance requirements)
- **Return**: Task object or None if not found

## 4. CLI Control Flow

### Main Menu Loop
```python
while True:
    display_menu()
    choice = get_user_input()
    if choice == '6':  # Exit
        break
    process_choice(choice)
```

### User Input Handling
- **Input Method**: `input()` function for all user interactions
- **Validation**: Strip whitespace, validate format and range
- **Error Recovery**: Display error message and re-prompt on invalid input
- **Exit Handling**: Graceful exit on Ctrl+C (KeyboardInterrupt)

### Menu Options Mapping
- **1**: Add Task → `add_task_flow()`
- **2**: View Tasks → `view_tasks_flow()`
- **3**: Update Task → `update_task_flow()`
- **4**: Delete Task → `delete_task_flow()`
- **5**: Toggle Status → `toggle_task_flow()`
- **6**: Exit → Break loop

### Input Flow Patterns
- **Single Input**: Menu choice, task ID
- **Two-Step Input**: Task ID + title (for add/update)
- **Confirmation**: Display success/error messages after operations

## 5. Separation of Responsibilities

### TaskManager Class
**Responsibilities:**
- Maintain in-memory task storage
- Generate unique task IDs
- Perform CRUD operations on tasks
- Validate task existence and data integrity

**Interface:**
- `add_task(title: str) -> Task`
- `get_all_tasks() -> List[Task]`
- `get_task_by_id(task_id: int) -> Optional[Task]`
- `update_task(task_id: int, new_title: str) -> bool`
- `delete_task(task_id: int) -> bool`
- `toggle_task_status(task_id: int) -> bool`

### CLIInterface Class
**Responsibilities:**
- Display menus and prompts
- Collect and validate user input
- Format and display task information
- Handle user interaction flow
- Display success and error messages

**Interface:**
- `display_main_menu() -> None`
- `get_menu_choice() -> str`
- `get_task_title(prompt: str) -> str`
- `get_task_id(prompt: str) -> int`
- `display_tasks(tasks: List[Task]) -> None`
- `display_message(message: str) -> None`
- `display_error(error: str) -> None`

### Main Function
**Responsibilities:**
- Initialize application components
- Coordinate between TaskManager and CLIInterface
- Manage main application loop
- Handle application shutdown

## 6. Error Handling Strategy

### Input Validation
- **Menu Choice**: Must be '1'-'6', re-prompt on invalid
- **Task ID**: Must be positive integer, validate existence
- **Task Title**: Non-empty, ≤100 characters, strip whitespace

### Error Types and Responses

#### Invalid Menu Choice
- **Detection**: Input not in ['1','2','3','4','5','6']
- **Response**: Display "Invalid choice. Please enter 1-6." and re-display menu

#### Invalid Task ID
- **Detection**: Task ID not found in task list
- **Response**: Display "Task with ID X not found." and return to menu

#### Empty Task List
- **Detection**: Task list is empty for view/update/delete/toggle
- **Response**: Display "No tasks available." and return to menu

#### Invalid Task Title
- **Detection**: Empty string or only whitespace after stripping
- **Response**: Display "Task title cannot be empty." and re-prompt

#### Task Title Too Long
- **Detection**: Title length > 100 characters
- **Response**: Display "Task title must be 100 characters or less." and re-prompt

### Exception Handling
- **KeyboardInterrupt**: Graceful exit with "Goodbye!" message
- **Unexpected Errors**: Generic error message and continue operation
- **Data Integrity**: Ensure task list remains consistent after operations

### Error Message Standards
- Clear and actionable error descriptions
- Consistent formatting across all error cases
- No technical jargon in user-facing messages
- Immediate feedback followed by re-prompt or menu return

## Implementation Constraints

- **Single File**: All code in one Python file
- **Standard Library Only**: No external dependencies
- **Python Version**: Compatible with Python 3.8+
- **Memory Management**: No memory optimization required for Phase I
- **Performance**: No performance requirements beyond basic functionality

## Testing Strategy

- **Unit Tests**: Test TaskManager operations in isolation
- **Integration Tests**: Test CLIInterface with mocked input
- **Manual Testing**: Verify end-to-end user flows
- **Error Case Testing**: Validate all error handling scenarios

---

*This plan is derived strictly from the Phase I specification and global Constitution. It defines the technical approach without introducing new features or deviating from approved requirements.*