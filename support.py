from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from data_provider import get_go_to_menu_kb, get_bot_token, get_support_kb, is_can_be_deleted

bot = Bot(token=get_bot_token())
dp = Dispatcher(bot)


# support
async def support(callback_query: types.CallbackQuery):
    if is_can_be_deleted(callback_query.message.date):
        await callback_query.message.delete()

    await callback_query.message.answer_photo(open("resources/pictures/support.png", "rb"),
                                              caption="Пожалуйста, выберите тему обращения ❤",
                                              reply_markup=get_support_kb())


# инициализация функций для технической поддержки
def init_support_application(telegram_bot, dispatcher):
    global bot, dp

    bot = telegram_bot
    dp = dispatcher

    dp.callback_query_handler(lambda c: c.data and c.data.startswith('support'))(support)
