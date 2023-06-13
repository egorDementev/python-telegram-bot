import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from start_application import init_start_application
from admin import init_admin_application
from check_up import init_checkup_application
from consultations import init_consultations_application
from psychologists import init_psycho_application
from registration import init_registration
from support import init_support_application
from transactions import init_transactions_application

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

init_start_application(bot, dp)
init_admin_application(bot, dp)
init_checkup_application(bot, dp)
init_consultations_application(bot, dp)
init_psycho_application(bot, dp)
init_registration(bot, dp)
init_support_application(bot, dp)
init_transactions_application(bot, dp)

executor.start_polling(dp, skip_updates=True)
