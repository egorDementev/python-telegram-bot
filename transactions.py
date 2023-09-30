from datetime import datetime
from sqlite3 import OperationalError

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher

from data_provider import get_data_base_object, get_go_to_menu_kb, get_bot_token, get_admin_list, get_super_admin_id
from start_application import write_log_to_file

bot = Bot(token=get_bot_token())
dp = Dispatcher(bot)


async def insert_into_tran(user_id, psy_id, count_consults, comment):
    con = get_data_base_object()

    try:

        with con:
            tran_id = len(list(con.execute(f"SELECT * FROM Transactions;"))) + 1

        sql1, data = 'INSERT INTO Transactions (id, user_id, date, time, psy_id, count_consults, comment) ' \
                     'values(?, ?, ?, ?, ?, ?, ?)', []

        data.append((tran_id, user_id, str(datetime.today().date().isoformat()), str(datetime.today().time().isoformat()),
                     psy_id, count_consults, comment))

        with con:
            con.executemany(sql1, data)

        await create_consult(tran_id, user_id)

    except OperationalError:
        await bot.send_message(user_id, "Похоже, что-то пошло не так...\n"
                                                            "Пожалуйста, сообщите о вашей проблеме в тех.поддержку",
                               reply_markup=get_go_to_menu_kb())

        error_text = f"ERROR: insert_into_tran_error [{datetime.now().isoformat()}] " \
                     f"UserID={user_id}"

        await bot.send_message(get_super_admin_id(), error_text, reply_markup=None)
        await write_log_to_file('errors.txt', error_text)


# create tran (or diagnostic consult)
async def create_tran(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    data = callback_query.data.split('_')
    psy_id = data[2]
    count_consults = data[3]

    if int(count_consults) == 0:
        await insert_into_tran(int(callback_query.from_user.id), int(psy_id), int(count_consults), data[4])

    else:
        if payment():
            await insert_into_tran(int(callback_query.from_user.id), int(psy_id), int(count_consults), "-")
        else:
            await bot.send_message(callback_query.from_user.id,
                                   "Произошла неизвестная ошибка при оплате...\nПожалуйста, обратитесь в поддержку!!!",
                                   reply_markup=get_go_to_menu_kb())


async def create_consult(tran_id, user_id):
    con = get_data_base_object()

    try:
        with con:
            number = int(list(con.execute(f"SELECT count_consults FROM Transactions WHERE id={tran_id};"))[0][0])
            con_id = len(list(con.execute(f"SELECT * FROM Consultation;")))
            comment = str(list(con.execute(f"SELECT comment FROM Transactions WHERE id={tran_id};"))[0][0])
            psy_id = int(list(con.execute(f"SELECT psy_id FROM Transactions WHERE id={tran_id};"))[0][0])

        sql1 = 'INSERT INTO Consultation (id, tran_id, number, is_done, date_time) ' \
               'values(?, ?, ?, ?, ?)'

        if number == 0:
            data = []
            data.append((con_id, tran_id, number, 0, comment))

            with con:
                con.executemany(sql1, data)

            await bot.send_message(user_id, "Поздравляем, вы записались на диагностическую встречу!!!\nВскоре, "
                                            "психолог свяжется с тобой для обсуждения времени консультации!\n"
                                            "Информацию о ваших консультациях вы можете посмотреть в личном профиле.",
                                   reply_markup=get_go_to_menu_kb())

            await bot.send_message(psy_id, f"Новый клиент записался к вам на диагностику на {comment}!\n"
                                           f"Подробную информацию можно посмотреть в кабинете психолога!",
                                   reply_markup=get_go_to_menu_kb())

            for admin in get_admin_list():
                with con:
                    user_url = str(list(con.execute(f"SELECT url FROM Person WHERE id={user_id}"))[0][0])
                    psy_name = str(list(con.execute(f"SELECT name FROM Psychologist WHERE id={psy_id}"))[0][0])
                await bot.send_message(admin, f"ЗАПИСЬ НА ДИАГНОСТИКУ\nКлиент: {user_url}\nUserID: {user_id}\nПсихолог: "
                                              f"{psy_name}")
        else:
            for i in range(number):
                data = []
                data.append((con_id, tran_id, i + 1, 0, comment))
                con_id += 1

                with con:
                    con.executemany(sql1, data)

            await bot.send_message(user_id, f"Поздравляем, вы успешно приобрели пакет консультаций "
                                            f"в количестве: {number} !!!\nВскоре, "
                                            "психолог свяжется с тобой для обсуждения времени консультации!\n"
                                            "Информацию о ваших консультациях вы можете посмотреть в личном профиле.",
                                   reply_markup=get_go_to_menu_kb())

            await bot.send_message(psy_id, f"Клиент приобрел у вас пакет консультаций в количестве: {number} !!\n"
                                           f"Подробную информацию можно посмотреть в кабинете психолога!",
                                   reply_markup=get_go_to_menu_kb())

    except OperationalError:
        await bot.send_message(user_id, "Похоже, что-то пошло не так...\n"
                                        "Пожалуйста, сообщите о вашей проблеме в тех.поддержку",
                               reply_markup=get_go_to_menu_kb())

        error_text = f"ERROR: create_consult_error [{datetime.now().isoformat()}] " \
                     f"UserID={user_id} " \
                     f"UserURL={user_url}"

        await bot.send_message(get_super_admin_id(), error_text, reply_markup=None)
        await write_log_to_file('errors.txt', error_text)



async def payment():
    return True


# инициализация функций создания транзакции и оплаты
def init_transactions_application(telegram_bot, dispatcher):
    global bot, dp

    bot = telegram_bot
    dp = dispatcher

    dp.callback_query_handler(lambda c: c.data and c.data.startswith('create_tran_'))(create_tran)
    # dp.pre_checkout_query_handler(lambda query: True)(process_pre_checkout_query)
    # dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)(process_successful_payment)
