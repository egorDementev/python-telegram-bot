from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import os
# import asyncio
# import aioschedule
import sqlite3 as sl
import work_with_db
import draw
import datetime

con = sl.connect('db//connection.db')

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

'''КЛИЕНТСКАЯ ЧАСТЬ'''
num = 0
# кнопка начать
get_attach_kb = InlineKeyboardMarkup().add(InlineKeyboardButton('➡️  Продолжить', callback_data='attach_0_0'))

contract_btn = [InlineKeyboardButton("✖️ Я прочитал и принимаю условия договора", callback_data='attach_1_0'),
                InlineKeyboardButton("✅ Я прочитал и принимаю условия договора", callback_data='nope'),
                InlineKeyboardButton("✖️ Я подтверждаю согласие на обработку персональных данных",
                                     callback_data='attach_1_1'),
                InlineKeyboardButton("✅ Я подтверждаю согласие на обработку персональных данных", callback_data='nope')]

start_button = InlineKeyboardMarkup().add(InlineKeyboardButton('🚀 Начать', callback_data='run'))

# кнопка перехода в меню
go_to_menu = InlineKeyboardMarkup().add(InlineKeyboardButton('➡️ Главное меню', callback_data='menu'))

# лист с кнопками основного меню
list_main_btn = [InlineKeyboardButton('👤 Мой кабинет', callback_data='user_account'),
                 InlineKeyboardButton('📅 Моё состояние', callback_data='my_feeling'),
                 InlineKeyboardButton('🙋‍♀️Обратиться к психологу', callback_data='need_help'),
                 InlineKeyboardButton('⚙️ Техподдержка', callback_data='support'),
                 InlineKeyboardButton('⚙️ Кабинет психолога', callback_data='psycho'),
                 InlineKeyboardButton('⚙️ Кабинет администратора', callback_data='admin')]

# admin kb
admin_kb = InlineKeyboardMarkup(row_width=1)
admin_kb.add(InlineKeyboardButton('⚙️ Показать психологов', callback_data='show_psycho'))
admin_kb.add(InlineKeyboardButton('⚙️ Добавить психолога в команду', callback_data='add'))
admin_kb.add(InlineKeyboardButton('⚙️ Удалить психолога из команды', callback_data='del_psy'))
admin_kb.add(InlineKeyboardButton('⚙️ Сделать рассылку', callback_data='alll'))
admin_kb.add(InlineKeyboardButton('➡️ Главное меню', callback_data='menu'))

# psychologist kb
psycho_kb = InlineKeyboardMarkup(row_width=1)
psycho_kb.add(InlineKeyboardButton('⚙️ Текущие консультации', callback_data='my_consults'))
psycho_kb.add(InlineKeyboardButton('⚙️ Добавить слоты на неделю', callback_data='slot'))
psycho_kb.add(InlineKeyboardButton('⚙️ Удалить слот', callback_data='remove_slot'))

support_kb = InlineKeyboardMarkup(row_width=1)
support_kb.add(InlineKeyboardButton("👤 По вопросам работы психологов", callback_data='sup_psy'))
support_kb.add(InlineKeyboardButton("🤖 По вопросам работы бота", callback_data='sup_bot'))
support_kb.add(InlineKeyboardButton('➡️ Главное меню', callback_data='menu'))

user_acc_kb = InlineKeyboardMarkup(row_width=1)
user_acc_kb.add(InlineKeyboardButton('💌 Связаться с психологом', callback_data='text_to_psy'))
user_acc_kb.add(InlineKeyboardButton('➡️ Главное меню', callback_data='menu'))

# TODO: подписать выбор из спика нескольких
# TODO: смайлик средний поменять, в одиночестве подписать сегодня, реверс графиков, убрать сохранение картинок

# клавиатура с выбором проблемы для дальнейшего консультирования
all_user_problems = InlineKeyboardMarkup()
all_user_problems.add(InlineKeyboardButton('👩 Посмотреть психологов', callback_data='all_psy0'))
all_user_problems.add(InlineKeyboardButton('➡️ Главное меню', callback_data='menu'))

# инлайн кнопки в двух вариантах: нажата или нет
list_prob_btn = [InlineKeyboardButton('Неуверенность в себе', callback_data='btn1'),
                 InlineKeyboardButton('Прокрастинация', callback_data='btn2'),
                 InlineKeyboardButton('Тревожность', callback_data='btn3'),
                 InlineKeyboardButton('Одиночество', callback_data='btn4'),
                 InlineKeyboardButton('Осуждение себя', callback_data='btn5'),
                 InlineKeyboardButton('✅ Неуверенность в себе', callback_data='btn6'),
                 InlineKeyboardButton('✅ Прокрастинация', callback_data='btn7'),
                 InlineKeyboardButton('✅ Тревожность', callback_data='btn8'),
                 InlineKeyboardButton('✅ Одиночество', callback_data='btn9'),
                 InlineKeyboardButton('✅ Осуждение себя', callback_data='btn10'),
                 InlineKeyboardButton('Дальше ➡️', callback_data='btn11')]

# лист с номерами кнопок, которые надо вывести на экран
# list_inline_btn = [0, 1, 2, 3, 4]
kb_my_prob = InlineKeyboardMarkup()
# for i in list_inline_btn:
#     kb_my_prob.add(list_prob_btn[i])

# строка, где будут храниться данные об оценке человеком своего состояния
st_condition = ''

