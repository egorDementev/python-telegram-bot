from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data_provider import get_go_to_menu_kb, get_data_base_object, get_bot_token, get_psycho_kb

bot = Bot(token=get_bot_token())
dp = Dispatcher(bot)


# psycho меню
async def psycho_page(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, 'Кабинет психолога', reply_markup=get_psycho_kb())


# psycho add slots
async def add_slots(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, 'Отправить данные одним сообщением вида:')
    await bot.send_message(callback_query.from_user.id,
                           'slot/гггг-мм-дд xx:xx/гггг-мм-дд xx:xx/гггг-мм-дд xx:xx и так далее')
    await bot.send_message(callback_query.from_user.id,
                           'Если кнопка нажата по ошибке, то просто перейдите в главное меню',
                           reply_markup=get_go_to_menu_kb())


# psycho select slot that have to remove
async def select_slot_to_del(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    con = get_data_base_object()

    with con:
        lst_slot = list(con.execute(f"SELECT date, time, id FROM Slot WHERE "
                                    f"psycho_id={callback_query.from_user.id} and is_free={1}"))

    await bot.send_message(callback_query.from_user.id, "Ваши слоты, которые еще не заняты:", reply_markup=None)

    for x in lst_slot:
        btn = InlineKeyboardMarkup()
        btn.add(InlineKeyboardButton("Удалить слот", callback_data='rem_slot_' + str(x[2])))
        await bot.send_message(callback_query.from_user.id, str(x[0]) + " " + str(x[1]), reply_markup=btn)

    await bot.send_message(callback_query.from_user.id,
                           "Если кнопка нажата по ошибке, то просто перейдите в главное меню",
                           reply_markup=get_go_to_menu_kb())


# psycho del slot
async def del_slot(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    con = get_data_base_object()

    slot_id = callback_query.data.split('_')[-1]

    with con:
        con.execute(f"DELETE from Slot WHERE id={slot_id};")

    await bot.send_message(callback_query.from_user.id, "Слот успешно удален!", reply_markup=get_go_to_menu_kb())


# all consults (psy page)
async def psy_consults(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    con = get_data_base_object()

    await bot.send_message(callback_query.from_user.id, 'Ваши текущие консультации, на которые кто-то записался:',
                           reply_markup=None)

    with con:
        lst_of_cons = list(con.execute(f"SELECT id, slot_id, tran_id FROM Consultation WHERE is_done={0}"))

    with con:
        for i in lst_of_cons:
            if i[1] is not None:
                lst = list(con.execute(f"SELECT psycho_id, date, time FROM Slot WHERE id={i[1]}"))
                if lst[0][0] == callback_query.from_user.id:
                    btn = InlineKeyboardMarkup()
                    user_id = list(con.execute(f"SELECT user_id, is_diagnostic FROM Transactions WHERE id={i[2]}"))[0]
                    btn.add(InlineKeyboardButton('✅ Отметить консультацию, как проведенную',
                                                 callback_data='done_con_' + str(i[0])))
                    st = "Диагностическая" if int(user_id[1]) == 1 else "Консультация"
                    await bot.send_message(callback_query.from_user.id, str(user_id[0]) + '\n' + str(lst[0][1]) + ' ' +
                                           str(lst[0][2]) + "\n" + st, reply_markup=btn)

    await bot.send_message(callback_query.from_user.id, 'end', reply_markup=get_go_to_menu_kb())


# mark consultation as done
async def done_con(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    con = get_data_base_object()

    con_id = callback_query.data.split('_')[-1]

    with con:
        con.execute(f"UPDATE Consultation SET is_done={1} WHERE id={con_id}")

    await bot.send_message(callback_query.from_user.id, 'done', reply_markup=get_go_to_menu_kb())


# инициализация функций для психолога
def init_psycho_application(telegram_bot, dispatcher):
    global bot, dp

    bot = telegram_bot
    dp = dispatcher

    dp.callback_query_handler(lambda c: c.data and c.data.startswith('psycho'))(psycho_page)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('slot'))(add_slots)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('remove_slot'))(select_slot_to_del)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('rem_slot_'))(del_slot)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('my_consults'))(psy_consults)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('done_con'))(done_con)
