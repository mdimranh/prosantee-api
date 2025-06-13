import json
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from api.v1.user.service import user_service
from core.utils.aes import AESCipher
from db.database import get_session

class LoginRequest(BaseModel):
    email: str
    password: str

router = APIRouter()

@router.post("/login")
async def login(data: LoginRequest,  response: Response, db: AsyncSession = Depends(get_session)):
    user = await user_service.get_by_email(db, email=data.email)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = AESCipher().generate_token(5, json.loads(user.json()))
    response.set_cookie(key="accessToken", value=token.token)
    return {
        "accessToken": token.token,
        "user": user
    }
