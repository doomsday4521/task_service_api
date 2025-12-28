from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse
)

from app.services.task_service import TaskService
router = APIRouter(prefix="/tasks",tags=["tasks"])

@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_task(
    payload:TaskCreate,
    db:AsyncSession=Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    try:
        return await TaskService.create(
            db,
            user_id=current_user.id,
            title=payload.title,
            description=payload.description
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    

@router.get("",response_model=list[TaskResponse])
async def list_tasks(
    limit:int=10,
    offset:int=0,
    db:AsyncSession=Depends(get_db),
    current_user:User = Depends(get_current_user)
):
   
    try:
         return await TaskService.list(
                db,
                user_id=current_user.id,
                limit=limit,
                offset=offset
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task(
    task_id:int,
    db:AsyncSession=Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    try:
        await TaskService.delete(
            db,
            task_id=task_id,
            user_id=current_user.id,
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
@router.patch(
    "/{task_id}",
    response_model=TaskResponse
)
async def update_task(
    task_id:int,
    payload:TaskUpdate,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        return await TaskService.update(
            db,
            task_id=task_id,
            user_id=current_user.id,
            title=payload.title,
            description=payload.description,
            is_completed=payload.description
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )