import datetime
import os
import sqlite3 as sl

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# возвращает лист из клавиш, которые отвечают за кнопки у договора и согласия на обработку персональных данных
def get_contract_kb() -> list:
    return [InlineKeyboardButton("✖️ Я прочитал и принимаю условия договора",
                                 callback_data='attach_1_0'),
            InlineKeyboardButton("✅ Я прочитал и принимаю условия договора",
                                 callback_data='nope'),
            InlineKeyboardButton("✖️ Я подтверждаю согласие на обработку персональных данных",
                                 callback_data='attach_1_1'),
            InlineKeyboardButton("✅ Я подтверждаю согласие на обработку персональных данных",
                                 callback_data='nope')]


# возвращает клавиатуру с кнопкой продолжить
def get_continue_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup().add(InlineKeyboardButton('➡️  Продолжить', callback_data='attach_0_0'))


# возвращает стартовую клавиатуру с кнопкой начать
def get_start_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup().add(InlineKeyboardButton('🚀 Начать', callback_data='run'))


# возвращает клавиатуру с кнопкой возврата в основное меню
def get_go_to_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup().add(InlineKeyboardButton('➡️ Главное меню', callback_data='menu'))


# возвращает лист клавиш, которые отвечают за разделы главного меню
def get_main_buttons_kb() -> list:
    return [
        InlineKeyboardButton('👤 Мой кабинет', callback_data='user_account'),
        InlineKeyboardButton('📅 Моё состояние', callback_data='my_feeling'),
        InlineKeyboardButton('🙋‍♀️Обратиться к психологу', callback_data='need_help'),
        InlineKeyboardButton('🎁 Получить гайд!', callback_data='guide'),
        InlineKeyboardButton('⚙️ Техподдержка', callback_data='support'),
        InlineKeyboardButton('⚙️ Кабинет психолога', callback_data='psycho'),
        InlineKeyboardButton('⚙️ Кабинет администратора', callback_data='admin')]


# возвращает клавиатуру администратора
def get_admin_kb() -> InlineKeyboardMarkup:
    admin_kb = InlineKeyboardMarkup(row_width=1)
    # admin_kb.add(InlineKeyboardButton('⚙️ Показать психологов', callback_data='show_psycho'))
    # admin_kb.add(InlineKeyboardButton('⚙️ Добавить психолога в команду', callback_data='add'))
    # admin_kb.add(InlineKeyboardButton('⚙️ Удалить психолога из команды', callback_data='del_psy'))
    admin_kb.add(InlineKeyboardButton('⚙️ Сделать рассылку', callback_data='send_to_all'))  # all
    admin_kb.add(InlineKeyboardButton('➡️ Главное меню', callback_data='menu'))
    return admin_kb


# возвращает клавиатуру для кабинета психолога
def get_psycho_kb() -> InlineKeyboardMarkup:
    psycho_kb = InlineKeyboardMarkup(row_width=1)
    psycho_kb.add(InlineKeyboardButton('⚙️ Текущие консультации', callback_data='my_consults'))
    # psycho_kb.add(InlineKeyboardButton('⚙️ Добавить слоты на неделю', callback_data='slot'))
    # psycho_kb.add(InlineKeyboardButton('⚙️ Удалить слот', callback_data='remove_slot'))
    psycho_kb.add(InlineKeyboardButton('➡️ Главное меню', callback_data='menu'))
    return psycho_kb


# возвращает клавиатуру для раздела технической поддержки бота
def get_support_kb() -> InlineKeyboardMarkup:
    support_kb = InlineKeyboardMarkup(row_width=1)
    support_kb.add(InlineKeyboardButton("👤 По вопросам работы психологов", callback_data='sup_psy',
                                        url="https://t.me/ilya_undertakes"))
    support_kb.add(InlineKeyboardButton("🤖 По вопросам работы бота", callback_data='sup_bot',
                                        url="https://t.me/egor_dementev"))
    support_kb.add(InlineKeyboardButton('➡️ Главное меню', callback_data='menu'))
    return support_kb


# возвращает клавиатуру для личного кабинета пользователя
def get_user_account_kb() -> InlineKeyboardMarkup:
    user_acc_kb = InlineKeyboardMarkup(row_width=1)
    user_acc_kb.add(InlineKeyboardButton('💌 Связаться с психологом', callback_data='text_to_psy'))
    user_acc_kb.add(InlineKeyboardButton('➡️ Главное меню', callback_data='menu'))
    return user_acc_kb


