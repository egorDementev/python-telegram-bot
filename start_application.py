from sqlite3 import OperationalError

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from data_provider import get_continue_kb, get_main_buttons_kb, get_admin_list, get_data_base_object, \
    get_go_to_menu_kb, get_bot_token
from aiogram.types import InlineKeyboardMarkup

bot = Bot(token=get_bot_token())
dp = Dispatcher(bot)

admins_id_list = get_admin_list()


# самое первое сообщение при старте бота
async def start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Привет, мы очень рады видеть тебя в нашем боте проекта Connection ❤️!\n'
                           'Для начала, давай познакомимся с возможностями этого бота!\n\n'
                           '‼️ Бот запущен в тестовом режиме, при возникновении каких-либо проблем просим писать '
                           'в тех.поддержку!!',
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
                                              caption='Привет 👋\nБлагодарим за доверие к нашему сервису ❤️',
                                              reply_markup=main_menu)


# user account page
async def user_account(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    con = get_data_base_object()

    future_consultations = []
    future_diagnostics = []

    with con:
        list_con = list(con.execute(f"SELECT tran_id, number FROM Consultation WHERE is_done='0'"))

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

    message = "Привет 😊\nВ личном кабинете будут отображаться консультации, на которые ты записался(лась)!"
    await callback_query.message.answer_photo(open('resources/pictures/user.png', "rb"), caption=message,
                                              reply_markup=get_go_to_menu_kb())

    if future_diagnostics:
        for x in future_diagnostics:
            with con:
                psy_name = list(con.execute(f"SELECT name FROM Psychologist WHERE id={x[0]};"))[0][0]
            mess = "🧩 Диагностическая встреча\nПсихолог: " + psy_name + "\nДата встречи: " + \
                   x[1] + "\nПсихолог с вами обязательно свяжется заранее, " \
                          "чтобы обсудить время проведения консультации 💖\n" \
                          "Если у вас есть какие-либо вопросы, или вам нужно " \
                          "связаться с психологом, то напишите, " \
                          "пожалуйста в тех. поддержку!"
            await bot.send_message(callback_query.from_user.id, mess, reply_markup=None)

        for x in future_consultations:
            with con:
                psy_name = list(con.execute(f"SELECT name FROM Psychologist WHERE id={x[0]}"))[0][0]
            mess = "💖 Консультация с психологом\nПсихолог: " + psy_name + "\nНомер консультации в пакете: " + \
                   str(x[1]) + "\nПсихолог обязательно с вами свяжется заранее, чтобы обсудить время проведения " \
                               "консультации ❤️\nЕсли у вас есть какие-то вопросы, или вам нужно связаться с " \
                               "психологом, то напишите в тех. поддержку!"
            await bot.send_message(callback_query.from_user.id, mess, reply_markup=None)


async def send_guide(callback_query: types.CallbackQuery):
    con = get_data_base_object()

    await bot.send_document(callback_query.from_user.id, open("resources/documents/как не увязать в рутине и "
                                                              "учебе и проживать студенческую жизнь ярко.pdf", "rb"),
                            caption="Наша команда очень надеется, что данный гайд окажется полезным для тебя ❤️",
                            reply_markup=None)

    with con:
        con.execute(f"UPDATE Person SET get_guide={1} WHERE id={callback_query.from_user.id};")


# функция предоставляет администратору данные, полученные sql-запросом
async def sql_request(request, admin_id):
    con = get_data_base_object()

    try:
        with con:
            answer = str(list(con.execute(request)))

        await bot.send_message(admin_id, answer, reply_markup=None)

    except OperationalError:
        await bot.send_message(admin_id, "Ошибка внутри запроса", reply_markup=None)


# функция добавляет нового психолога в базу данных
async def add_new_psychologist(data, admin_id):
    con = get_data_base_object()

    sql1, data1 = 'INSERT INTO Psychologist (id, name, about, photo) values(?, ?, ?, ?)', []
    data1.append((data[1], data[2], data[3], 'нет фото'))

    try:
        with con:
            con.executemany(sql1, data1)

        await bot.send_message(admin_id, 'Теперь отправь сюда фото психолога (не как файл)',
                               reply_markup=get_go_to_menu_kb())
    except OperationalError:
        await bot.send_message(admin_id, "Неизвестная ошибка...", reply_markup=None)


# функция удаляет психолого из базы данных
async def delete_psychologist(data, admin_id):
    con = get_data_base_object()

    try:
        with con:
            con.execute(f"DELETE from Psychologist WHERE id='{data}'")

        await bot.send_message(admin_id, 'Психолог удален')

    except OperationalError:
        await bot.send_message(admin_id, "Неизвестная ошибка...", reply_markup=None)


# функция делает текстовую рассылку по всем пользователям
async def mailing(data):
    con = get_data_base_object()

    try:
        with con:
            user_list = list(con.execute(f"SELECT id FROM Person"))

        for user in user_list:
            await bot.send_message(user[0], data)

    except OperationalError:
        for user in admins_id_list:
            await bot.send_message(user, "Неизвестная ошибка...", reply_markup=None)


async def set_date_time_of_consultation(con_id, date_time):
    con = get_data_base_object()

    date_time = '/'.join(date_time)
    print(date_time)

    with con:
        con.execute(f"UPDATE Consultation SET date_time='{str(date_time)}' WHERE id={con_id};")
        tran_id = list(con.execute(f"SELECT tran_id FROM Consultation WHERE id={con_id}"))[0][0]
        con.execute(f"UPDATE Transactions SET comment='{str(date_time)}' WHERE id={tran_id};")
        data = list(con.execute(f"SELECT user_id, psy_id FROM Transactions WHERE id={tran_id};"))[0]
        psy_name = str(list(con.execute(f"SELECT name FROM Psychologist WHERE id={data[1]}"))[0][0])
        user_url = str(list(con.execute(f"SELECT url FROM Person WHERE id={data[0]}"))[0][0])

    await bot.send_message(data[0], f"Психолог - {psy_name} - изменил время консультации на {date_time}!\nЕсли "
                                    f"у вас есть какие-то вопросы, то обратитесь в тех.поддержку!")

    for admin in get_admin_list():
        await bot.send_message(admin, f"ИЗМЕНЕНИЕ ВРЕМЕНИ КОНСУЛЬТАЦИИ\nКлиент: {user_url}\nUserId: {data[0]}\n"
                                      f"Психолог: {psy_name}\nConsultationID: {con_id}\nДата и время "
                                      f"консультации: {date_time}")


# обработка текстовых сообщений
async def user_problems(message: types.Message):
    con = get_data_base_object()

    with con:
        psycho_list = [str(x[0]) for x in list(con.execute(f"SELECT id FROM Psychologist;"))]

    if message.text[:3] == 'add' and str(message.from_user.id) in admins_id_list:
        mass = message.text.split('/')
        await add_new_psychologist(mass, message.from_user.id)

    elif message.text[:3] == 'del' and str(message.from_user.id) in admins_id_list:
        await delete_psychologist(message.text[4:], message.from_user.id)

    elif message.text[:3] == 'all' and str(message.from_user.id) in admins_id_list:
        mass = message.text.split('/')
        await mailing(mass[1])

    elif message.text[:3] == 'sql' and str(message.from_user.id) in admins_id_list:
        await sql_request(message.text[4:], message.from_user.id)
    elif str(message.from_user.id) in psycho_list:
        try:
            await set_date_time_of_consultation(message.text.split('/')[0], message.text.split('/')[1:])
            await bot.send_message(message.from_user.id, 'Успешно!', reply_markup=get_go_to_menu_kb())
        except OperationalError:
            await bot.send_message(message.from_user.id, "Произошла неизвестная ошибка ...",
                                   reply_markup=get_go_to_menu_kb())

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
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('guide'))(send_guide)
    dp.message_handler()(user_problems)
