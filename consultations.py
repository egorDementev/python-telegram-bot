from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data_provider import get_data_base_object, get_show_psycho_kb, get_go_to_menu_kb, get_types_of_consults, \
    get_bot_token
import datetime

bot = Bot(token=get_bot_token())
dp = Dispatcher(bot)


# окно с отображением информации о консультациях
async def need_help(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    await callback_query.message.answer_photo(open("resources/pictures/psy.png", "rb"),
                                              caption='Наша миссия - сделать тебя '
                                                      'счастливее ❤️\n\nУ нас ты можешь посетить бесплатную '
                                                      'диагностическую встречу с психологом, чтобы познакомиться, '
                                                      'сформировать запрос, '
                                                      'наметить план дальнейший действий!\nЭто поможет тебе выбрать '
                                                      'того психолога, который '
                                                      'будет тебе по душе 😊\n'
                                                      'Чтобы увидеть всех психологов, нажми на кнопку '
                                                      '"Хочу посмотреть всех психологов"',
                                              reply_markup=get_show_psycho_kb())
    await bot.send_message(callback_query.from_user.id, "🚨🚨🚨 Внимание 🚨🚨🚨\nБот запущен в режиме тестирования, "
                                                        "записаться на настоящую консультацию через него пока "
                                                        "нельзя!!\nВсе, что вы увидите дальше - это СИМУЛЯЦИЯ того, "
                                                        "как в дальнейшем будет происходить запись на "
                                                        "консультации!!\nЕсли вы хотите обратиться к психологу "
                                                        "через наш сервис, то вы можете записаться на "
                                                        "диагностическую встречу в нашем телеграм канале "
                                                        "(ссылка в описании бота)  \nС любовью, Connection ❤️",
                           reply_markup=None)


# показ психологов
async def psycho(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    con = get_data_base_object()

    with con:
        list_psy = list(con.execute(f"SELECT * FROM Psychologist"))

    code = int(callback_query.data[7:])
    but = InlineKeyboardMarkup(row_width=3)

    but.add(InlineKeyboardButton('⬅️', callback_data='all_psy' + str((code - 1) % len(list_psy))))
    but.add(InlineKeyboardButton('👩 Выбрать психолога',
                                 callback_data='psy_' + str(list_psy[code][0]) + '_' + str(code % len(list_psy))))
    but.add(InlineKeyboardButton('➡️', callback_data='all_psy' + str((code + 1) % len(list_psy))))
    but.add(InlineKeyboardButton('➡️ Главное меню', callback_data='menu'))

    await callback_query.message.answer_photo(open('psy_photo//' + str(list_psy[code][0]) + '.jpg', "rb"),
                                              caption=(list_psy[code][1] + '\n' + list_psy[code][2] +
                                                       '\nКоличество консультаций: ' +
                                                       str(list_psy[code][4])),
                                              reply_markup=but)


# показ слотов психологов
async def psy_slots(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    con = get_data_base_object()

    data = callback_query.data.split('_')
    psy_id = data[1]
    but = InlineKeyboardMarkup()
    if len(data) == 3:
        today = datetime.date.today()
        list_of_date = []

        with con:
            data_list = list(con.execute(f"SELECT date, id FROM Slot Where psycho_id='{psy_id}' and is_free='1';"))

        for date in data_list:
            if today <= datetime.date(int(date[0][:4]), int(date[0][5:7]), int(date[0][8:])):
                if date[0][8:] + '.' + date[0][5:7] not in list_of_date:
                    but.add(InlineKeyboardButton('📅 ' + date[0][8:] + '.' + date[0][5:7],
                                                 callback_data='psy_' + psy_id + '_' + str(date[0]) + '_' + data[2]))
                    # айди психолога, дата, номер психолога
                    list_of_date.append(date[0][8:] + '.' + date[0][5:7])
        but.add(InlineKeyboardButton('⬅️ Назад к психологам', callback_data='all_psy' + data[2]))

        await bot.send_message(callback_query.from_user.id, 'Пожалуйста, выберите наиболее подходящий для вас день ❤️',
                               reply_markup=but)
    else:
        date_of_slots = data[2]

        with con:
            time_list = list(con.execute(f"SELECT time, id FROM Slot WHERE psycho_id='{psy_id}' "
                                         f"and date='{date_of_slots}' and is_free='1';"))
        print(time_list)
        date_of_slots = date_of_slots.split('-')
        date_of_slots = [int(x) for x in date_of_slots]
        for time in time_list:
            slot_time = datetime.time.fromisoformat(time[0])
            now_time = datetime.time.fromisoformat(str(datetime.datetime.now().time()))
            #  + ':' + str(datetime.datetime.now().time().minute))
            if (now_time < slot_time and
                datetime.datetime.now() == datetime.datetime(date_of_slots[0], date_of_slots[1], date_of_slots[2])) or \
                    (datetime.datetime.now() < datetime.datetime(date_of_slots[0], date_of_slots[1], date_of_slots[2])):
                print(1)
                but.add(InlineKeyboardButton('⏰ ' + time[0], callback_data='reserve_slot_' + str(time[1])))
        but.add(InlineKeyboardButton('⬅️ Назад к психологам', callback_data='all_psy' + data[3]))

        await bot.send_message(callback_query.from_user.id, 'Пожалуйста, выберите наиболее подходящее для вас время ❤️',
                               reply_markup=but)


# choose type of slot
async def reserve_slot(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    con = get_data_base_object()

    slot_id = callback_query.data.split('_')[2]

    with con:
        list_con = list(con.execute(f"SELECT tran_id, slot_id FROM Consultation WHERE is_done='0'"))

    print(list_con)
    is_free_slot = 0

    for i in list_con:
        if i[1] is None:
            with con:
                lst = list(con.execute(f"SELECT user_id, id FROM Transactions WHERE id={i[0]}"))
            if str(lst[0][0]) == str(callback_query.from_user.id):
                with con:
                    con.execute(f"UPDATE Slot SET is_free='0' WHERE id='{slot_id}'")
                with con:
                    id_con = list(con.execute(f"SELECT id FROM Consultation WHERE tran_id={i[0]} "
                                              f"and slot_id is null"))[0][0]
                with con:
                    con.execute(f"UPDATE Consultation SET slot_id={slot_id} WHERE tran_id={i[0]} and id={id_con}")
                is_free_slot = 1
                await bot.send_message(callback_query.from_user.id,
                                       'Поздравляю, вы записаны на консультацию........! ❤️\n'
                                       'В личном кабинете вы можете посмотреть всю '
                                       'информацию о своих консультациях!',
                                       reply_markup=get_go_to_menu_kb())
                with con:
                    psy_id = list(con.execute(f"SELECT psycho_id FROM Slot WHERE id={slot_id}"))[0][0]

                await bot.send_message(psy_id, "Пользователь " + str(callback_query.from_user.id) +
                                       " к вам на консультацию!\nБолее подробную информацию можно посмотреть в личном "
                                       "кабинете психолога)")
        if is_free_slot == 1:
            break

    if not is_free_slot:

        with con:
            condition = list(con.execute(f"SELECT is_free FROM Slot WHERE id='{slot_id}'"))[0][0]

        if int(condition) == 1:
            # with con:
            #     con.execute(f"UPDATE Slot SET is_free='0' WHERE id='{slot_id}'")

            choose_type_of_consult = get_types_of_consults(slot_id)

            await bot.send_message(callback_query.from_user.id,
                                   'Пожалуйста, выберите тип услуги, которую хотите получить ❤️',
                                   reply_markup=choose_type_of_consult)
        else:
            await bot.send_message(callback_query.from_user.id, 'К сожалению, этот слот только заняли(\nПожалуйста, '
                                                                'выберите другой',
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton('⬅️ Назад к психологам', callback_data='all_psy' + '0')))


# инициализация функций показа психологов, слотов и записи на консультации
def init_consultations_application(telegram_bot, dispatcher):
    global bot, dp

    bot = telegram_bot
    dp = dispatcher

    dp.callback_query_handler(lambda c: c.data and c.data.startswith('need_help'))(need_help)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('all_psy'))(psycho)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('psy_'))(psy_slots)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('reserve_slot_'))(reserve_slot)
