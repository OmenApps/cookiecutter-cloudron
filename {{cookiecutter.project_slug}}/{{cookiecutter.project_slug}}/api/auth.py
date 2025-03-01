from typing import Any

from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from ninja import Router

from . import api
from .schemas.auth import (
    LoginSchema,
    PasswordChangeSchema,
    TokenSchema,
    UserBasicSchema,
    UserCreateSchema,
    UserDetailSchema,
    UserUpdateSchema,
)

router = Router(tags=["Authentication"])
User = get_user_model()


@router.post("/login", response={200: TokenSchema, 401: dict}, auth=None)
def login(request, data: LoginSchema) -> dict[str, Any]:
    """Login endpoint that handles both regular and MFA authentication"""
    user = authenticate(email=data.email, password=data.password)

    if not user:
        return 401, {"message": "Invalid credentials"}

    if not user.is_active:
        return 401, {"message": "User account is disabled"}

    # Handle MFA if enabled
    if user.mfa_enabled:
        if not data.mfa_code:
            return 401, {"message": "MFA code required"}

        if not user.verify_mfa_code(data.mfa_code):
            return 401, {"message": "Invalid MFA code"}

    # Generate token
    token = user.generate_auth_token()

    return 200, {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 3600,  # 1 hour
    }


@router.post("/register", response={201: UserBasicSchema, 400: dict}, auth=None)
def register(request, data: UserCreateSchema) -> dict[str, Any]:
    """Register a new user account"""
    try:
        user = User.objects.create_user(email=data.email, password=data.password, name=data.name)
        return 201, UserBasicSchema.from_orm(user)
    except ValidationError as e:
        return 400, {"message": str(e)}


@router.get("/me", response=UserDetailSchema)
def get_current_user(request):
    """Get details of the currently authenticated user"""
    return UserDetailSchema.from_orm(request.auth)


@router.put("/me", response=UserDetailSchema)
def update_current_user(request, data: UserUpdateSchema):
    """Update the currently authenticated user's details"""
    user = request.auth

    if data.name:
        user.name = data.name
    if data.email:
        user.email = data.email

    user.save()
    return UserDetailSchema.from_orm(user)


@router.post("/me/change-password", response={200: dict, 400: dict})
def change_password(request, data: PasswordChangeSchema):
    """Change the current user's password"""
    user = request.auth

    if not user.check_password(data.current_password):
        return 400, {"message": "Current password is incorrect"}

    try:
        user.set_password(data.new_password)
        user.save()
        return 200, {"message": "Password updated successfully"}
    except ValidationError as e:
        return 400, {"message": str(e)}


@router.post("/me/enable-mfa", response={200: dict, 400: dict})
def enable_mfa(request):
    """Enable MFA for the current user"""
    user = request.auth

    if user.mfa_enabled:
        return 400, {"message": "MFA is already enabled"}

    try:
        secret = user.enable_mfa()
        return 200, {"message": "MFA enabled successfully", "secret": secret, "qr_code": user.get_mfa_qr_code()}
    except Exception as e:
        return 400, {"message": str(e)}


@router.post("/me/disable-mfa", response={200: dict, 400: dict})
def disable_mfa(request):
    """Disable MFA for the current user"""
    user = request.auth

    if not user.mfa_enabled:
        return 400, {"message": "MFA is not enabled"}

    try:
        user.disable_mfa()
        return 200, {"message": "MFA disabled successfully"}
    except Exception as e:
        return 400, {"message": str(e)}


# Admin-only endpoints
@router.get("/users", response=list[UserBasicSchema])
def list_users(request):
    """List all users (admin only)"""
    if not request.auth.is_staff:
        return 403, {"message": "Admin access required"}

    return [UserBasicSchema.from_orm(user) for user in User.objects.all()]


@router.get("/users/{user_id}", response=UserDetailSchema)
def get_user(request, user_id: int):
    """Get details of a specific user (admin only)"""
    if not request.auth.is_staff:
        return 403, {"message": "Admin access required"}

    try:
        user = User.objects.get(id=user_id)
        return UserDetailSchema.from_orm(user)
    except User.DoesNotExist:
        return 404, {"message": "User not found"}


@router.put("/users/{user_id}", response=UserDetailSchema)
def update_user(request, user_id: int, data: UserUpdateSchema):
    """Update a specific user (admin only)"""
    if not request.auth.is_staff:
        return 403, {"message": "Admin access required"}

    try:
        user = User.objects.get(id=user_id)

        if data.name:
            user.name = data.name
        if data.email:
            user.email = data.email
        if data.is_active is not None:
            user.is_active = data.is_active

        user.save()
        return UserDetailSchema.from_orm(user)
    except User.DoesNotExist:
        return 404, {"message": "User not found"}


@router.delete("/users/{user_id}")
def delete_user(request, user_id: int):
    """Delete a user (admin only)"""
    if not request.auth.is_staff:
        return 403, {"message": "Admin access required"}

    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return 200, {"message": "User deleted successfully"}
    except User.DoesNotExist:
        return 404, {"message": "User not found"}


# Register the router
api.add_router("/auth/", router)
