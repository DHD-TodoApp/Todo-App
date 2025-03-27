import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Message,
    SubTodo,
    SubTodoCreate,
    SubTodoPublic,
    SubTodosPublic,
    SubTodoUpdate,
    Todo,
)

router = APIRouter(prefix="/todos/{todo_id}/subtodos", tags=["subtodos"])


def validate_todo_access(
    session: SessionDep, current_user: CurrentUser, todo_id: uuid.UUID
) -> Todo:
    """Validate that the user has access to the todo."""
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if not current_user.is_superuser and (todo.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return todo


@router.get("/", response_model=SubTodosPublic)
def read_subtodos(
    session: SessionDep,
    current_user: CurrentUser,
    todo_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Retrieve subtodos for a specific todo."""
    # Validate todo access
    validate_todo_access(session, current_user, todo_id)
    # Get subtodos
    statement = (
        select(SubTodo).where(SubTodo.todo_id == todo_id).offset(skip).limit(limit)
    )
    subtodos = session.exec(statement).all()
    count = len(subtodos)
    return SubTodosPublic(data=subtodos, count=count)


@router.post("/", response_model=SubTodoPublic)
def create_subtodo(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    todo_id: uuid.UUID,
    subtodo_in: SubTodoCreate,
) -> Any:
    """Create a new subtodo for a specific todo."""
    # Validate todo access
    validate_todo_access(session, current_user, todo_id)
    # Create subtodo
    subtodo = SubTodo(
        title=subtodo_in.title,
        desc=subtodo_in.desc,
        todo_id=todo_id,
        status="in_progress",
    )
    session.add(subtodo)
    session.commit()
    session.refresh(subtodo)
    # Convert to SubTodoPublic before returning
    return SubTodoPublic(
        id=subtodo.id,
        title=subtodo.title,
        desc=subtodo.desc,
        created_at=subtodo.created_at,
        updated_at=subtodo.updated_at,
        todo_id=subtodo.todo_id,
        status=subtodo.status,
    )


@router.get("/{id}", response_model=SubTodoPublic)
def read_subtodo(
    session: SessionDep, current_user: CurrentUser, todo_id: uuid.UUID, id: uuid.UUID
) -> Any:
    """Get a specific subtodo."""
    # Validate todo access
    validate_todo_access(session, current_user, todo_id)
    # Get subtodo
    subtodo = session.get(SubTodo, id)
    if not subtodo:
        raise HTTPException(status_code=404, detail="Subtodo not found")
    if subtodo.todo_id != todo_id:
        raise HTTPException(
            status_code=400, detail="Subtodo does not belong to this todo"
        )
    return subtodo


@router.put("/{id}", response_model=SubTodoPublic)
def update_subtodo(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    todo_id: uuid.UUID,
    id: uuid.UUID,
    subtodo_in: SubTodoUpdate,
) -> Any:
    """Update a subtodo."""
    # Validate todo access
    validate_todo_access(session, current_user, todo_id)
    # Get subtodo
    subtodo = session.get(SubTodo, id)
    if not subtodo:
        raise HTTPException(status_code=404, detail="Subtodo not found")
    if subtodo.todo_id != todo_id:
        raise HTTPException(
            status_code=400, detail="Subtodo does not belong to this todo"
        )
    # Update subtodo
    update_dict = subtodo_in.model_dump(exclude_unset=True)
    subtodo.sqlmodel_update(update_dict)
    session.add(subtodo)
    session.commit()
    session.refresh(subtodo)
    return subtodo


@router.delete("/{id}")
def delete_subtodo(
    session: SessionDep, current_user: CurrentUser, todo_id: uuid.UUID, id: uuid.UUID
) -> Message:
    """Delete a subtodo."""
    # Validate todo access
    validate_todo_access(session, current_user, todo_id)
    # Get subtodo
    subtodo = session.get(SubTodo, id)
    if not subtodo:
        raise HTTPException(status_code=404, detail="Subtodo not found")
    if subtodo.todo_id != todo_id:
        raise HTTPException(
            status_code=400, detail="Subtodo does not belong to this todo"
        )
    # Delete subtodo
    session.delete(subtodo)
    session.commit()
    return Message(message="Subtodo deleted successfully")
