import logging

from bot.dbreader import *
from bot.dbwriter import writer

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.markdown import hlink
from aiogram.utils.executor import start_webhook
from bot.settings import (BOT_TOKEN, HEROKU_APP_NAME,
                          WEBHOOK_URL, WEBHOOK_PATH,
                          WEBAPP_HOST, WEBAPP_PORT)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

keyboard_buttons = ['Музика', 'Фільми', 'YouTube', 'Книги']


@dp.message_handler(commands='start')
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*keyboard_buttons)

    await message.answer('<b>Привіт!</b>\n'
                         '\n'
                         'Тебе вітає бот <b>"Знай українське"</b>!\n'
                         '\n'
                         'Тут ти зможеш знайти багато цікавого:\n'
                         'фільми, популярну і не дуже музику, сучасних українських діячів, блогерів та їх продукти, '
                         'цікаві факти про нашу країну та багато іншого і це все наше - українське!\n'
                         '\n'
                         'Тисни кнопку нижче і почни споживати наше!'
                         '\n\n'
                         '/help - Детальніше', parse_mode=types.ParseMode.HTML, reply_markup=keyboard)


@dp.message_handler(commands='help')
async def start(message: types.Message):
    await message.answer('<b>Привіт!</b>\n'
                         '\n'
                         'Тебе вітає бот <b>"Знай українське"</b>!\n'
                         '\n'
                         'За допомогою цього бота можна шукати український контент всього в два кліки.\n'
                         'Натисни /start, щоб почати роботу.\n'
                         'В тебе зʼявляться кнопки з категоріями контенту, який тобі цікавий - тисни, до прикладу, "YouTube".\n'
                         'Тобі будуть приведенені жанри та категорії за якими ти зможеш відфільтрувати цікавий для тебе контент.\n'
                         'Вибирай жанр або категорію і дивись повідомлення в яких буде твій улюблений контент. В цих же повідомленнях є посилання на ресурс з якого ти зможеш черпати інформацію.\n'
                         '\n'
                         '<b>Маєш ідеї або пропозиції, а можливо і критика - пиши автору: @pryvedenets_vania</b>', parse_mode=types.ParseMode.HTML)


@dp.message_handler()
async def message_dispatcher(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['text'] = message.text

        for text in keyboard_buttons:
            if text == data['text']:

                info = db_reader(data['text'].lower())

                buttons = [types.InlineKeyboardButton(text=row[0].strip(), callback_data=row[0].strip()) for row in info]

                keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
                keyboard.add(*buttons)
                await message.answer('Вибери свій улюблений жанр:', reply_markup=keyboard)


@dp.callback_query_handler()
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    id = callback_query.from_user.id
    comm_dispath(id)

    async with state.proxy() as data:
        topic = data['text'].lower()
        genre = callback_query.data
        info = genre_constructor(topic, genre)

        if topic == 'музика':
            message = 'Збірку пісень цього виконавця слухай на сервісі YouTube Music за посиланням нижче.'
        elif topic == 'фільми':
            message = 'Цей фільм можна глянути за посиланням нижче.'
        elif topic == 'youtube':
            message = 'Посилання на Ютуб канал нижче.'
        elif topic == 'книги':
            message = 'Переглянути і купити книгу можна за посиланням нижче.'

        await bot.send_message(callback_query.from_user.id, 'Ось контент українських виконавців в жанрі ' + genre + ':\nНасолоджуйся:)')

        for case in info:
            author, image, link, description = case
            link = hlink('Посилання на ресурс', link)
            await bot.send_photo(callback_query.from_user.id, photo=open('images/'+topic+'/'+image, 'rb'),
                                 caption='<b>{}</b>\n\n''{}\n{}\n{}'.format(author, description, message, link), parse_mode=types.ParseMode.HTML)



async def on_startup(dp):
    logging.warning(
        'Starting connection. ')
    await bot.set_webhook(WEBHOOK_URL,drop_pending_updates=True)


async def on_shutdown(dp):
    logging.warning('Bye! Shutting down webhook connection')


def main():
    writer()
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
