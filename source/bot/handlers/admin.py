from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from ...config import Config
from ...service.competitions.models import CompetitionState, Competition

router = Router()


async def is_admin(message: Message):
    if Config.TELEGRAM_ADMIN_ID != message.from_user.id:
        await message.answer("✋ Вы не являетесь администратором площадки")
        return False

    return True


@router.message(Command("settings"))
async def settings_message(
    message: Message
):
    if not await is_admin(message):
        return

    await message.answer(
        text="Админ-панель площадки",
        reply_markup=InlineKeyboardBuilder()
        .button(text="Добавить олимпиаду", callback_data="new_competition")
        .button(text="Сменить состояние олимпиады", callback_data="change_state")
        .button(text="Отправить сообщение пользователям", callback_data="mail_users")
        .adjust(1, 1)
        .as_markup()
    )


@router.callback_query(F.data == "change_state")
async def select_competitions_state(query: CallbackQuery):
    await query.message.edit_text("Выберите состояние олимпиад")
    await query.message.edit_reply_markup(
        reply_markup=InlineKeyboardBuilder()
        .button(text="Регистрация", callback_data="change_state:registration")
        .button(text="Завтрак", callback_data="change_state:breakfast")
        .adjust(1, 1, )
        .as_markup()
    )


@router.callback_query(F.data.startswith("change_state"))
async def change_competitions_state(query: CallbackQuery, session: AsyncSession):
    new_state = query.data.split(":")[1]

    state_from_db_query = await session.execute(
        select(CompetitionState)
        .where(CompetitionState.type == new_state)
    )

    state_from_db: CompetitionState = state_from_db_query.scalars().one_or_none()

    if state_from_db:
        await session.execute(
            update(Competition)
            .values({'state_id': state_from_db.id})
        )
        await session.commit()
        await query.message.answer("Состояние олимпиад обновлено")
