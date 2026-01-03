# Phase I Specification: Basic Todo Console Application

## Overview

This specification defines Phase I of the "Evolution of Todo" project, implementing a basic in-memory Python console application for single-user task management. This phase establishes the foundational task management functionality while adhering strictly to the global Constitution's constraints.

## Scope and Constraints

### In Scope
- In-memory Python console application
- Single user operation
- Runtime-only persistence (no data survives application restart)

### Out of Scope
- Databases or file-based persistence
- Multi-user functionality
- Authentication or authorization
- Web interfaces or APIs
- Advanced features (search, filtering, categories, due dates, etc.)
- References to future phase capabilities

## Task Data Model

### Task Entity
Each task shall be represented by the following immutable data structure:

```python
@dataclass(frozen=True)
class Task:
    id: int                    # Unique identifier (auto-generated)
    title: str                 # Task description (1-100 characters)
    completed: bool = False    # Completion status (default: False)
    created_at: datetime       # Creation timestamp (auto-generated)
```

### Constraints
- **ID**: Positive integer, auto-incremented starting from 1
- **Title**: Non-empty string, maximum 100 characters, no leading/trailing whitespace
- **Completed**: Boolean value (True/False)
- **Created At**: UTC timestamp, set at task creation time

### Data Storage
- Tasks stored in memory using a Python list
- No persistence beyond application runtime
- Task IDs must remain unique within a single application session

## User Stories

### US-1: Add Task
As a user, I want to add a new task so that I can track something I need to do.

**Acceptance Criteria:**
- User can enter a task title via console input
- System generates unique ID and creation timestamp
- Task is added to the in-memory list
- Success confirmation is displayed

### US-2: View Task List
As a user, I want to view all my tasks so that I can see what I need to do.

**Acceptance Criteria:**
- All tasks are displayed in a readable format
- Tasks show ID, title, completion status, and creation time
- Empty list displays appropriate message
- Tasks are displayed in creation order (oldest first)

### US-3: Update Task
As a user, I want to update an existing task's title so that I can correct or modify my tasks.

**Acceptance Criteria:**
- User provides task ID and new title
- System validates task exists
- Task title is updated while preserving other fields
- Success confirmation is displayed

### US-4: Delete Task
As a user, I want to delete a task so that I can remove completed or unnecessary tasks.

**Acceptance Criteria:**
- User provides task ID
- System validates task exists
- Task is permanently removed from the list
- Success confirmation is displayed

### US-5: Mark Task Complete/Incomplete
As a user, I want to toggle a task's completion status so that I can track progress.

**Acceptance Criteria:**
- User provides task ID
- System validates task exists
- Task completion status is toggled (True ↔ False)
- Success confirmation is displayed

## CLI Interaction Flow

### Main Menu
```
=== Todo Application ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Task Status
6. Exit

Choose an option (1-6):
```

### Add Task Flow
```
Enter task title: [user input]
Task added successfully! (ID: 1)
```

### View Tasks Flow
```
=== Your Tasks ===
1. Buy groceries (Incomplete) - Created: 2024-01-04 10:30:00
2. Call dentist (Complete) - Created: 2024-01-04 10:35:00

Total tasks: 2
```

### Update Task Flow
```
Enter task ID to update: [user input]
Enter new title: [user input]
Task updated successfully!
```

### Delete Task Flow
```
Enter task ID to delete: [user input]
Task deleted successfully!
```

### Toggle Status Flow
```
Enter task ID to toggle: [user input]
Task status toggled successfully! (Now: Complete/Incomplete)
```

### Exit Flow
```
Goodbye!
```

## Acceptance Criteria

### General Criteria
- Application starts and displays main menu
- All menu options are functional
- Input validation prevents invalid operations
- Clear error messages for invalid inputs
- Application exits cleanly when requested

### Feature-Specific Criteria

#### Add Task
- Accepts titles 1-100 characters long
- Rejects empty or whitespace-only titles
- Generates sequential IDs starting from 1
- Sets creation timestamp to current UTC time
- Displays success message with assigned ID

#### View Tasks
- Shows all tasks when list is not empty
- Shows "No tasks found." when list is empty
- Displays tasks in creation order
- Shows completion status clearly (Complete/Incomplete)
- Shows creation timestamp in readable format

#### Update Task
- Accepts valid task ID (existing in list)
- Accepts new title 1-100 characters long
- Preserves original creation timestamp
- Updates only the title field
- Rejects invalid task IDs

#### Delete Task
- Accepts valid task ID (existing in list)
- Permanently removes task from memory
- Rejects invalid task IDs
- IDs of remaining tasks remain unchanged

#### Toggle Task Status
- Accepts valid task ID (existing in list)
- Changes completion status from True to False or False to True
- Preserves all other task fields
- Rejects invalid task IDs

## Error Cases

### Invalid Task ID
**Scenario**: User enters non-existent task ID for update, delete, or toggle operations
**Expected Behavior**:
- Display error: "Task with ID X not found."
- Return to main menu without changes

### Empty Task List
**Scenario**: User attempts view, update, delete, or toggle when no tasks exist
**Expected Behavior**:
- View: Display "No tasks found."
- Update/Delete/Toggle: Display "No tasks available." and return to menu

### Invalid Title Input
**Scenario**: User enters empty string or only whitespace for task title
**Expected Behavior**:
- Display error: "Task title cannot be empty."
- Prompt for input again

### Title Too Long
**Scenario**: User enters title exceeding 100 characters
**Expected Behavior**:
- Display error: "Task title must be 100 characters or less."
- Prompt for input again

### Invalid Menu Choice
**Scenario**: User enters non-numeric or out-of-range menu option
**Expected Behavior**:
- Display error: "Invalid choice. Please enter 1-6."
- Redisplay main menu

## Implementation Notes

- Use Python's built-in `dataclass` for Task model
- Use `datetime` module for timestamps
- Implement as single Python file for simplicity
- Use console input/output for all interactions
- Handle keyboard interrupts gracefully (Ctrl+C to exit)
- No external dependencies required

## Testing Requirements

- Unit tests for Task model creation and validation
- Integration tests for each CLI operation
- Error case testing for all invalid inputs
- Edge case testing (empty lists, single task operations)

---

*This specification complies with the global Constitution and defines the complete scope of Phase I delivery.*