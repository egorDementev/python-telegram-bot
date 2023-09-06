from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from data_provider import get_continue_kb, get_main_buttons_kb, get_admin_list, get_data_base_object, \
    get_go_to_menu_kb, get_bot_token
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token=get_bot_token())
dp = Dispatcher(bot)


# самое первое сообщение при старте бота
async def start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'ППППривет, мы очень рады видеть тебя в нашем боте! Давай пройдем короткую регистрацию, '
                           'после чего ты сможешь полноценно пользоваться услугами нашего бота ❤️',
                           reply_markup=get_continue_kb())


# главное меню
async def home_page(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    all_main_buttons = get_main_buttons_kb()
    con = get_data_base_object()

    main_menu = InlineKeyboardMarkup(row_width=1)

    if str(callback_query.from_user.id) in get_admin_list():
        main_menu.add(all_main_buttons[-1])

    with con:
        psycho_list = [str(x[0]) for x in list(con.execute(f"SELECT id FROM Psychologist;"))]

    if str(callback_query.from_user.id) in psycho_list:
        main_menu.add(all_main_buttons[-2])

    for x in range(len(all_main_buttons) - 2):
        main_menu.add(all_main_buttons[x])
    await callback_query.message.answer_photo(open("resources/pictures/logo.png", "rb"),
                                              caption='Привет 👋\nВыбери одну из функций:',
                                              reply_markup=main_menu)


# user account page
async def user_account(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    con = get_data_base_object()

    future_consultation = []
    count_consult_without_slot = 0

    with con:
        list_con = list(con.execute(f"SELECT tran_id, slot_id FROM Consultation WHERE is_done='0'"))

    print(list_con)

    for i in list_con:
        if i[1] is None:
            with con:
                lst = list(con.execute(f"SELECT user_id FROM Transactions WHERE id={i[0]}"))
            if str(lst[0][0]) == str(callback_query.from_user.id):
                count_consult_without_slot += 1
        else:
            with con:
                lst = list(con.execute(f"SELECT user_id FROM Transactions WHERE id={i[0]}"))
            if str(lst[0][0]) == str(callback_query.from_user.id):
                with con:
                    future_consultation.append(list(con.execute(f"SELECT date, time, psycho_id FROM "
                                                                f"Slot WHERE id={i[1]}")))

    message = "Привет 😊\nКонсультации, которые ты записался(ась):"
    await callback_query.message.answer_photo(open('resources/pictures/user.png', "rb"), caption=message,
                                              reply_markup=get_go_to_menu_kb())

    for x in future_consultation:
        with con:
            psy_name = list(con.execute(f"SELECT name FROM Psychologist WHERE id={x[0][2]}"))[0][0]
        mess = "Психолог: " + str(psy_name) + "\nДата и время консультации: " + str(x[0][0]) + "  " + str(x[0][1])
        await bot.send_message(callback_query.from_user.id, mess, reply_markup=None)


# обработка текстовых сообщений
async def user_problems(message: types.Message):
    con = get_data_base_object()

    with con:
        psycho_list = [str(x[0]) for x in list(con.execute(f"SELECT id FROM Psychologist;"))]
        print(psycho_list)

    if message.text[:3] == 'add' and (str(message.from_user.id) == '596752948' or str(message.from_user.id)
                                      == '840638420'):
        mass = message.text.split('/')
        sql1, data1 = 'INSERT INTO Psychologist (id, name, about, photo, rating) values(?, ?, ?, ?, ?)', []
        data1.append((mass[1], mass[2], mass[3], 'нет фото', 0))

        with con:
            con.executemany(sql1, data1)

        await bot.send_message(message.from_user.id, '10x', reply_markup=get_go_to_menu_kb())
    elif message.text[:3] == 'del' and (str(message.from_user.id) == '596752948' or str(message.from_user.id)
                                        == '840638420'):

        with con:
            con.execute(f"DELETE from Psychologist WHERE id='{message.text[4:]}'")

        await bot.send_message(message.from_user.id, 'Психолог удален')

    elif message.text[:4] == 'slot' and str(message.from_user.id) in psycho_list:
        mass = message.text.split('/')
        sql1 = 'INSERT INTO Slot (id, psycho_id, date, time, is_free) values(?, ?, ?, ?, ?)'

        with con:
            lst = list(con.execute(f"SELECT * FROM Slot"))
        with con:
            if len(lst) > 0:
                count = int(list(con.execute(f"SELECT MAX(id) FROM Slot"))[0][0])
            else:
                count = 0

        for x in range(1, len(mass)):
            dt = mass[x].split()
            data1 = [(count + x, int(message.from_user.id), dt[0], dt[1], 1)]

            with con:
                con.executemany(sql1, data1)

        await bot.send_message(message.from_user.id, 'Ваши слоты установлены', reply_markup=get_go_to_menu_kb())
    elif message.text[:3] == 'all' and (str(message.from_user.id) == '596752948' or str(message.from_user.id)
                                        == '840638420'):
        mass = message.text.split('/')

        with con:
            user_list = list(con.execute(f"SELECT id FROM Person"))

        for user in user_list:
            await bot.send_message(user[0], mass[1])
    else:
        await bot.send_message(message.from_user.id, 'Некорректный ввод данных. Попробуйте снова',
                               reply_markup=get_go_to_menu_kb())


# начало работы всего приложения
def init_start_application(telegram_bot, dispatcher):
    global bot, dp

    bot = telegram_bot
    dp = dispatcher
    dp.message_handler(commands=['start', 'help'])(start)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('menu'))(home_page)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('user_account'))(user_account)
    dp.message_handler()(user_problems)
