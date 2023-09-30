from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.work_with_db import if_register, add_new_person
from data_provider import get_contract_kb, get_start_kb, get_go_to_menu_kb, get_bot_token, get_super_admin_id
from datetime import datetime
from start_application import write_log_to_file

bot = Bot(token=get_bot_token())
dp = Dispatcher(bot)


# метод отправляет сообщение с документом - договором
async def send_contract_message(cq, kb):
    await bot.send_document(cq.from_user.id, open("resources/documents/contract.docx", "rb"),
                            caption="Подтвердите, что вы ознакомились с договором(оферта на оказание агентских Услуг)"
                                    " и принимаете его условия",
                            reply_markup=kb)


# метод отправляет сообщение с документом - согласием на обработку персональных данных
async def send_agreement_message(cq, kb):
    await bot.send_document(cq.from_user.id, open("resources/documents/personal_data.docx", "rb"),
                            caption="Подтвердите, что вы соглашаетесь на обработку персональных данных",
                            reply_markup=kb)


# метод отправляет новым пользователям договор и согласие на обработку персональных данных
async def attach(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    data = callback_query.data.split('_')

    if int(data[1]) == int(data[2]) == 0:
        await bot.send_message(callback_query.from_user.id, "Так как в ближайшее время именно через этого бота будет "
                                                            "производиться услуга подбора психолога, то, чтобы "
                                                            "обезопасить себя и нас, ознакомьтесь, пожалуйста, со "
                                                            "следующими документами!!\nДля продолжения работы с ботом "
                                                            "вам нужно подтвердить, что вы ознакомились с договором, "
                                                            "а так же принимаете соглашение на обработку персональных "
                                                            "данных.")
        await send_contract_message(callback_query, InlineKeyboardMarkup().add(get_contract_kb()[0]))

    elif int(data[1]) == 1 and int(data[2]) == 0:
        await send_contract_message(callback_query, InlineKeyboardMarkup().add(get_contract_kb()[1]))
        await send_agreement_message(callback_query, InlineKeyboardMarkup().add(get_contract_kb()[2]))

    elif int(data[1]) == 1 and int(data[2]) == 1:
        await send_agreement_message(callback_query, InlineKeyboardMarkup().add(get_contract_kb()[3]))
        await bot.send_message(callback_query.from_user.id, "Отлично, теперь можем продолжить!",
                               reply_markup=get_start_kb())

        log_text = f"LOG: accept [{datetime.now().isoformat()}] " \
                   f"UserID={callback_query.from_user.id} " \
                   f"UserURL={f'https://t.me/{callback_query.from_user.username if callback_query.from_user.username else None}'}"

        await bot.send_message(get_super_admin_id(), log_text, reply_markup=None)
        await write_log_to_file('logs.txt', log_text)


# регистрация пользователя, если его еще нет в базе данных
async def start_bot(callback_query: types.CallbackQuery):

    await callback_query.message.delete()
    if if_register(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, 'Вы уже зарегистрированы в боте ❤️',
                               reply_markup=get_go_to_menu_kb())
    else:
        add_new_person(
            callback_query.from_user.id,
            f"https://t.me/"
            f"{callback_query.from_user.username if callback_query.from_user.username else 'нет имени пользователя'}")

        await bot.send_message(callback_query.from_user.id, 'Спасибо, что доверился(лась) нам ❤',
                               reply_markup=None)
        media = types.MediaGroup()
        media.attach_photo(types.InputFile('resources/pictures/check_up.png'))

        await bot.send_media_group(callback_query.from_user.id, media=media)
        await bot.send_message(callback_query.from_user.id, 'В нашем боте ты можешь ежедневно устраивать рефлексию и '
                                                            'отмечать свое состояние по нескольким критериям 🎉\n'
                                                            'Для твоего удобства, по каждому критерию '
                                                            'будет построен график состояния за неделю. Так, ты '
                                                            'сможешь наглядно проследить, в какой области чаще всего '
                                                            'возникают трудности, а также, если будет желание, сможешь '
                                                            'показать графики психологу.\nP.S. Эта информация '
                                                            'полностью конфиденциальна и '
                                                            'не будет передана третьим лицам.', reply_markup=None)

        media = types.MediaGroup()
        media.attach_photo(types.InputFile('resources/pictures/example.png'),
                           '📈 Пример графика настроения за неделю')

        await bot.send_media_group(callback_query.from_user.id, media=media)

        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton('🔜 Продолжить', callback_data='subscribe'))
        await bot.send_message(callback_query.from_user.id, 'Давай продолжим регистрацию!',
                               reply_markup=kb)


async def subscribe(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    message = 'Для дальнейшей работы с нашим ботом, тебе нужно подписаться на наш телеграм канал, в котором мы ' \
              'регулярно публикуем:\n🔹 ответы психологов на ваши вопросы\n🔹 советы по "выживанию" для студентов\n🔹 ' \
              'поднимаем много актуальных тем, которые многим из вас откликнутся'

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton('🔔 Подписаться на канал', url='https://t.me/connectionBotChannel'))
    kb.add(InlineKeyboardButton('✅ Проверить подписку', callback_data='s_check'))

    await callback_query.message.answer_photo(open('resources/pictures/tg.png', "rb"), caption=message,
                                              reply_markup=kb)


async def check_subscribe(callback_query: types.CallbackQuery):

    user_channel_status = await bot.get_chat_member(chat_id=-1001737343585,
                                                    user_id=callback_query.from_user.id)
    if user_channel_status["status"] != 'left':
        await successful_subscribe(callback_query)
    else:
        await bot.send_message(callback_query.from_user.id, "Похоже, что вы не подписаны на канал...\nПодпишитесь, "
                                                            "и повторите попытку еще раз ❤️")


async def successful_subscribe(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    await bot.send_message(callback_query.from_user.id, 'Спасибо ❤️\nТеперь можешь переходить в главное меню!',
                           reply_markup=get_go_to_menu_kb())

    log_text = f"LOG: registered [{datetime.now().isoformat()}] " \
               f"UserID={callback_query.from_user.id} " \
               f"UserURL={f'https://t.me/{callback_query.from_user.username if callback_query.from_user.username else None}'}"

    await bot.send_message(get_super_admin_id(), log_text, reply_markup=None)
    await write_log_to_file('logs.txt', log_text)


def init_registration(telegram_bot, dispatcher):
    global bot, dp

    bot = telegram_bot
    dp = dispatcher

    dp.callback_query_handler(lambda c: c.data and c.data.startswith('attach'))(attach)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('run'))(start_bot)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('subscribe'))(subscribe)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('s_check'))(check_subscribe)

