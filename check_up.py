from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher

from data_provider import get_go_to_menu_kb, get_data_base_object, get_check_up_kb, get_check_kb, get_questions, \
    get_bot_token
from database.work_with_db import if_check, count_today_check_ups, write_check_up
from draw import create_graphs, photo_del

bot = Bot(token=get_bot_token())
dp = Dispatcher(bot)


# меню с кнопками про чек-ап
async def my_feeling(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer_photo(open("resources/pictures/check_up.png", "rb"),
                                              caption='Давай вспомним, как прошел твой день ❤️\n'
                                                      'Тут ты можешь порефлексировать и оценить свое состояние!\n\n'
                                                      'А если ты не знаешь, зачем отвечать на вопросы из бота, '
                                                      'и может ли саморефлексия ухудшить состояние человека, '
                                                      'то советуем прочитать статью на нашем сайте, в которой '
                                                      'мы ответили на эти вопросы!',
                                              reply_markup=get_check_up_kb())


# отправка графиков
async def send_check_ups(cq):
    media = types.MediaGroup()
    media.attach_photo(types.InputFile('resources//files//' + str(cq.from_user.id) + "_mood.png"),
                       caption='📈 На сегодняшний день графики вашего состояния выглядят так:')
    media.attach_photo(types.InputFile('resources//files//' + str(cq.from_user.id) + "_calmness.png"))
    media.attach_photo(types.InputFile('resources//files//' + str(cq.from_user.id) + "_productivity.png"))
    media.attach_photo(types.InputFile('resources//files//' + str(cq.from_user.id) + "_environment.png"))
    media.attach_photo(types.InputFile('resources//files//' + str(cq.from_user.id) + "_self_confidence.png"))
    media.attach_photo(types.InputFile('resources//files//' + str(cq.from_user.id) + "_pacification.png"))
    media.attach_photo(types.InputFile('resources//files//' + str(cq.from_user.id) + "_self_satisfaction.png"))
    await bot.send_media_group(cq.from_user.id, media=media)
    await bot.send_message(cq.from_user.id,
                           'С заботой, твой connection ❤️', reply_markup=get_go_to_menu_kb())


# функция, которая отвечает за сбор данных о состоянии пользователя
async def process_check_up(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    code = int(callback_query.data[3:])
    count = count_today_check_ups(callback_query.from_user.id)
    write_check_up(callback_query.from_user.id, code, count)

    if count < 6:
        await bot.send_message(callback_query.from_user.id, get_questions()[count], reply_markup=get_check_kb())
    else:

        create_graphs(callback_query.from_user.id)
        media = types.MediaGroup()
        media.attach_photo(types.InputFile('resources/pictures/check_up.png'))
        await bot.send_media_group(callback_query.from_user.id, media=media)

        await send_check_ups(callback_query)

        photo_del(callback_query.from_user.id)


# функция, которая отвечает за проверку, проходил ли человек чек-ап и вывод прошлых результатов
async def is_check_up_done(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    code = callback_query.data[3:]
    if int(code) == 1:
        if if_check(callback_query.from_user.id):
            await bot.send_message(callback_query.from_user.id, 'Какое у тебя настроение сегодня? '
                                                                'Как ты себя чувствуешь?',
                                   reply_markup=get_check_kb())
        else:
            await bot.send_message(callback_query.from_user.id, 'Вы уже отследили свое состояние сегодня ❤️',
                                   reply_markup=get_go_to_menu_kb())
    else:
        con = get_data_base_object()
        cursor = con.cursor()
        sqlite_select_query = f"SELECT * from CheckUp where user_id='{callback_query.from_user.id}'"
        cursor.execute(sqlite_select_query)
        last_date = cursor.fetchall()
        if last_date:
            create_graphs(callback_query.from_user.id)

            await send_check_ups(callback_query)

            photo_del(callback_query.from_user.id)
        else:
            await bot.send_message(callback_query.from_user.id, 'Вы еще ни разу не отслеживали свое состояние ❤️',
                                   reply_markup=get_go_to_menu_kb())


# инициализация функций для прохождения и показа состояния
def init_checkup_application(telegram_bot, dispatcher):
    global bot, dp

    bot = telegram_bot
    dp = dispatcher

    dp.callback_query_handler(lambda c: c.data and c.data.startswith('my_feeling'))(my_feeling)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('chk'))(is_check_up_done)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('con'))(process_check_up)