# кнопки с выбором оценки своего состояния
kb_check = InlineKeyboardMarkup().add(InlineKeyboardButton('🤗', callback_data='con4'),
                                      InlineKeyboardButton('😄', callback_data='con3'),
                                      InlineKeyboardButton('😐', callback_data='con2'),
                                      InlineKeyboardButton('☹️', callback_data='con1'),
                                      InlineKeyboardButton('😭', callback_data='con0'),
                                      InlineKeyboardButton('⛔ Стоп', callback_data='stop'))

check_up_btn = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('🗸 Отследить состояние',
                                                                          callback_data='chk1'),
                                                     InlineKeyboardButton('📈 Посмотреть мои графики',
                                                                          callback_data='chk2'),
                                                     InlineKeyboardButton('➡️ Главное меню', callback_data='menu'))

# лист вопросов для оценки своего состояния
list_q = ['Оцени свой уровень тревожности сегодня:\n🤗 - совсем не было повода переживать\n😭 - сильно переживаю '
          'из-за чего-то',
          'Много времени ушло на прокрастинацию сегодня?\n🤗 - совсем не прокрастинировал(а)\n😭 - очень много времени '
          'было потрачено впустую',
          'Испытавал(а) ли чувство одиночества?\n🤗 - совсем не было такого чувства\n😭 - сильно переживал(а) по '
          'этому поводу',
          'Оцени уровень неуверенности в себе сегодня:\n🤗 - чувствовал(а) себя на все 100% уверенно\n😭 - ощущал(а) '
          'себя очень неуверенно',
          'Оцени уровень осуждения себя сегодня:\n🤗 - совсем не осуждал(а) себя\n😭 - сегодня мне было очень тяжело']


# самое первое сообщение при старте бота
@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Привет, мы очень рады видеть тебя в нашем боте! Давай пройдем короткую регистрацию, '
                           'после чего ты сможешь полноценно пользоваться услугами нашего бота ❤️',
                           reply_markup=get_attach_kb)


# get attachments
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('attach'))
async def attach(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    data = callback_query.data.split('_')
    kb = InlineKeyboardMarkup()
    if int(data[1]) == 0 and int(data[2]) == 0:
        kb.add(contract_btn[0])
        await bot.send_document(callback_query.from_user.id, open("contract.docx", "rb"),
                                caption="Подтвердите, что вы ознакомились с договором и принимаете его условия",
                                reply_markup=kb)
    if int(data[1]) == 1 and int(data[2]) == 0:
        kb.add(contract_btn[1])
        await bot.send_document(callback_query.from_user.id, open("contract.docx", "rb"),
                                caption="Подтвердите, что вы ознакомились с договором и принимаете его условия",
                                reply_markup=kb)

        kb = InlineKeyboardMarkup()
        kb.add(contract_btn[2])
        await bot.send_document(callback_query.from_user.id, open("personal_data.docx", "rb"),
                                caption="Подтвердите, что вы соглашаетесь на обработку персональных данных",
                                reply_markup=kb)
    if int(data[1]) == 1 and int(data[2]) == 1:
        kb.add(contract_btn[3])
        await bot.send_document(callback_query.from_user.id, open("personal_data.docx", "rb"),
                                caption="Подтвердите, что вы соглашаетесь на обработку персональных данных",
                                reply_markup=kb)
        await bot.send_message(callback_query.from_user.id, "Отлично, теперь можем продолжить!", reply_markup=start_button)


# регистрация пользователя, если его еще нет в базе данных
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('run'))
async def start_bot(callback_query: types.CallbackQuery):
    global kb_my_prob, con

    await callback_query.message.delete()
    if work_with_db.if_register(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, 'Вы уже зарегистрированы в боте ❤️',
                               reply_markup=go_to_menu)
    else:
        work_with_db.add_new_person(callback_query.from_user.id, '0 1 2 3 4')

        with con:
            list_user_prob = list(con.execute(f"SELECT problems FROM Person WHERE id={callback_query.from_user.id}"))[0][0].split()
            list_user_prob = [int(x) for x in list_user_prob]

        kb_my_prob = InlineKeyboardMarkup()
        for i in list_user_prob:
            kb_my_prob.add(list_prob_btn[i])
        await bot.send_message(callback_query.from_user.id, 'Для начала нам нужно понять, с какими сложностями ты '
                                                            'сталкиваешься, чтобы подобрать для тебя психологов, '
                                                            'которые точно смогут тебе помочь!\nВыбери из списка наиболее '
                                                            'актуальные для тебя трудности.\n'
                                                            'P.S. Эта информация полностью конфиденциальна и '
                                                            'не будет передана третьим лицам.', reply_markup=kb_my_prob)


# главное меню
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('menu'))
async def home_page(callback_query: types.CallbackQuery):
    global num, list_main_btn, con
    num = 0
    await callback_query.message.delete()
    main_menu = InlineKeyboardMarkup(row_width=1)
    if str(callback_query.from_user.id) == '596752948':
        main_menu.add(list_main_btn[-1])

    with con:
        psycho_list = [str(x[0]) for x in list(con.execute(f"SELECT id FROM Psychologist;"))]

    if str(callback_query.from_user.id) in psycho_list:
        main_menu.add(list_main_btn[-2])

    for x in range(len(list_main_btn) - 2):
        main_menu.add(list_main_btn[x])
    await callback_query.message.answer_photo(open("logo.png", "rb"), caption='Привет 👋\nВыбери одну из функций:',
                                              reply_markup=main_menu)


# admin меню
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('admin'))
async def admin_page(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, 'Кабинет администратора', reply_markup=admin_kb)


