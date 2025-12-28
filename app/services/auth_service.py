from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime,timedelta,timezone
from app.core.refresh import generate_refresh_token,hash_refresh_token
from app.models.refresh_token import RefreshToken
from app.core.security import create_access_token,verify_password
from app.core.config import settings
from sqlalchemy import select


from app.repositories.user_repo import (
    get_user_by_email,
    create_user
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


class AuthService:
    @staticmethod
    async def register(
        db:AsyncSession,
        email:str,
        password:str
    ):
        existing=await get_user_by_email(db,email)
        if existing:
            raise ValueError("Email already registered!")
        
        hashed=hash_password(password)
        return await create_user(db,email,hashed)
    @staticmethod
    async def login(
        db:AsyncSession,
        email:str,
        password:str
    )->dict:
        user = await get_user_by_email(db, email)
        if not user or not verify_password(password,user.hashed_password):
            raise ValueError("Invalid credentials!")
        access_token = create_access_token(subject=user.id)
        raw_refresh=generate_refresh_token()
        refresh_hash= hash_refresh_token(raw_refresh)
        refresh_token = RefreshToken(
            user_id=user.id,
            token_hash = refresh_hash,
            expires_at =  datetime.now(timezone.utc)+timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        db.add(refresh_token)
        await db.commit()
        return {
            "access_token":access_token,
            "refresh_token":raw_refresh
        }
        # return create_access_token(subject=user.id)
    @staticmethod
    async def refresh(db:AsyncSession,raw_refresh:str):
        refresh_hash = hash_refresh_token(raw_refresh)
        result = await db.execute(
            select(RefreshToken).where(
                RefreshToken.token_hash==refresh_hash,
                RefreshToken.revoked_at.is_(None),
                RefreshToken.expires_at>datetime.now(timezone.utc)
            )
        )
        token  =result.scalar_one_or_none()
        if token is None:
            raise ValueError("Invalid refresh token")
        
        token.revoked_at = datetime.now(timezone.utc)
        new_raw = generate_refresh_token()
        new_hash = hash_refresh_token(new_raw)
        new_token = RefreshToken(
            user_id = token.user_id,
            token_hash = new_hash,
            expires_at = datetime.now(timezone.utc)+timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        db.add(new_token)
        await db.commit()
        access_token = create_access_token(subject=token.user_id)
        return {
            "access_token":access_token,
            "refresh_token":new_raw
        }
        
    @staticmethod
    async def logout(db:AsyncSession,raw_refresh:str)->None:
        refresh_hash=hash_refresh_token(raw_refresh)
        result = await db.execute(
            select(RefreshToken).where(
                RefreshToken.token_hash==refresh_hash,
                RefreshToken.revoked_at.is_(None)
            )
        )
        token = result.scalar_one_or_none()
        if token is None:
            return
        
        token.revoked_at = datetime.now(timezone.utc)
        await db.commit()