pre_buy_demo_alert = '''\
Так как сейчас я запущен в тестовом режиме, для оплаты нужно использовать карточку с номером 1111 1111 1111 1026, 12/22, 
CVC 000
Счёт для оплаты:
'''

tm_title = 'Покупка психологических консультаций в количестве: '
tm_description = '''\
Всего одно ваше действие может перевернуть жизнь на 180 градусов!\n
Станьте счастливее с Connection ❤
'''

successful_payment = '''
Ура! Платеж на сумму `{total_amount} {currency}` совершен успешно! Приятного пользования новенькой машиной времени!
Правила возврата средств смотрите в /terms
Купить ещё одну машину времени своему другу - /buy
'''


MESSAGES = {
    'pre_buy_demo_alert': pre_buy_demo_alert,
    'tm_title': tm_title,
    'tm_description': tm_description,
    'successful_payment': successful_payment,
}