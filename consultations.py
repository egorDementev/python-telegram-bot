from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data_provider import get_data_base_object, get_show_psycho_kb, get_bot_token, is_can_be_deleted

bot = Bot(token=get_bot_token())
dp = Dispatcher(bot)

sites_about_psychologists = {'332399557': 'http://connection.online.tilda.ws/viktoria_vagapova',
                             '807143565': 'http://connection.online.tilda.ws/anastasia_diveikina',
                             '283800610': 'http://connection.online.tilda.ws/psychologist_natalia_kulikova',
                             '596752948': 'https://t.me/egor_dementev'}


# Функция, которая возвращает список из ближайших 7 дней без субботы и воскресенья
def get_next_7_weekdays():
    today = datetime.today()

    day_names = {0: "Пн", 1: "Вт", 2: "Ср", 3: "Чт", 4: "Пт", 5: "Сб", 6: "Вс"}
    weekdays = []
    count = 0

    while count < 7:
        next_day = today + timedelta(days=1)

        if next_day.weekday() not in [5, 6]:
            weekdays.append([next_day.strftime(f"({day_names[next_day.weekday()]}) %d.%m"),
                             next_day.date().isoformat()])
            count += 1

        today = next_day

    return weekdays


# окно с отображением информации о консультациях
async def need_help(callback_query: types.CallbackQuery):
    if is_can_be_deleted(callback_query.message.date):
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


# показ психологов
async def psycho(callback_query: types.CallbackQuery):
    if is_can_be_deleted(callback_query.message.date):
        await callback_query.message.delete()

    con = get_data_base_object()

    with con:
        list_psy = list(con.execute(f"SELECT * FROM Psychologist"))

    code = int(callback_query.data[7:])
    but = InlineKeyboardMarkup(row_width=3)

    but.add(InlineKeyboardButton('🗒 Подробно о психологе', url=sites_about_psychologists[str(list_psy[code][0])]))
    but.row(InlineKeyboardButton('⬅️', callback_data='all_psy' + str((code - 1) % len(list_psy))),
            InlineKeyboardButton('👩 Выбрать',
                                 callback_data='psy_' + str(list_psy[code][0]) + '_' + str(code)),
            InlineKeyboardButton('➡️', callback_data='all_psy' + str((code + 1) % len(list_psy))))
    but.add(InlineKeyboardButton('➡️ Главное меню', callback_data='menu'))

    await callback_query.message.answer_photo(open('psy_photo//' + str(list_psy[code][0]) + '.jpg', "rb"),
                                              caption=(list_psy[code][1] + '\n\n' + list_psy[code][2] + '\n\n' +
                                                       list_psy[code][3]),
                                              reply_markup=but)


# выбор типа услуги психолога
async def choose_type(callback_query: types.CallbackQuery):
    if is_can_be_deleted(callback_query.message.date):
        await callback_query.message.delete()

    data = callback_query.data.split('_')
    psy_id = data[1]
    but = InlineKeyboardMarkup()
    but.add(InlineKeyboardButton('🧩 Диагностическая встреча', callback_data='diagnostic_' + psy_id))
    # but.add(InlineKeyboardButton('💖 Полноценная консультация', callback_data='makeConsultation_' + psy_id))
    but.add(InlineKeyboardButton('👩 Назад к психологам', callback_data='all_psy' + data[2]))

    await bot.send_message(callback_query.from_user.id,
                           'Пожалуйста, выберите тип консультации, на которую вы хотели бы записаться ❤️',
                           reply_markup=but)


# выбор дня недели для диагностической встречи
async def choose_day_for_diagnostic(callback_query: types.CallbackQuery):
    if is_can_be_deleted(callback_query.message.date):
        await callback_query.message.delete()

    psy_id = callback_query.data.split('_')[1]

    days_kb = InlineKeyboardMarkup()
    days = get_next_7_weekdays()
    for i in range(len(days)):
        days_kb.add(InlineKeyboardButton('🗓 ' + days[i][0], callback_data='create_tran_' + psy_id + '_0_' + days[i][1]))

    days_kb.add(InlineKeyboardButton('➡️ Вернуться в главное меню', callback_data='menu'))

    await bot.send_message(callback_query.from_user.id,
                           "Выберите день, в который вам было бы удобно провести диагностическую встречу с "
                           "психологом.\nЕсли у вас поменяются планы, то дату можно будет изменить, обговорив "
                           "с психологом.\nВремя консультации обговаривается лично с психологом.",
                           reply_markup=days_kb)


# выбор пакета консультаций
async def choose_tariff(callback_query: types.CallbackQuery):
    if is_can_be_deleted(callback_query.message.date):
        await callback_query.message.delete()

    psy_id = callback_query.data.split('_')[1]

    tariff_kb = InlineKeyboardMarkup()
    tariff_kb.add(InlineKeyboardButton('❤ 1 консультация - 1599 руб', callback_data='create_tran_' + psy_id + '_1'))
    tariff_kb.add(InlineKeyboardButton('❤ 3 консультации - 4499 руб', callback_data='create_tran_' + psy_id + '_3'))
    tariff_kb.add(InlineKeyboardButton('❤ 5 консультаций - 7199 руб', callback_data='create_tran_' + psy_id + '_5'))
    tariff_kb.add(InlineKeyboardButton('❤ 10 консультация - 13399 руб', callback_data='create_tran_' + psy_id + '_10'))
    tariff_kb.add(InlineKeyboardButton('➡️ Вернуться в главное меню', callback_data='menu'))

    await bot.send_message(callback_query.from_user.id,
                           "Выберите, пожалуйста, пакет консультаций, который вы хотите приобрести.",
                           reply_markup=tariff_kb)


# инициализация функций показа психологов, слотов и записи на консультации
def init_consultations_application(telegram_bot, dispatcher):
    global bot, dp

    bot = telegram_bot
    dp = dispatcher

    dp.callback_query_handler(lambda c: c.data and c.data.startswith('need_help'))(need_help)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('all_psy'))(psycho)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('psy_'))(choose_type)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('diagnostic_'))(choose_day_for_diagnostic)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('makeConsultation_'))(choose_tariff)


# with con:
#     psy_id = list(con.execute(f"SELECT psycho_id FROM Slot WHERE id={slot_id}"))[0][0]
#
# await bot.send_message(psy_id, "Пользователь " + str(callback_query.from_user.id) +
#                        " к вам на консультацию!\nБолее подробную информацию можно посмотреть в личном "
#                        "кабинете психолога)")
