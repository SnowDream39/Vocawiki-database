from fastapi import APIRouter, Depends

from app.user_manager import fastapi_users, auth_backend_bearer, auth_backend_cookie, current_active_user
from app.schemas.user import UserRead, UserCreate
from app.models import User
router = APIRouter()

# 登录，利用 backend


router.include_router(
    fastapi_users.get_auth_router(auth_backend_bearer), prefix="/auth/jwt", tags=["auth"]
)
router.include_router(
    fastapi_users.get_auth_router(auth_backend_cookie), prefix="/auth/jwt-cookie", tags=["auth"]
)

# 其他

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

@router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