# admin show psycho
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('show_psycho'))
async def show_psycho(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    global con

    with con:
        lst = list(con.execute(f"SELECT id, name FROM Psychologist"))

    for x in lst:
        btn = InlineKeyboardMarkup()
        btn.add(InlineKeyboardButton('Показать проведенные консультации', callback_data='show_consult_' + str(x[0])))
        await bot.send_message(callback_query.from_user.id, str(x[1]), reply_markup=btn)
    await bot.send_message(callback_query.from_user.id, "go back", reply_markup=go_to_menu)


# admin show psycho consultations
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('show_consult_'))
async def show_psycho_consultations(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    global con

    psy_id = callback_query.data.split('_')[-1]

    with con:
        lst = list(con.execute(f"SELECT slot_id FROM Consultation WHERE is_done='1'"))

    st = "Проведенные консультации:\n"
    for x in lst:
        with con:
            data = list(con.execute(f"SELECT date, time FROM Slot WHERE psycho_id={psy_id} and id={x[0]}"))
            print(data)
        if data[0][0] is not None:
            st += str(data[0][0]) + " " + str(data[0][1]) + "\n"
    await bot.send_message(callback_query.from_user.id, st, reply_markup=go_to_menu)


# admin add psychologist
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('add'))
async def admin_add_psycho(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, 'Отправить данные одним сообщением вида:')
    await bot.send_message(callback_query.from_user.id,
                           'add/<telegram id>/<ФИО>/<Список проблем, с которыми работает психолог(через запятую)>/'
                           '<О псилогоге>\nПосле этого необходимо отправить фото просто в бота, программа сама '
                           'добавит его в профиль психолога')
    await bot.send_message(callback_query.from_user.id,
                           'Если кнопка нажата по ошибке, то просто перейдите в главное меню', reply_markup=go_to_menu)


# admin del psychologist
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('del'))
async def admin_add_psycho(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, 'Отправить данные одним сообщением вида:')
    await bot.send_message(callback_query.from_user.id, 'del/<telegram id>')
    await bot.send_message(callback_query.from_user.id,
                           'Если кнопка нажата по ошибке, то просто перейдите в главное меню', reply_markup=go_to_menu)


# admin рассылка
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('alll'))
async def admin_add_psycho(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, 'Чтобы отправить сообщние всем пользователям, '
                                                        'напишите: all/текст сообщения')
    await bot.send_message(callback_query.from_user.id,
                           'Если кнопка нажата по ошибке, то просто перейдите в главное меню', reply_markup=go_to_menu)


# psycho меню
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('psycho'))
async def psycho_page(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, 'Кабинет психолога', reply_markup=psycho_kb)


# psycho add slots
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('slot'))
async def psycho_page(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, 'Отправить данные одним сообщением вида:')
    await bot.send_message(callback_query.from_user.id,
                           'slot/гггг-мм-дд xx:xx/гггг-мм-дд xx:xx/гггг-мм-дд xx:xx и так далее')
    await bot.send_message(callback_query.from_user.id,
                           'Если кнопка нажата по ошибке, то просто перейдите в главное меню', reply_markup=go_to_menu)


# psycho select slot that have to remove
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('remove_slot'))
async def del_slot(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    global con

    with con:
        lst_slot = list(con.execute(f"SELECT date, time, id FROM Slot WHERE "
                                    f"psycho_id={callback_query.from_user.id} and is_free={1}"))

    await bot.send_message(callback_query.from_user.id, "Ваши слоты, которые еще не заняты:", reply_markup=None)

    for x in lst_slot:
        btn = InlineKeyboardMarkup()
        btn.add(InlineKeyboardButton("Удалить слот", callback_data='rem_slot_' + str(x[2])))
        await bot.send_message(callback_query.from_user.id, str(x[0]) + " " + str(x[1]), reply_markup=btn)

    await bot.send_message(callback_query.from_user.id,
                           "Если кнопка нажата по ошибке, то просто перейдите в главное меню", reply_markup=go_to_menu)


# psycho del slot
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('rem_slot_'))
async def del_slot(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    global con

    slot_id = callback_query.data.split('_')[-1]

    with con:
        con.execute(f"DELETE from Slot WHERE id={slot_id};")

    await bot.send_message(callback_query.from_user.id, "Слот успешно удален!", reply_markup=go_to_menu)


# support
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('support'))
async def support(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    await callback_query.message.answer_photo(open("support.png", "rb"),
                                              caption="Пожалуйста, выберите тему обращения ❤", reply_markup=support_kb)


# support bot
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('sup_bot'))
async def sup_bot(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    await callback_query.message.answer_photo(open("support.png", "rb"),
                                              caption="Опишите свой вопрос максимально подробно!\nОтправьте "
                                                      "сообщение вида:\nsup_bot/<ваш вопрос>\nВ противном случае, "
                                                      "наша команда не сможет его увидеть...", reply_markup=go_to_menu)


# support psy
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('sup_psy'))
async def sup_psy(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    await callback_query.message.answer_photo(open("support.png", "rb"),
                                              caption="Опишите свой вопрос максимально подробно!\nОтправьте "
                                                      "сообщение вида:\nsup_psy/<ваш вопрос>\nВ противном случае, "
                                                      "наша команда не сможет его увидеть...", reply_markup=go_to_menu)


# меню с кнопками про чек-ап
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('my_feeling'))
async def my_feeling(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer_photo(open("check_up.png", "rb"), caption='Давай вспомним, как прошел '
                                                                                  'твой день ❤️',
                                              reply_markup=check_up_btn)


# кнопки с выбором проблем для обращения к психологу
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('need_help'))
async def need_help(callback_query: types.CallbackQuery):
    global con
    await callback_query.message.delete()

    list_problems = list(con.execute(f"SELECT problems FROM Person WHERE id='{callback_query.from_user.id}'"))[0][
        0].split()
    print(list_problems)
    # for problem in list_problems:
    #     if int(problem) == 5:
    #         all_user_problems.add(InlineKeyboardButton('Неуверенность в себе', callback_data='prob0'))
    #     elif int(problem) == 6:
    #         all_user_problems.add(InlineKeyboardButton('Прокрастинация', callback_data='prob1'))
    #     elif int(problem) == 7:
    #         all_user_problems.add(InlineKeyboardButton('Тревожность', callback_data='prob2'))
    #     elif int(problem) == 8:
    #         all_user_problems.add(InlineKeyboardButton('Одиночество', callback_data='prob3'))
    #     elif int(problem) == 9:
    #         all_user_problems.add(InlineKeyboardButton('Осуждение себя', callback_data='prob4'))

    await callback_query.message.answer_photo(open("psy.png", "rb"),
                                              caption='Наша миссия - сделать тебя с'
                                                      'частливее ❤️\n\nУ нас ты можешь посетить бесплатную '
                                                      'диагностическую встречу с психологом, чтобы познакомиться, '
                                                      'сформировать запрос, '
                                                      'наметить план дольшейший действий!\nЭто поможет тебе выбрать '
                                                      'того психолога, который '
                                                      'будет тебе по душе 😊\n\nКонсультация с психологом 60 минут - '
                                                      '1199 рублей\nМы делаем '
                                                      'все возможное, чтобы занятия '
                                                      'с психологами стали максимально доступными для тебя!\n\n'
                                                      'Чтобы увидеть всех психологов, нажми на кнопку '
                                                      '"Хочу посмотреть всех психологов"',
                                              reply_markup=all_user_problems)


