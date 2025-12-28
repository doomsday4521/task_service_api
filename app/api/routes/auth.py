from fastapi import APIRouter,Depends,HTTPException,status

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import(
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshRequest
)
from app.services.auth_service import AuthService
from app.db.session import get_db
from app.schemas.auth import LogoutRequest

router = APIRouter(prefix="/auth",tags=["auth"])


@router.post("/register",status_code=status.HTTP_201_CREATED)
async def register(
    payload:RegisterRequest,
    db:AsyncSession=Depends(get_db)
):
    try:
        await AuthService.register(
            db,
            payload.email,
            payload.password
        )
        return {"message":"user created"}
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    
@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await AuthService.login(
            db,
            payload.email,
            payload.password,
        )
       
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

@router.post("/refresh",response_model=TokenResponse)
async def refresh(
    payload:RefreshRequest,
    db:AsyncSession=Depends(get_db)
):
    try:
        return await AuthService.refresh(
            db,
            payload.refresh_token
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
@router.post("/logout",status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    payload:LogoutRequest,
    db:AsyncSession=Depends(get_db)
):
    await AuthService.logout(
        db,
        payload.refresh_token
    )