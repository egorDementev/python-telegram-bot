from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data_provider import get_go_to_menu_kb, get_data_base_object, get_bot_token, get_psycho_kb, get_admin_list, \
    is_can_be_deleted

bot = Bot(token=get_bot_token())
dp = Dispatcher(bot)


# psycho меню
async def psycho_page(callback_query: types.CallbackQuery):
    if is_can_be_deleted(callback_query.message.date):
        await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, 'Кабинет психолога', reply_markup=get_psycho_kb())


# all consults (psy page)
async def psy_consults(callback_query: types.CallbackQuery):
    if is_can_be_deleted(callback_query.message.date):
        await callback_query.message.delete()

    con = get_data_base_object()
    list_of_my_consults = []

    await bot.send_message(callback_query.from_user.id, 'Ваши текущие консультации, на которые кто-то записался:',
                           reply_markup=get_go_to_menu_kb())

    with con:
        lst_of_cons = list(con.execute(f"SELECT tran_id, number, date_time, id FROM Consultation WHERE is_done={0}"))

        for consult in lst_of_cons:
            con_data = list(con.execute(f"SELECT user_id, psy_id, count_consults, comment "
                                        f"FROM Transactions WHERE id={consult[0]}"))[0]
            print(con_data)
            if str(con_data[1]) == str(callback_query.from_user.id):
                list_of_my_consults.append([con_data[0], con_data[2], con_data[3], consult[1], consult[2], consult[3]])

    for consult in list_of_my_consults:
        if consult[1] == 0:
            with con:
                user_url = str(list(con.execute(f"SELECT url FROM Person WHERE id={consult[0]}"))[0][0])
            print(consult[0])

            message = 'Диагностическая встреча:\nКлиент - ' + user_url + \
                      '\nДата консультации - ' + \
                      str(consult[4])

            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton('Отметить консультацию проведенной', callback_data='done_con_' +
                                                                                           str(consult[5]) + '_' +
                                                                                           str(consult[0])))
            kb.add(InlineKeyboardButton('Изменить дату и время консультации', callback_data='set_date_time_' +
                                                                                            str(consult[5])))

            await bot.send_message(callback_query.from_user.id, message, reply_markup=kb)
        else:
            pass


# mark consultation as done
async def done_con(callback_query: types.CallbackQuery):
    if is_can_be_deleted(callback_query.message.date):
        await callback_query.message.delete()

    con = get_data_base_object()

    data = callback_query.data.split('_')
    con_id, user_id, psy_id = data[2], data[3], callback_query.from_user.id

    with con:
        con.execute(f"UPDATE Consultation SET is_done={1} WHERE id={con_id}")
        psy_name = str(list(con.execute(f"SELECT name FROM Psychologist WHERE id={psy_id}"))[0][0])
        con_data = str(list(con.execute(f"SELECT date_time FROM Consultation WHERE id={con_id}"))[0][0])
        user_url = str(list(con.execute(f"SELECT url FROM Person WHERE id={user_id}"))[0][0])

    await bot.send_message(callback_query.from_user.id, 'Консультация успешно отмечена как проведенная!',
                           reply_markup=get_go_to_menu_kb())

    await bot.send_message(int(user_id), f"Психолог - {psy_name} - отметил консультацию, которая была запланирована на "
                                    f"{con_data}, как проведенную!\nЕсли эта консультация не проводилась с "
                                    f"психологом, то напишите, пожалуйста в тех.поддержку!")

    for admin in get_admin_list():
        await bot.send_message(admin, f"ПРОВЕДЕНА КОНСУЛЬТАЦИЯ\nКлиент: {user_url}\nUserID: {user_id}\nПсихолог: "
                                      f"{psy_name}\nConsultationID: {con_id}\nДата и время консультации: {con_data}")


# работает только для диагностических встреч
async def change_date_time(callback_query: types.CallbackQuery):
    if is_can_be_deleted(callback_query.message.date):
        await callback_query.message.delete()

    con_id = callback_query.data.split('_')[-1]

    message = f'Для того, чтобы изменить время и дату консультации напишите такое сообщение: {con_id}/<полная дата ' \
              f'и время консультации в любом удобном для вас формате>\nПример: {con_id}/10.10.2023 10:45 мск\n' \
              f'Для удобства скопируйте и дополните следующее сообщение'

    await bot.send_message(callback_query.from_user.id, message, reply_markup=None)
    await bot.send_message(callback_query.from_user.id, f'{con_id}/', reply_markup=None)


# инициализация функций для психолога
def init_psycho_application(telegram_bot, dispatcher):
    global bot, dp

    bot = telegram_bot
    dp = dispatcher

    dp.callback_query_handler(lambda c: c.data and c.data.startswith('psycho'))(psycho_page)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('my_consults'))(psy_consults)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('done_con'))(done_con)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('set_date_time_'))(change_date_time)
