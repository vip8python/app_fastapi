from datetime import datetime, timezone
from exceptions import TokenExpiredException, NotUserException, NotAdminException, IncorrectTokenFormatException, \
    TokenAbsentException
from fastapi import Request, Depends
import jwt
from config import settings
from users.dao import UsersDAO
from users.models import Users


def get_token(request: Request):
    token = request.cookies.get('booking_access_token')
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except jwt.PyJWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get('exp')
    if not expire or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise TokenExpiredException
    user_id: str = payload.get('sub')
    if not user_id:
        raise NotUserException
    user = await UsersDAO.find_my_id(int(user_id))
    if not user:
        raise NotUserException
    if user.email == settings.ADMIN:
        user.is_admin = True
    else:
        user.is_admin = False
    return user


async def get_current_admin_user(current_user: Users = Depends(get_current_user)):
    if not current_user.is_admin:
        raise NotAdminException
    return current_user
