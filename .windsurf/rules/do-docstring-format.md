---
trigger: model_decision
description: When writing or reviewing function/method docstrings
---

# Rule: Docstring Format with Examples

## Required Format

All functions and methods MUST have docstrings following this exact format:

```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """
    A brief summary of what the function does.

    :param param1: description as Type1. Example: value_example
    :param param2: description as Type2. Example: value_example
    :return: Description of the value returned. Example: return_value_example
    :raises ExceptionType: When this exception is raised.
    """
```

## Key Requirements

1. **Summary Line**: Brief description of function purpose
2. **Blank Line**: After summary
3. **Parameters**: Each parameter documented with:
   - Name
   - Description as Type
   - **Example value** (REQUIRED)
4. **Return**: Description with **Example** (REQUIRED)
5. **Raises**: Document exceptions (if any)

## Examples

### Simple Function

```python
def get_workflow(workflow_id: str) -> Dict:
    """
    Retrieve workflow by ID.

    :param workflow_id: workflow UUID as str. Example: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    :return: Workflow data as dict. Example: {"id": "a1b2c3d4", "name": "Build Feature", "activities": 5}
    :raises ValueError: If workflow_id is not a valid UUID.
    :raises NotFoundError: If workflow does not exist.
    """
```

### Multiple Parameters

```python
def create_activity(name: str, role_id: int, workflow_id: str, estimated_hours: float = 2.0) -> Activity:
    """
    Create a new activity in a workflow.

    :param name: activity name as str. Example: "Design Component"
    :param role_id: role identifier as int. Example: 3
    :param workflow_id: workflow UUID as str. Example: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    :param estimated_hours: estimated time as float. Example: 4.5
    :return: Created activity instance. Example: Activity(id=12, name="Design Component", role=Role(3))
    :raises ValueError: If name is empty or role_id is invalid.
    :raises NotFoundError: If workflow does not exist.
    """
```

### Complex Return Types

```python
def get_workflow_with_activities(workflow_id: str) -> Dict[str, Any]:
    """
    Retrieve workflow with all related activities and metadata.

    :param workflow_id: workflow UUID as str. Example: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    :return: Workflow data with activities as dict. Example: {
        "workflow": {"id": "a1b2c3d4", "name": "Build Feature"},
        "activities": [{"id": 1, "name": "Design"}, {"id": 2, "name": "Implement"}],
        "activity_count": 2,
        "completion_percentage": 50.0
    }
    :raises ValueError: If workflow_id is not a valid UUID.
    :raises NotFoundError: If workflow does not exist.
    """
```

### List Return Type

```python
def filter_activities_by_role(workflow_id: str, role_id: int) -> List[Dict]:
    """
    Get all activities for a specific role in a workflow.

    :param workflow_id: workflow UUID as str. Example: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    :param role_id: role identifier as int. Example: 3
    :return: List of activity dictionaries. Example: [
        {"id": 1, "name": "Design Component", "role_id": 3},
        {"id": 5, "name": "Code Review", "role_id": 3}
    ]
    :raises ValueError: If workflow_id or role_id is invalid.
    """
```

### No Parameters

```python
def get_all_methodologies() -> List[str]:
    """
    Retrieve list of all available methodology names.

    :return: Methodology names as list. Example: ["FDD", "Scrum", "Kanban"]
    """
```

### No Return Value

```python
def log_activity_event(activity_id: int, event_type: str, user_id: int) -> None:
    """
    Log an activity event to the system log.

    :param activity_id: activity identifier as int. Example: 42
    :param event_type: event type as str. Example: "started"
    :param user_id: user identifier as int. Example: 7
    :return: None
    :raises ValueError: If activity_id or user_id does not exist.
    """
```

### Class Methods

```python
class MethodologyService:
    def __init__(self, repository: Repository):
        """
        Initialize methodology service.

        :param repository: data access layer. Example: DjangoORMRepository()
        """
        self.repository = repository
    
    def add_workflow_to_methodology(self, methodology_id: str, workflow_name: str) -> Workflow:
        """
        Add a new workflow to an existing methodology.

        :param methodology_id: methodology UUID as str. Example: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        :param workflow_name: workflow name as str. Example: "Build Feature"
        :return: Created workflow instance. Example: Workflow(id="b2c3d4e5", name="Build Feature")
        :raises ValueError: If workflow_name is empty.
        :raises NotFoundError: If methodology does not exist.
        """
```

## Why Examples Are Required

1. **Clarity**: Shows exact expected format of inputs/outputs
2. **Testing**: Examples guide test case creation
3. **Debugging**: Makes troubleshooting easier with concrete values
4. **Onboarding**: New developers understand usage immediately
5. **Documentation**: Auto-generated docs are more useful

## Anti-Patterns to Avoid

### ❌ Bad: No Examples
```python
def get_workflow(workflow_id: str) -> Dict:
    """
    Retrieve workflow by ID.

    :param workflow_id: workflow UUID as str
    :return: Workflow data as dict
    """
```

### ❌ Bad: Vague Descriptions
```python
def create_activity(name: str, role_id: int) -> Activity:
    """
    Creates an activity.

    :param name: the name
    :param role_id: the role
    :return: the activity
    """
```

### ❌ Bad: Missing Return Example
```python
def get_activities() -> List[Dict]:
    """
    Get all activities.

    :return: List of activities
    """
```

### ✅ Good: Complete with Examples
```python
def get_activities() -> List[Dict]:
    """
    Retrieve all activities in the system.

    :return: Activity list as list of dicts. Example: [
        {"id": 1, "name": "Design", "role": "Engineer"},
        {"id": 2, "name": "Test", "role": "QA"}
    ]
    """
```

## Enforcement

- **Code Reviews**: Check all new functions have proper docstrings
- **Pre-commit**: Consider docstring linter in future
- **IDE**: Configure IDE to show docstring warnings
- **Tests**: Test docstrings should follow same format

## Special Cases

### Optional Parameters
```python
def search_activities(keyword: str, role_id: Optional[int] = None) -> List[Dict]:
    """
    Search activities by keyword and optionally filter by role.

    :param keyword: search term as str. Example: "design"
    :param role_id: optional role filter as int or None. Example: 3 or None
    :return: Matching activities as list. Example: [{"id": 1, "name": "Design Component"}]
    """
```

### Variable Arguments
```python
def create_activities_batch(*names: str) -> List[Activity]:
    """
    Create multiple activities at once.

    :param names: activity names as variable args. Example: "Design", "Implement", "Test"
    :return: Created activity instances as list. Example: [Activity(id=1), Activity(id=2), Activity(id=3)]
    """
```

### Keyword Arguments
```python
def update_activity(activity_id: int, **updates: Any) -> Activity:
    """
    Update activity with provided field changes.

    :param activity_id: activity identifier as int. Example: 42
    :param updates: field updates as kwargs. Example: name="New Name", estimated_hours=5.0
    :return: Updated activity instance. Example: Activity(id=42, name="New Name", estimated_hours=5.0)
    :raises ValueError: If activity_id does not exist.
    """
```

## Summary

**Always include:**
- ✅ Brief summary
- ✅ Parameter descriptions with types
- ✅ **Example values for every parameter**
- ✅ Return description with type
- ✅ **Example value for return**
- ✅ Exceptions raised (if any)

This format makes code self-documenting and dramatically improves maintainability.
