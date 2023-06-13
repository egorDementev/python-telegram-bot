from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from data_provider import get_go_to_menu_kb, get_bot_token, get_support_kb

bot = Bot(token=get_bot_token())
dp = Dispatcher(bot)


# support
async def support(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    await callback_query.message.answer_photo(open("resources/pictures/support.png", "rb"),
                                              caption="Пожалуйста, выберите тему обращения ❤",
                                              reply_markup=get_support_kb())


# support bot
async def sup_bot(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    await callback_query.message.answer_photo(open("resources/pictures/support.png", "rb"),
                                              caption="Опишите свой вопрос максимально подробно!\nОтправьте "
                                                      "сообщение вида:\nsup_bot/<ваш вопрос>\nВ противном случае, "
                                                      "наша команда не сможет его увидеть...",
                                              reply_markup=get_go_to_menu_kb())


# support psy
async def sup_psy(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    await callback_query.message.answer_photo(open("resources/pictures/support.png", "rb"),
                                              caption="Опишите свой вопрос максимально подробно!\nОтправьте "
                                                      "сообщение вида:\nsup_psy/<ваш вопрос>\nВ противном случае, "
                                                      "наша команда не сможет его увидеть...",
                                              reply_markup=get_go_to_menu_kb())


# инициализация функций для технической поддержки
def init_support_application(telegram_bot, dispatcher):
    global bot, dp

    bot = telegram_bot
    dp = dispatcher

    dp.callback_query_handler(lambda c: c.data and c.data.startswith('support'))(support)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('sup_bot'))(sup_bot)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('sup_psy'))(sup_psy)
