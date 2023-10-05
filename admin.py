from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data_provider import get_admin_kb, get_data_base_object, get_go_to_menu_kb, get_admin_list, get_bot_token, \
    is_can_be_deleted

bot = Bot(token=get_bot_token())
dp = Dispatcher(bot)


# admin меню
async def admin_page(callback_query: types.CallbackQuery):
    if is_can_be_deleted(callback_query.message.date):
        await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, 'Кабинет администратора', reply_markup=get_admin_kb())


# admin show psycho
async def show_psycho(callback_query: types.CallbackQuery):
    if is_can_be_deleted(callback_query.message.date):
        await callback_query.message.delete()

    con = get_data_base_object()

    with con:
        lst = list(con.execute(f"SELECT id, name FROM Psychologist"))

    for x in lst:
        btn = InlineKeyboardMarkup()
        btn.add(InlineKeyboardButton('Показать проведенные консультации', callback_data='show_consult_' + str(x[0])))
        await bot.send_message(callback_query.from_user.id, str(x[1]), reply_markup=btn)

    await bot.send_message(callback_query.from_user.id, "go back", reply_markup=get_go_to_menu_kb())


# admin show psycho consultations
async def show_psycho_consultations(callback_query: types.CallbackQuery):
    if is_can_be_deleted(callback_query.message.date):
        await callback_query.message.delete()

    psy_id = callback_query.data.split('_')[-1]
    con = get_data_base_object()

    with con:
        lst = list(con.execute(f"SELECT slot_id FROM Consultation WHERE is_done='1'"))

    st = "Проведенные консультации:\n"
    for x in lst:
        with con:
            data = list(con.execute(f"SELECT date, time FROM Slot WHERE psycho_id={psy_id} and id={x[0]}"))
        if data[0][0] is not None:
            st += str(data[0][0]) + " " + str(data[0][1]) + "\n"

    await bot.send_message(callback_query.from_user.id, st, reply_markup=get_go_to_menu_kb())


# admin add psychologist
async def admin_add_psycho(callback_query: types.CallbackQuery):
    if is_can_be_deleted(callback_query.message.date):
        await callback_query.message.delete()

    await bot.send_message(callback_query.from_user.id, 'Отправить данные одним сообщением вида:')
    await bot.send_message(callback_query.from_user.id,
                           'add/<telegram id>/<ФИО>/'
                           '<О психологе>\nПосле этого необходимо отправить фото просто в бота, программа сама '
                           'добавит его в профиль психолога')
    await bot.send_message(callback_query.from_user.id,
                           'Если кнопка нажата по ошибке, то просто перейдите в главное меню',
                           reply_markup=get_go_to_menu_kb())


# admin del psychologist
async def admin_del_psycho(callback_query: types.CallbackQuery):
    if is_can_be_deleted(callback_query.message.date):
        await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, 'Отправить данные одним сообщением вида:')
    await bot.send_message(callback_query.from_user.id, 'del/<telegram id>')
    await bot.send_message(callback_query.from_user.id,
                           'Если кнопка нажата по ошибке, то просто перейдите в главное меню',
                           reply_markup=get_go_to_menu_kb())


# admin рассылка
async def admin_sender(callback_query: types.CallbackQuery):
    if is_can_be_deleted(callback_query.message.date):
        await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, 'Чтобы отправить сообщение всем пользователям, '
                                                        'напишите: all/текст сообщения')
    await bot.send_message(callback_query.from_user.id,
                           'Если кнопка нажата по ошибке, то просто перейдите в главное меню',
                           reply_markup=get_go_to_menu_kb())


# обработка фото-сообщений (установка фото психолога)
async def get_photo(message: types.Message):
    if str(message.from_user.id) in get_admin_list():
        con = get_data_base_object()

        with con:
            psy_id = list(con.execute(f"SELECT id FROM Psychologist WHERE photo='нет фото';"))

        if psy_id:
            await message.photo[-1].download(destination_file='psy_photo//' + str(psy_id[0][0]) + '.jpg')

            with con:
                con.execute(f"UPDATE Psychologist SET photo='фото' WHERE id='{psy_id[0][0]}';")

            await bot.send_message(message.from_user.id, 'photo set', reply_markup=get_go_to_menu_kb())
        else:
            await bot.send_message(message.from_user.id, 'Нет психологов без фото', reply_markup=get_go_to_menu_kb())
    else:
        await bot.send_message(message.from_user.id, 'Некорректный ввод данных')


# инициализация функций админской части приложения
def init_admin_application(telegram_bot, dispatcher):
    global bot, dp

    bot = telegram_bot
    dp = dispatcher

    dp.callback_query_handler(lambda c: c.data and c.data.startswith('admin'))(admin_page)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('show_psycho'))(show_psycho)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('show_consult_'))(show_psycho_consultations)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('add'))(admin_add_psycho)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('del'))(admin_del_psycho)
    dp.callback_query_handler(lambda c: c.data and c.data.startswith('send_to_all'))(admin_sender)
    dp.message_handler(content_types=['photo'])(get_photo)