# возвращает клавиатуру с кнопкой просмотра всех психологов (all_user_problems)
def get_show_psycho_kb() -> InlineKeyboardMarkup:
    psy_kb = InlineKeyboardMarkup()
    psy_kb.add(InlineKeyboardButton('👩 Посмотреть психологов', callback_data='all_psy0'))
    psy_kb.add(InlineKeyboardButton('➡️ Главное меню', callback_data='menu'))
    return psy_kb


# возвращает клавиатуру для оценки своего состояния
def get_check_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup().add(InlineKeyboardButton('🤗', callback_data='con4'),
                                      InlineKeyboardButton('😄', callback_data='con3'),
                                      InlineKeyboardButton('😐', callback_data='con2'),
                                      InlineKeyboardButton('☹️', callback_data='con1'),
                                      InlineKeyboardButton('😭', callback_data='con0'))


# возвращает клавиатуру для окна оценки своего состояния
def get_check_up_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton('🗸 Отследить состояние', callback_data='chk1'),
        InlineKeyboardButton('📈 Посмотреть мои графики', callback_data='chk2'),
        InlineKeyboardButton('📖 Прочитать статью', url='http://connection.online.tilda.ws/self_reflection'),
        InlineKeyboardButton('➡️ Главное меню', callback_data='menu'))


# возвращает клавиатуру с типами консультаций
def get_types_of_consults(slot_id) -> InlineKeyboardMarkup:
    choose_type_of_consult = InlineKeyboardMarkup()
    choose_type_of_consult.add(
        InlineKeyboardButton('🧩 Диагностическая встреча', callback_data='create_tran_0_' + slot_id))
    # choose_type_of_consult.add(
    #     InlineKeyboardButton('❤️ Хочу купить 1 консультацию', callback_data='create_tran_1_' + slot_id))
    # choose_type_of_consult.add(
    #     InlineKeyboardButton('💖 Хочу купить 5 консультаций', callback_data='create_tran_5_' + slot_id))
    # choose_type_of_consult.add(
    #     InlineKeyboardButton('💝 Хочу купить 10 консультаций', callback_data='create_tran_10_' + slot_id))
    choose_type_of_consult.add(InlineKeyboardButton('➡️ Главное меню', callback_data='menu'))
    return choose_type_of_consult


# возвращает список вопросов для оценки своего состояния
def get_questions() -> list:
    return ['Оцени свой уровень спокойствия сегодня:\n🤗 - совсем не было повода переживать\n😭 - сильное '
            'чувство тревожности',
            'Насколько сегодня ты был(а) продуктивным(ной), по сравнению с планом намеченных дел?\n🤗 - сделал(а) все, '
            'что хотел / у меня сегодня выходной\n😭 - весь день был потрачен впустую',
            'Преследовало ли тебя чувство одиночества в любом его проявлении?\n🤗 - совсем нет, меня окружают '
            'прекрасные люди\n😭 - сильно переживал(а) по этому поводу',
            'Насколько уверенно ты себя чувствовал(а) сегодня?\n🤗 - чувствовал(а) себя на все 100% уверенно\n😭 - '
            'ощущал(а) себя очень неуверенно',
            'Были ли раздражающие тебя факторы?\n🤗 - ничего раздражающего не наблюдал(а), чувствовал(а) себя '
            'умиротворенно\n😭 - весь день меня преследовало раздражение',
            'Доволен(льна) ли ты собой?\n🤗 - абсолютно, не было никаких поводов осуждать себя\n😭 - '
            'были причины осуждать себя']


# список с админами сервиса
def get_admin_list() -> list:
    return ['596752948', '840638420']


def get_super_admin_id():
    return '596752948'


# возвращает объект для работы с базой данных
def get_data_base_object():
    return sl.connect("resources/db//connection.db")


# returns bot
def get_bot_token() -> str:
    return os.getenv('TOKEN')


def is_can_be_deleted(mess_date):
    now = datetime.datetime.now()

    if (now - mess_date).total_seconds() < 48 * 3600:
        return True
    return False