# функция остановки чек-апа, если пользователь передумал
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('stop'))
async def stop_check_up(callback_query: types.CallbackQuery):
    global st_condition
    await callback_query.message.delete()
    st_condition = ''
    await bot.send_message(callback_query.from_user.id,
                           'Процесс отслеживания состояния прерван, результаты не будут сохранены.\n'
                           'Не забудьте вернуться сюда сегодня и отметить свое состояние ❤', reply_markup=go_to_menu)


# функция, которая отвечает за регистрацию
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn'))
async def register(callback_query: types.CallbackQuery):
    global list_prob_btn, kb_my_prob, con

    with con:
        list_inline_btn = list(con.execute(f"SELECT problems FROM Person WHERE id={callback_query.from_user.id}"))[0][0].split()
        list_inline_btn = [int(x) for x in list_inline_btn]

    code = callback_query.data[3:]
    if code.isdigit():
        code = int(code)
    if code <= 5:
        # если пользователь нажал на кнопку с проблемой, которая не была выбрана раньше, то изменяем клавиатуру
        await callback_query.message.edit_reply_markup(reply_markup=None)
        kb_my_prob = InlineKeyboardMarkup()
        for pr in range(len(list_inline_btn)):
            if code - 1 == list_inline_btn[pr]:
                list_inline_btn[pr] += 5
            kb_my_prob.add(list_prob_btn[list_inline_btn[pr]])
        if len(list_inline_btn) == 5:
            kb_my_prob.add(list_prob_btn[-1])
            list_inline_btn.append(10)

        with con:
            con.execute(f"UPDATE Person SET problems='{' '.join([str(x) for x in list_inline_btn])}' WHERE id='{callback_query.from_user.id}';")

        await callback_query.message.edit_reply_markup(reply_markup=kb_my_prob)
    elif 6 <= code <= 10:
        await callback_query.message.edit_reply_markup(reply_markup=None)
        kb_my_prob = InlineKeyboardMarkup()
        for pr in range(len(list_inline_btn)):
            if code - 1 == list_inline_btn[pr]:
                list_inline_btn[pr] -= 5
        if list_inline_btn[0] < 5 and list_inline_btn[1] < 5 and list_inline_btn[2] < 5 and list_inline_btn[3] < 5 \
                and list_inline_btn[4] < 5:
            del list_inline_btn[-1]
        for pr in range(len(list_inline_btn)):
            kb_my_prob.add(list_prob_btn[list_inline_btn[pr]])

        with con:
            con.execute(f"UPDATE Person SET problems='{' '.join([str(x) for x in list_inline_btn])}' "
                        f"WHERE id='{callback_query.from_user.id}';")

        await callback_query.message.edit_reply_markup(reply_markup=kb_my_prob)
    elif code == 11:
        await callback_query.message.delete()
        await bot.send_message(callback_query.from_user.id, 'Спасибо, что поделился(лась) своими переживаниями ❤',
                               reply_markup=None)
        media = types.MediaGroup()
        media.attach_photo(types.InputFile('check_up.png'))
        await bot.send_media_group(callback_query.from_user.id, media=media)
        await bot.send_message(callback_query.from_user.id, 'У нас ты можешь ежедневно отмечать свое эмоциональное '
                                                            'состояние 🎉\nДля твоего удобства, по каждому критерию '
                                                            'будет построен график состояния за неделю. Так, ты '
                                                            'сможешь наглядно проследить, в какой области чаще всего '
                                                            'возникают трудности, а также если будет желание, сможешь '
                                                            'показать графики психологу.\nP.S. Эта информация '
                                                            'полностью конфиденциальна и '
                                                            'не будет передана третьим лицам.', reply_markup=None)
        media = types.MediaGroup()
        media.attach_photo(types.InputFile('example.png'), '📈 Пример графика настроения за каждый день нелели')
        await bot.send_media_group(callback_query.from_user.id, media=media)

        with con:
            con.execute(f"UPDATE Person SET problems='{' '.join([str(x) for x in list_inline_btn[:-1]])}' "
                        f"WHERE id='{callback_query.from_user.id}';")

        await bot.send_message(callback_query.from_user.id, 'Теперь переходи в главное меню', reply_markup=go_to_menu)


