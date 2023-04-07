from aiogram import Router
from aiogram.types import Message

from app.db.functions import User, Awards

from app.filters.is_chat import IsChat

router = Router()


@router.message(IsChat(is_chat=False))
async def text_handler(message: Message):
    if message.text == 'Статистика':
        pos = await User.get_top_position(message.from_user.id)
        user = await User.get_data(message.from_user.id)
        refer = await User.get_data(user.refer)
        count = await User.get_count()

        if not refer:
            refer = User(id=0, name="Unknown")

        text = "🍅 Ваша статистика:\n\n"
        text += f" - Вы заразили: <b>{len(user.referrals)}</b>\n"
        text += f" - Вас заразили: <a href='tg://user?id={user.refer}'>{refer.name}</a>\n"
        text += f" - Всего заражено: <b>{count['confirmed']}/{count['all']}</b>\n"
        text += f" - Вы были заражены: <b>{user.register_date}</b>\n"
        text += f" - Ваша ссылка для приглашения друзей: " \
                f"<code>https://t.me/tomatoclanbot?start={message.from_user.id}</code>\n"
        text += f" - Ваша позиция в рейтинге: <b>{pos}</b>"
        return await message.answer(text)

    if message.text == 'Топ':
        top = await User.get_top()
        text = "🍅 Топ 10:\n\n"
        for i, user in enumerate(top):
            text += f"{i+1}. <a href='tg://user?id={user.id}'>{user.name}</a> - {len(user.referrals)}\n"
        return await message.answer(text)

    if message.text == 'Профиль':
        user = await User.get_data(message.from_user.id)
        user_awards = user.awards
        awards = await Awards.get_all()
        badges = []
        for award in awards:
            if award.name in user_awards:
                badges.append(award.badge)
        text = "🍅 Ваш профиль:\n\n"
        text += f" - Имя: <b>{user.name}</b>\n"
        text += f" - Статус: <b>{user.status}</b>\n"
        text += f" - Баланс: <b>{user.balance}</b>\n"
        text += f" - Значки: <b>{', '.join(badges)}</b>\n"
        text += f" - Достижения: <b>{len(user_awards)}/{len(awards)}</b>\n"
        return await message.answer(text)
