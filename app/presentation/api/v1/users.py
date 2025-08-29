from fastapi import APIRouter, Depends, status
from app.presentation.schemas.user_schema import CreateUserRequest, UserResponse
from app.presentation.schemas.common_schema import StandardResponse
from app.application.use_cases.register_user import RegisterUserUseCase
from app.application.use_cases.get_user import GetUserUseCase
from app.presentation.api.dependencies import (
    register_user_use_case_dependency,
    get_user_use_case_dependency
)
from app.application.dto.user_dto import CreateUserDTO
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=StandardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user account with the provided information"
)
async def create_user(
    user_request: CreateUserRequest,
    register_use_case: RegisterUserUseCase = Depends(register_user_use_case_dependency)
):
    logger.info(f"Creating user with UID: {user_request.uid}")

    # Convert request schema to DTO
    create_user_dto = CreateUserDTO(
        uid=user_request.uid,
        email=user_request.email,
        name=user_request.name,
        piano_level=user_request.piano_level
    )

    # Execute use case
    user_response_dto = await register_use_case.execute(create_user_dto)
    
    # DTO → Schema
    user_response = UserResponse(
        uid=user_response_dto.uid,
        email=user_response_dto.email,
        name=user_response_dto.name,
        piano_level=user_response_dto.piano_level
    )
    
    # Return standardized response
    response = StandardResponse.created(
        data=user_response.dict(),
        message="User created successfully"
    )

    logger.info(f"User created successfully: {user_request.uid}")
    return response


@router.get(
    "/{uid}",
    response_model=StandardResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user by UID",
    description="Retrieve a single user by UID"
)
async def get_user_by_id(
    uid: str,
    get_user_use_case: GetUserUseCase = Depends(get_user_use_case_dependency)
):
    logger.info(f"Fetching user with UID: {uid}")

    user_response_dto = await get_user_use_case.get_by_id(uid)
    
    # DTO → Schema
    user_response = UserResponse(
        uid=user_response_dto.uid,
        email=user_response_dto.email,
        name=user_response_dto.name,
        piano_level=user_response_dto.piano_level
    )
    
    logger.info(f"User fetched successfully: {uid}")
    
    return StandardResponse.success(
        data=user_response.dict(),
        message="User retrieved successfully"
    )
   

@router.get(
    "/",
    response_model=StandardResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all users",
    description="Retrieve all users in the system"
)
async def get_all_users(
    get_user_use_case: GetUserUseCase = Depends(get_user_use_case_dependency)
):
    logger.info("Fetching all users")

    users_response_dto = await get_user_use_case.get_all()

    # DTOs → Schemas
    users_response = [
        UserResponse(
            uid=user.uid,
            email=user.email,
            name=user.name,
            piano_level=user.piano_level
        ) for user in users_response_dto
    ]
    
    logger.info(f"Retrieved {len(users_response_dto)} users successfully")
    
    return StandardResponse.success(
        data=[user.dict() for user in users_response],
        message="All users retrieved successfully"
    )