# функция, которая отвечает за сбор данных о состоянии пользователя
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('con'))
async def process_check_up(callback_query: types.CallbackQuery):
    global st_condition
    global list_q
    await callback_query.message.delete()
    code = callback_query.data[3:]
    if code.isdigit():
        code = int(code)
    st_condition += str(code) + ' '
    if len(st_condition) < 12:
        await bot.send_message(callback_query.from_user.id, list_q[len(st_condition) // 2 - 1], reply_markup=kb_check)
    else:
        work_with_db.check_up(callback_query.from_user.id, st_condition)
        draw.create_graphs(callback_query.from_user.id)
        media = types.MediaGroup()
        media.attach_photo(types.InputFile('check_up.png'))
        await bot.send_media_group(callback_query.from_user.id, media=media)
        media = types.MediaGroup()
        media.attach_photo(types.InputFile('files//' + str(callback_query.from_user.id) + "_mood.png"),
                           caption='📈 На сегодняшний день графики вашего состояния выглядят так:')
        media.attach_photo(types.InputFile('files//' + str(callback_query.from_user.id) + "_anxiety.png"))
        media.attach_photo(types.InputFile('files//' + str(callback_query.from_user.id) + "_procrastination.png"))
        media.attach_photo(types.InputFile('files//' + str(callback_query.from_user.id) + "_loneliness.png"))
        media.attach_photo(types.InputFile('files//' + str(callback_query.from_user.id) + "_doubt.png"))
        media.attach_photo(types.InputFile('files//' + str(callback_query.from_user.id) + "_condemning.png"))
        await bot.send_media_group(callback_query.from_user.id, media=media)
        await bot.send_message(callback_query.from_user.id,
                               'С заботой, твой connection ❤️', reply_markup=go_to_menu)
        draw.photo_del(callback_query.from_user.id)


# функция, которая отвечает за проверку, проходил ли человек чек-ап и вывод прошлых результатов
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('chk'))
async def process_callback_check_up(callback_query: types.CallbackQuery):
    global con
    await callback_query.message.delete()
    code = callback_query.data[3:]
    if int(code) == 1:
        if work_with_db.if_check(callback_query.from_user.id):
            await bot.send_message(callback_query.from_user.id, 'Какое у тебя настроение сегодня?',
                                   reply_markup=kb_check)
        else:
            await bot.send_message(callback_query.from_user.id, 'Вы уже отследили свое состояние сегодня ❤️',
                                   reply_markup=go_to_menu)
    else:
        cursor = con.cursor()
        sqlite_select_query = f"SELECT * from CheckUp where user_id='{callback_query.from_user.id}'"
        cursor.execute(sqlite_select_query)
        last_date = cursor.fetchall()
        print(last_date)
        if last_date:
            media = types.MediaGroup()
            draw.create_graphs(callback_query.from_user.id)
            media.attach_photo(types.InputFile('files//' + str(callback_query.from_user.id) + "_mood.png"),
                               caption='📈 На сегодняшний день графики вашего состояния выглядят так:')
            media.attach_photo(types.InputFile('files//' + str(callback_query.from_user.id) + "_anxiety.png"))
            media.attach_photo(types.InputFile('files//' + str(callback_query.from_user.id) + "_procrastination.png"))
            media.attach_photo(types.InputFile('files//' + str(callback_query.from_user.id) + "_loneliness.png"))
            media.attach_photo(types.InputFile('files//' + str(callback_query.from_user.id) + "_doubt.png"))
            media.attach_photo(types.InputFile('files//' + str(callback_query.from_user.id) + "_condemning.png"))
            await bot.send_media_group(callback_query.from_user.id, media=media)
            await bot.send_message(callback_query.from_user.id,
                                   'С заботой, твой connection ❤️', reply_markup=go_to_menu)
            draw.photo_del(callback_query.from_user.id)
        else:
            await bot.send_message(callback_query.from_user.id, 'Вы еще ни разу не отслеживали свое состояние ❤️',
                                   reply_markup=go_to_menu)


# показ психологов
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('all_psy'))
async def psycho(callback_query: types.CallbackQuery):
    global con

    await callback_query.message.delete()

    with con:
        list_psy = list(con.execute(f"SELECT * FROM Psychologist"))

    code = int(callback_query.data[7:])
    but = InlineKeyboardMarkup(row_width=3)

    but.add(InlineKeyboardButton('⬅️', callback_data='all_psy' + str((code - 1) % len(list_psy))))
    but.add(InlineKeyboardButton('👩 Выбрать психолога', callback_data='psy_' + str(list_psy[code][0]) + '_' +
                                                                       str(code % len(list_psy))))
    but.add(InlineKeyboardButton('➡️', callback_data='all_psy' + str((code + 1) % len(list_psy))))
    but.add(InlineKeyboardButton('➡️ Главное меню', callback_data='menu'))

    await callback_query.message.answer_photo(open('psy_photo//' + str(list_psy[code][0]) + '.jpg', "rb"),
                                              caption=(list_psy[code][1] + '\n' + list_psy[code][2] + '\n' +
                                                       list_psy[code][3] + '\n Количество консультаций: ' +
                                                       str(list_psy[code][5])),
                                              reply_markup=but)


