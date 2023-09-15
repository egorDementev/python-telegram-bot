from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from data_provider import get_continue_kb, get_main_buttons_kb, get_admin_list, get_data_base_object, \
    get_go_to_menu_kb, get_bot_token
from aiogram.types import InlineKeyboardMarkup

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
    # await callback_query.message.delete()

    con = get_data_base_object()

    future_consultations = []
    future_diagnostics = []

    with con:
        list_con = list(con.execute(f"SELECT tran_id, number FROM Consultation WHERE is_done='0'"))

    print(list_con)

    for i in list_con:
        with con:
            lst = list(con.execute(f"SELECT user_id FROM Transactions WHERE id={int(i[0])}"))
        if str(lst[0][0]) == str(callback_query.from_user.id):
            if i[1] == 0:
                with con:
                    future_diagnostics.append(list(con.execute(f"SELECT psy_id, comment FROM "
                                                               f"Transactions WHERE id={int(i[0])};"))[0])
            else:
                with con:
                    future_consultations.append([list(con.execute(f"SELECT psy_id FROM Transactions "
                                                                  f"WHERE id={int(i[0])};"))[0][0], i[1]])

    message = "Привет 😊\nВ личном кабинете отображаются консультации, на которые ты записался(лась):"
    await callback_query.message.answer_photo(open('resources/pictures/user.png', "rb"), caption=message,
                                              reply_markup=get_go_to_menu_kb())

    if future_diagnostics:
        for x in future_diagnostics:
            print(x)
            with con:
                psy_name = list(con.execute(f"SELECT name FROM Psychologist WHERE id={x[0]};"))[0][0]
            print(psy_name)
            mess = "🧩 Диагностическая встреча\nПсихолог: " + psy_name + "\nДата встречи: " + \
                   x[1][8:] + "." + x[1][5:7] + "." + x[1][:4] + "\nПсихолог с вами обязательно свяжется заранее, " \
                                                                 "чтобы обсудить время проведения консультации 💖\n" \
                                                                 "Если у вас есть какие-либо вопросы, или вам нужно " \
                                                                 "связаться с психологом, то напишите, " \
                                                                 "пожалуйста в тех. поддержку!"
            await bot.send_message(callback_query.from_user.id, mess, reply_markup=None)

        for x in future_consultations:
            print(x)
            with con:
                psy_name = list(con.execute(f"SELECT name FROM Psychologist WHERE id={x[0]}"))[0][0]
            mess = "💖 Консультация с психологом\nПсихолог: " + psy_name + "\nНомер консультации с пакете: " + \
                   str(x[1]) + "\nПсихолог обязательно с вами свяжется заранее, чтобы обсудить время проведения " \
                               "консультации ❤️\nЕсли у вас есть какие-то вопросы, или вам нужно связаться с " \
                               "психологом, то напишите в тех. поддержку!"
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
        sql1, data1 = 'INSERT INTO Psychologist (id, name, about, photo) values(?, ?, ?, ?)', []
        data1.append((mass[1], mass[2], mass[3], 'нет фото'))

        with con:
            con.executemany(sql1, data1)

        await bot.send_message(message.from_user.id, '10x', reply_markup=get_go_to_menu_kb())
    elif message.text[:3] == 'del' and (str(message.from_user.id) == '596752948' or str(message.from_user.id)
                                        == '840638420'):

        with con:
            con.execute(f"DELETE from Psychologist WHERE id='{message.text[4:]}'")

        await bot.send_message(message.from_user.id, 'Психолог удален')

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
