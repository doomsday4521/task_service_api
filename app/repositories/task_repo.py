from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,desc
from typing import List

from app.models.task import Task


async def create_task(
    db:AsyncSession,
    *,
    user_id:int,
    title:str,
    description:str|None
)->Task:
    task = Task(
        user_id=user_id,
        title=title,
        description=description
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def list_tasks(
        db:AsyncSession,
        *,
        user_id:int,
        limit:int,
        offset:int
)->List[Task]:
    result =  await db.execute(
        select(Task).where(Task.user_id==user_id).order_by(desc(Task.created_at)).limit(limit).offset(offset)
    )
    return result.scalars().all()

async def get_task_by_id(
        db:AsyncSession,
        *,
        task_id:int,
        user_id:int
)->Task|None:
    result = await db.execute(
        select(Task).where(
            Task.id==task_id,
            Task.user_id==user_id
        )
    )
    return result.scalar_one_or_none()


async def delete_task(
        db:AsyncSession,
        *,
        task:Task
)->None:
    await db.delete(task)
    await db.commit()
    
async def update_task(
        db,
        *,
        task
):
    await db.commit()
    await db.refresh(task)
    return task