# показ слотов психологов
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('psy_'))
async def psycho(callback_query: types.CallbackQuery):
    global con

    await callback_query.message.delete()

    data = callback_query.data.split('_')
    psy_id = data[1]
    but = InlineKeyboardMarkup()
    if len(data) == 3:
        today = datetime.date.today()
        margin_a = datetime.timedelta(days=6 - datetime.datetime.today().weekday())
        margin_b = datetime.timedelta(days=1)
        list_of_date = []

        with con:
            data_list = list(con.execute(f"SELECT date, id FROM Slot Where psycho_id='{psy_id}' and is_free='1';"))

        for date in data_list:
            if today + margin_b <= datetime.date(int(date[0][:4]), int(date[0][5:7]), int(date[0][8:])) <= today + margin_a:
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
            now_time = datetime.time.fromisoformat(str(datetime.datetime.now().time())) #  + ':' +
                                                   # str(datetime.datetime.now().time().minute))
            if (now_time < slot_time and
                datetime.datetime.now() == datetime.datetime(date_of_slots[0], date_of_slots[1], date_of_slots[2])) or \
                    (datetime.datetime.now() < datetime.datetime(date_of_slots[0], date_of_slots[1], date_of_slots[2])):
                print(1)
                but.add(InlineKeyboardButton('⏰ ' + time[0], callback_data='reserve_slot_' + str(time[1])))
        but.add(InlineKeyboardButton('⬅️ Назад к психологам', callback_data='all_psy' + data[3]))

        await bot.send_message(callback_query.from_user.id, 'Пожалуйста, выберите наиболее подходящее для вас время ❤️',
                               reply_markup=but)


# choose type of slot
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('reserve_slot_'))
async def reserve_slot(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    global con


    slot_id = callback_query.data.split('_')[2]
    choose_type_of_consult = InlineKeyboardMarkup()

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
                    id_con = list(con.execute(f"SELECT id FROM Consultation WHERE tran_id={i[0]} and slot_id is null"))[0][0]
                with con:
                    con.execute(f"UPDATE Consultation SET slot_id={slot_id} WHERE tran_id={i[0]} and id={id_con}")
                is_free_slot = 1
                await bot.send_message(callback_query.from_user.id, 'Поздравляю, вы записаны на консультацию! ❤️\n'
                                                                    'В личном кабинете вы можете посмотреть всю '
                                                                    'информацию о своих консультациях!',
                                       reply_markup=go_to_menu)
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
            with con:
                con.execute(f"UPDATE Slot SET is_free='0' WHERE id='{slot_id}'")

            choose_type_of_consult.add(
                InlineKeyboardButton('🧩 Диагностическая встреча', callback_data='create_tran_0_' + slot_id))
            choose_type_of_consult.add(
                InlineKeyboardButton('❤️ Хочу купить 1 консультацию', callback_data='create_tran_1_' + slot_id))
            choose_type_of_consult.add(
                InlineKeyboardButton('💖 Хочу купить 5 консультаций', callback_data='create_tran_5_' + slot_id))
            choose_type_of_consult.add(
                InlineKeyboardButton('💝 Хочу купить 10 консультаций', callback_data='create_tran_10_' + slot_id))
            choose_type_of_consult.add(InlineKeyboardButton('➡️ Главное меню', callback_data='menu'))

            await bot.send_message(callback_query.from_user.id, 'Пожалуйста, выберите тип услуги, которую хотите получить ❤️\n '
                                                                'При покупке 5 или 10 консультаций, вы записываетесь на это '
                                                                'время, а время для остальных консультаций можете выбрать '
                                                                'позже 😊\nЧтобы это сделать, просто снова выберите '
                                                                'психолога, дату и время консультации!',
                                   reply_markup=choose_type_of_consult)
        else:
            choose_type_of_consult.add(InlineKeyboardButton('⬅️ Назад к психологам', callback_data='all_psy' + '0'))
            await bot.send_message(callback_query.from_user.id, 'К сожалению, этот слот только заняли(\nПожалуйста, '
                                                                'выберите другой', reply_markup=choose_type_of_consult)


# create tran (or diagnostic consult)
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('create_tran_'))
async def create_tran(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    global con

    data = callback_query.data.split('_')
    slot_id = data[3]
    type_of_service = data[2]
    create_con_btn = InlineKeyboardMarkup()

    if int(type_of_service) == 0:
        # TODO: добавить проверку, что количество диагностик не превышает 3
        # TODO: при добавлении оплат в таблицу с транзакциями добавить поле is_paid и cost
        #  (соответственно добавление полей в таблицы и поиск изменится!!!!!!)
        print(callback_query.from_user.id)

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

        await bot.send_message(callback_query.from_user.id, 'Поздравляю, вы записаны на диагностическую '
                                                            'встречу ❤️\nВ личном кабинете вы можете посмотреть всю '
                                                            'информацию о своих консультациях!',
                               reply_markup=go_to_menu)
    else:
        sql1, data1 = 'INSERT INTO Transactions (user_id, date, time, is_diagnostic) values(?, ?, ?, ?)', []
        data1.append((callback_query.from_user.id, str(datetime.datetime.now().date()),
                      str(datetime.datetime.now().time()), False))

        with con:
            con.executemany(sql1, data1)

        with con:
            tran_id = list(con.execute(f"SELECT id FROM Transactions WHERE "
                                       f"user_id={callback_query.from_user.id} and is_diagnostic={0}"))[0][0]

        create_con_btn.add(InlineKeyboardButton('➡ Дальше', callback_data='create_con_' + str(type_of_service) + '_' +
                                                                          str(tran_id) + '_' + str(slot_id)))

        await bot.send_message(callback_query.from_user.id, 'Оплачено!', reply_markup=create_con_btn)


# create con
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('create_con_'))
async def create_con(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    global con

    data = callback_query.data.split('_')
    count = int(data[2])
    tran_id = data[3]
    slot_id = data[4]

    for i in range(count):
        if i == 0:
            sql1, data1 = 'INSERT INTO Consultation (tran_id, slot_id) values(?, ?)', []
            data1.append((tran_id, slot_id))
        else:
            sql1, data1 = 'INSERT INTO Consultation (tran_id) values(?)', []
            data1.append(tran_id)

        with con:
            con.executemany(sql1, data1)

    with con:
        psy_id = list(con.execute(f"SELECT psycho_id FROM Slot WHERE id={slot_id}"))[0][0]

    await bot.send_message(psy_id, "Пользователь " + str(callback_query.from_user.id) +
                           " к вам на консультацию!\nБолее подробную информацию можно посмотреть в личном "
                           "кабинете психолога)")

    await bot.send_message(callback_query.from_user.id, 'Поздравляю, вы записаны на консультацию! ❤️\n'
                                                        'В личном кабинете вы можете посмотреть всю '
                                                        'информацию о своих консультациях!',
                           reply_markup=go_to_menu)


# all consults (psy page)
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('my_consults'))
async def psy_consults(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    global con

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
                    btn.add(InlineKeyboardButton('💌 Отправить сообщение пользователю', callback_data='send_mess_' +
                                                                                                      str(user_id[0])))
                    btn.add(InlineKeyboardButton('✅ Отметить консультацию, как проведенную',
                                                 callback_data='done_con_' + str(i[0])))
                    st = "Диагностическая" if int(user_id[1]) == 1 else "Консультация"
                    await bot.send_message(callback_query.from_user.id, str(user_id[0]) + '\n' + str(lst[0][1]) + ' ' +
                                           str(lst[0][2]) + "\n" + st, reply_markup=btn)

    await bot.send_message(callback_query.from_user.id, 'end', reply_markup=go_to_menu)


# mark consultation as done
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('done_con'))
async def done_con(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    global con

    con_id = callback_query.data.split('_')[-1]
    print(con_id)

    with con:
        con.execute(f"UPDATE Consultation SET is_done={1} WHERE id={con_id}")

    await bot.send_message(callback_query.from_user.id, 'done', reply_markup=go_to_menu)


# send message to user
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('send_mess_'))
async def send_mes(callback_query: types.CallbackQuery):

    user_id = callback_query.data.split('_')[-1]

    await bot.send_message(callback_query.from_user.id, "Чтобы отправить сообщение пользователю " + user_id +
                           " вам нужно:\nНаписать: send/" + user_id + "/текст сообщения\nЕсли кнопка нажата по ошибке, "
                                                                      "то просто перейдите в главное меню",
                           reply_markup=go_to_menu)
    await bot.send_message(callback_query.from_user.id,
                           "Для удобства, скопируйте следующее сообщение, вставьте и дополните его:", reply_markup=None)
    await bot.send_message(callback_query.from_user.id, "send/" + user_id + "/", reply_markup=None)


