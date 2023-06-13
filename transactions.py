import datetime

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher

from data_provider import get_data_base_object, get_go_to_menu_kb, get_bot_token

bot = Bot(token=get_bot_token())
dp = Dispatcher(bot)


# create tran (or diagnostic consult)
async def create_tran(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    con = get_data_base_object()

    data = callback_query.data.split('_')
    slot_id = data[3]
    type_of_service = data[2]

    if int(type_of_service) == 0:
        print(callback_query.from_user.id)

        with con:
            con.execute(f"UPDATE Slot SET is_free='0' WHERE id='{slot_id}'")

        sql1, data1 = 'INSERT INTO Transactions (user_id, date, time, is_diagnostic) values(?, ?, ?, ?)', []
        data1.append((callback_query.from_user.id, str(datetime.datetime.now().date()),
                      str(datetime.datetime.now().time()), True))

        with con:
            con.executemany(sql1, data1)

        with con:
            print(list(con.execute(f"SELECT id FROM Transactions WHERE "
                                   f"user_id={callback_query.from_user.id} and is_diagnostic={1}")))
            tran_id = list(con.execute(f"SELECT id FROM Transactions WHERE "
                                       f"user_id={callback_query.from_user.id} and is_diagnostic={1}"))[0][0]

        sql1, data1 = 'INSERT INTO Consultation (tran_id, slot_id) values(?, ?)', []
        data1.append((tran_id, slot_id))

        with con:
            con.executemany(sql1, data1)

        with con:
            psy_id = list(con.execute(f"SELECT psycho_id FROM Slot WHERE id={slot_id}"))[0][0]

        await bot.send_message(psy_id, "Пользователь " + str(callback_query.from_user.id) +
                               " к вам на диагностическую встречу!\nБолее подробную информацию можно посмотреть "
                               "в личном кабинете психолога)")

        await bot.send_message(callback_query.from_user.id, 'Поздравляю, вы записаны на диагностическую '
                                                            'встречу ❤️\nВ личном кабинете вы можете посмотреть всю '
                                                            'информацию о своих консультациях!',
                               reply_markup=get_go_to_menu_kb())
    # else:
    #     if PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
    #         await bot.send_message(callback_query.from_user.id, MESSAGES['pre_buy_demo_alert'])
    #     price = 0
    #     if int(type_of_service) == 1:
    #         price = PRICE_1
    #     elif int(type_of_service) == 5:
    #         price = PRICE_5
    #     elif int(type_of_service) == 10:
    #         price = PRICE_10
    #     await bot.send_invoice(callback_query.from_user.id,
    #                            title=MESSAGES['tm_title'],
    #                            description=MESSAGES['tm_description'],
    #                            provider_token=PAYMENTS_PROVIDER_TOKEN,
    #                            currency='rub',
    #                            is_flexible=False,  # True если конечная цена зависит от способа доставки
    #                            prices=[price],
    #                            start_parameter='time-machine-example',
    #                            payload=str(slot_id) + '_' + str(type_of_service),
    #                            )
    #     await bot.send_message(callback_query.from_user.id,
    #                            'Если вы нажали кнопку по ошибке, или передумали платить, '
    #                            'то просто перейдите в главное меню и НИКОГДА НЕ ПЛАТИТЕ ПО ДАННОЙ КНОПКЕ '
    #                            '(когда решитесь на покупку, то выберите новый слот и у вас появится новая '
    #                            'форма оплаты)!!', reply_markup=get_go_to_menu_kb())


# async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
#     await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


# async def process_successful_payment(message: types.Message):
#     print('successful_payment:')
#     payment = message.successful_payment.to_python()
#     data = payment['invoice_payload'].split('_')
#     count = data[1]
#     slot_id = data[0]
#
#     print(data)
#
#     con = get_data_base_object()
#
#     with con:
#         con.execute(f"UPDATE Slot SET is_free='0' WHERE id='{slot_id}'")
#
#     sql1, data1 = 'INSERT INTO Transactions (user_id, date, time, is_diagnostic) values(?, ?, ?, ?)', []
#     data1.append((message.from_user.id, str(datetime.datetime.now().date()),
#                   str(datetime.datetime.now().time()), False))
#
#     with con:
#         con.executemany(sql1, data1)
#
#     with con:
#         tran_id = list(con.execute(f"SELECT id FROM Transactions WHERE "
#                                    f"user_id={message.from_user.id} and is_diagnostic={0}"))[0][0]
#
#
#     with con:
#         list_con = list(con.execute(f"SELECT tran_id, slot_id FROM Consultation WHERE is_done='0'"))
#
#     print(list_con)
#     is_free_slot = 0
#
#     for i in list_con:
#         if i[1] is None:
#             with con:
#                 lst = list(con.execute(f"SELECT user_id, id FROM Transactions WHERE id={i[0]}"))
#             if str(lst[0][0]) == str(message.from_user.id):
#                 with con:
#                     con.execute(f"UPDATE Slot SET is_free='0' WHERE id='{slot_id}'")
#                 with con:
#                     id_con = list(con.execute(f"SELECT id FROM Consultation WHERE tran_id={i[0]} and
#                     slot_id is null"))[0][0]
#                 with con:
#                     con.execute(f"UPDATE Consultation SET slot_id={slot_id} WHERE tran_id={i[0]} and id={id_con}")
#                 is_free_slot = 1
#         if is_free_slot == 1:
#             break
#
#     for i in range(int(count)):
#         if i == 0:
#             sql1, data1 = 'INSERT INTO Consultation (tran_id, slot_id) values(?, ?)', []
#             data1.append((tran_id, slot_id))
#         else:
#             sql1, data1 = 'INSERT INTO Consultation (tran_id, slot_id) values(?, ?)', []
#             data1.append((tran_id, None))
#
#         with con:
#             con.executemany(sql1, data1)
#     print(1)
#     with con:
#         psy_id = list(con.execute(f"SELECT psycho_id FROM Slot WHERE id={slot_id}"))[0][0]
#
#     await bot.send_message(psy_id, "Пользователь " + str(message.from_user.id) +
#                            " к вам на консультацию!\nБолее подробную информацию можно посмотреть в личном "
#                            "кабинете психолога)")
#
#     await bot.send_message(message.from_user.id, 'Поздравляю, вы записаны на консультацию! ❤️\n'
#                                                         'В личном кабинете вы можете посмотреть всю '
#                                                         'информацию о своих консультациях!',
#                            reply_markup=go_to_menu)


# инициализация функций создания транзакции и оплаты
def init_transactions_application(telegram_bot, dispatcher):
    global bot, dp

    bot = telegram_bot
    dp = dispatcher

    dp.callback_query_handler(lambda c: c.data and c.data.startswith('create_tran_'))(create_tran)
    # dp.pre_checkout_query_handler(lambda query: True)(process_pre_checkout_query)
    # dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)(process_successful_payment)
