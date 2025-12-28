from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.task_repo import (
    create_task,
    list_tasks,
    get_task_by_id,
    delete_task,
    update_task
)

from app.models.task import Task

class TaskService:
    @staticmethod
    async def create(
         db: AsyncSession,
        *,
        user_id: int,
        title: str,
        description: str | None,
    )->Task:
        if not title or not title.strip():
            raise ValueError("Title can't be empty!")
        return await create_task(
            db,
            user_id=user_id,
            title=title.strip(),
            description=description,
        )
    
    @staticmethod
    async def list(
        db: AsyncSession,
        *,
        user_id: int,
        limit:int,
        offset:int
    )    -> list[Task]:
        if limit <= 0:
            raise ValueError("limit must be > 0")

        if limit > 100:
            raise ValueError("limit cannot exceed 100")

        if offset < 0:
            raise ValueError("offset must be >= 0")
        
        return await list_tasks(
            db,
            user_id=user_id,
            limit=limit,
            offset=offset
        )
    @staticmethod
    async def delete(
        db: AsyncSession,
        *,
        task_id: int,
        user_id: int,
         ) -> None:
        task = await get_task_by_id(
            db,
            task_id=task_id,
            user_id=user_id,
        )

        if task is None:
            raise ValueError("Task not found")

        await delete_task(
            db,
            task=task,
        )
    @staticmethod
    async def update(
        db,
        *,
        task_id:int,
        user_id:int,
        title:str|None,
        description:str|None,
        is_completed:bool|None
    ):
        task = await get_task_by_id(
            db,
            task_id=task_id,
            user_id=user_id
        )
        if task is None:
            raise ValueError("Task not found!")
        if title is not None:
            if not title.strip():
                raise ValueError("Title can't be empty!")
            task.title = title.strip()
        
        if description is not None:
            task.description = description
        if is_completed is not None:
            task.is_completed = is_completed
        
        return await update_task(db,task=task)