# user account page
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('user_account'))
async def user_account(callback_query: types.CallbackQuery):
    await callback_query.message.delete()

    global con

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
                    future_consultation.append(list(con.execute(f"SELECT date, time, psycho_id FROM Slot WHERE id={i[1]}")))

    message = "Привет 😊\nКоличество оплаченных консультаций, на которые ты еще не запасался(ась): " + \
              str(count_consult_without_slot) + "\nКонсультации, которые ты оплатил(а) и записался(ась):"
    await callback_query.message.answer_photo(open('user.png', "rb"), caption=message, reply_markup=go_to_menu)

    for x in future_consultation:
        with con:
            psy_name = list(con.execute(f"SELECT name FROM Psychologist WHERE id={x[0][2]}"))[0][0]
        mess = "Психолог: " + str(psy_name) + "\nДата и время консультации: " + str(x[0][0]) + "  " + str(x[0][1])
        btn = InlineKeyboardMarkup()
        btn.add(InlineKeyboardButton('💌 Отправить сообщение психологу', callback_data='send_mess_' +
                                                                                          str(x[0][2])))
        await bot.send_message(callback_query.from_user.id, mess, reply_markup=btn)


# обработка фото-сообщений для админов, психологов, пользователей
@dp.message_handler(content_types=['photo'])
async def get_photo(message: types.Message):
    global con

    if str(message.from_user.id) == '596752948':

        with con:
            id = list(con.execute(f"SELECT id FROM Psychologist WHERE photo='нет фото';"))

        if id:
            await message.photo[-1].download(destination_file='psy_photo//' + str(id[0][0]) + '.jpg')

            with con:
                con.execute(f"UPDATE Psychologist SET photo='фото' WHERE id='{id[0][0]}';")

            await bot.send_message(message.from_user.id, 'photo set', reply_markup=go_to_menu)
        else:
            await bot.send_message(message.from_user.id, 'Нет психологов без фото', reply_markup=go_to_menu)
    else:
        await bot.send_message(message.from_user.id, 'Некорректный ввод данных', reply_markup=start_button)


