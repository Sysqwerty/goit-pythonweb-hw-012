from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas import UserCreate, Token, User, RequestEmail, ResetPassword
from src.services.email_service import send_confirm_email, send_reset_password_email
from src.services.auth_service import create_access_token, Hash, get_email_from_token, get_password_from_token
from src.services.users_service import UserService
from src.database.db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


# Реєстрація користувача
@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, background_tasks: BackgroundTasks,
                        request: Request, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)

    email_user = await user_service.get_user_by_email(user_data.email)
    if email_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Користувач з таким email вже існує",
        )

    username_user = await user_service.get_user_by_username(user_data.username)
    if username_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Користувач з таким іменем вже існує",
        )
    user_data.password = Hash().get_password_hash(user_data.password)
    new_user = await user_service.create_user(user_data)
    background_tasks.add_task(
        send_confirm_email, new_user.email, new_user.username, request.base_url
    )

    return new_user


# Логін користувача
@router.post("/login", response_model=Token)
async def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    user = await user_service.get_user_by_username(form_data.username)
    if not user or not Hash().verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильний логін або пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Електронна адреса не підтверджена",
        )

    access_token = await create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/confirmed_email/{token}")
async def confirmed_email(token: str, db: AsyncSession = Depends(get_db)):
    email = await get_email_from_token(token)
    user_service = UserService(db)
    user = await user_service.get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error"
        )
    if user.confirmed:
        return {"message": "Ваша електронна пошта вже підтверджена"}
    await user_service.confirmed_email(email)
    return {"message": "Електронну пошту підтверджено"}


@router.post("/request_email")
async def request_email(
        body: RequestEmail,
        background_tasks: BackgroundTasks,
        request: Request,
        db: AsyncSession = Depends(get_db),
):
    user_service = UserService(db)
    user = await user_service.get_user_by_email(body.email)

    if user and user.confirmed:
        return {"message": "Ваша електронна пошта вже підтверджена"}
    if user:
        background_tasks.add_task(
            send_confirm_email, user.email, user.username, request.base_url
        )
    return {"message": "Перевірте свою електронну пошту для підтвердження"}


@router.post("/reset_password")
async def reset_password_request(
        body: ResetPassword,
        background_tasks: BackgroundTasks,
        request: Request,
        db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    user = await user_service.get_user_by_email(body.email)

    if not user:
        # Не повідомляємо, чи існує користувач
        return {"message": "Перевірте свою електронну пошту для скидання пароля"}

    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Електронна адреса не підтверджена"
        )

    hashed_password = Hash().get_password_hash(body.password)

    reset_token = await create_access_token(
        data={"sub": user.email, "password": hashed_password}
    )

    # Відправка email
    background_tasks.add_task(
        send_reset_password_email,
        to_email=body.email,
        username=user.username,
        host=str(request.base_url),
        reset_token=reset_token
    )

    return {"message": "Перевірте свою електронну пошту для скидання пароля"}


@router.get("/confirm_reset_password/{token}")
async def confirm_reset_password(
        token: str,
        db: AsyncSession = Depends(get_db)
):
    email = await get_email_from_token(token)
    hashed_password = await get_password_from_token(token)

    if not email or not hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Недійсний або прострочений токен"
        )

    user_service = UserService(db)
    user = await user_service.get_user_by_email(email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Користувача з такою електронною поштою не знайдено"
        )

    # Оновлення пароля
    await user_service.reset_password(user.id, hashed_password)

    return {"message": "Пароль успішно оновлено"}