# обработка текстовых сообщений для админов, психологов, пользователей
@dp.message_handler()
async def user_problems(message: types.Message):
    global con

    with con:
        psycho_list = [str(x[0]) for x in list(con.execute(f"SELECT id FROM Psychologist;"))]

    if message.text[:3] == 'add' and (str(message.from_user.id) == '596752948' or str(message.from_user.id) == '840638420'):
        mass = message.text.split('/')
        sql1, data1 = 'INSERT INTO Psychologist (id, name, problems, about, photo, rating) values(?, ?, ?, ?, ?, ?)', []
        data1.append((mass[1], mass[2], mass[3], mass[4], 'нет фото', 0))

        with con:
            con.executemany(sql1, data1)

        await bot.send_message(message.from_user.id, '10x', reply_markup=go_to_menu)
    elif message.text[:3] == 'del' and (str(message.from_user.id) == '596752948' or str(message.from_user.id) == '840638420'):

        with con:
            con.execute(f"DELETE from Psychologist WHERE id='{message.text[4:]}'")

        await bot.send_message(message.from_user.id, 'Психолог удален')

    elif message.text[:4] == 'slot' and str(message.from_user.id) in psycho_list:
        mass = message.text.split('/')
        sql1 = 'INSERT INTO Slot (id, psycho_id, date, time, is_free) values(?, ?, ?, ?, ?)'

        with con:
            count = int(list(con.execute(f"SELECT MAX(id) FROM Slot"))[0][0])

        for x in range(1, len(mass)):
            dt = mass[x].split()
            data1 = [(count + x, int(message.from_user.id), dt[0], dt[1], 1)]

            with con:
                con.executemany(sql1, data1)

        await bot.send_message(message.from_user.id, 'Ваши слоты установлены', reply_markup=go_to_menu)
    elif message.text[:3] == 'all' and (str(message.from_user.id) == '596752948' or str(message.from_user.id) == '840638420'):
        mass = message.text.split('/')

        with con:
            user_list = list(con.execute(f"SELECT id FROM Person"))

        for user in user_list:
            await bot.send_message(user[0], mass[1])
    elif message.text[:4] == 'send':
        mess = message.text.split('/')

        answer_kb = InlineKeyboardMarkup()
        answer_kb.add(InlineKeyboardButton('Ответить', callback_data='send_mess_' + str(message.from_user.id)))

        await bot.send_message(mess[1], "Новое сообщение:\n" + mess[2], reply_markup=answer_kb)
        await bot.send_message(message.from_user.id, 'Сообщение успешно отправлено!', reply_markup=go_to_menu)
    elif message.text[:7] == 'sup_bot':
        mess = message.text.split("/")[1]
        await bot.send_message(message.from_user.id, 'Сообщение успешно отправлено!\nСкоро наша команда вам ответит ❤',
                               reply_markup=go_to_menu)
        answer_kb = InlineKeyboardMarkup()
        answer_kb.add(InlineKeyboardButton('Ответить', callback_data='send_mess_' + str(message.from_user.id)))
        await bot.send_message('596752948', "Вопрос в поддержку от: " + str(message.from_user.id) + "\n" + mess,
                               reply_markup=answer_kb)
    elif message.text[:7] == 'sup_psy':
        mess = message.text.split("/")[1]
        await bot.send_message(message.from_user.id, 'Сообщение успешно отправлено!\nСкоро наша команда вам ответит ❤',
                               reply_markup=go_to_menu)
        answer_kb = InlineKeyboardMarkup()
        answer_kb.add(InlineKeyboardButton('Ответить', callback_data='send_mess_' + str(message.from_user.id)))
        await bot.send_message('840638420', "Вопрос в поддержку от: " + str(message.from_user.id) + "\n" + mess,
                               reply_markup=answer_kb)
    else:
        await bot.send_message(message.from_user.id, 'Некорректный ввод данных. Попробуйте снова',
                               reply_markup=go_to_menu)


'''АДМИНСКАЯ ЧАСТЬ'''
time_for_checkup = dict()

'''ОБЩАЯ ЧАСТЬ'''
executor.start_polling(dp, skip_updates=True)

# проверка, корректно ли введено время для чек-апа

# elif message.text[0:2].isdigit() and message.text[3:].isdigit() and int(message.text[0:2]) <= 23 and \
# message.text[2] == ':' and int(message.text[3:]) <= 59 and len(message.text) == 5:
#     print(11111)
#     time_for_checkup[message.from_user.id] = message.text
# сейчас проблемы добавляются вообще не правильно (но я пока это не использую)
#     work_with_db.add_new_person(message.from_user.id, ' '.join([str(x) for x in list_inline_btn[:-1]]))
#     print(message.text, message.from_user.id)
#     await bot.send_message(message.from_user.id, f'Хорошо, теперь тебе будут приходить напоминания ежедневно в '
#                                                  f'{time_for_checkup[message.from_user.id]}, чтобы ты не забывал(а)'
#                                                  f' отслеживать свое состояние ❤️',
#                            reply_markup=None)
#   await bot.send_message(message.from_user.id, 'Теперь переходи в главное меню!', reply_markup=go_to_menu)


# не работающая штука для ежедневных напоминаний
# @dp.message_handler()
# async def send_message(user_id):
#     await bot.send_message(user_id, "Хей🖖 не забудь отметить свое состояние сегодня!", reply_markup=go_to_menu)
#
#
# async def scheduler(time, user_id):
#     aioschedule.every().day.at(time).do(send_message(user_id))
#     print(1)
#     while True:
#         await aioschedule.run_pending()
#         await asyncio.sleep(1)


# async def on_startup(dp):
#     asyncio.create_task(scheduler())
