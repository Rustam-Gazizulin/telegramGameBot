import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, Text
from aiogram.types import Message

API_TOKEN: str = '5976510239:AAE_GAdpynTlNEHbJNtdIroDDjRzXwl_8xY'

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

# Количество попыток, доступных пользователю в игре
ATTEMPTS: int = 7

# Словарь, в котором будут храниться данные пользователя
users: dict = {}


# Функция возвращающая случайное целое число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)


# Хендлер для команды /start
@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Привет!\nДавай сыграем в игру "Угадай число"?\n\n'
                         'Чтобы получить правила игры и список доступных '
                         'команд - отправьте команду /help')

    # Если пользователь только запустил бота и его нет в словаре'
    # 'users - добавляем его в словарь
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}


# Хендлер для команды /help
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
                         f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
                         f'попыток\n\nДоступные команды:\n/help - правила '
                         f'игры и список команд\n/cancel - выйти из игры\n'
                         f'/stat - посмотреть статистику\n\nДавай сыграем?')


# Хендлер для команды /stat
@dp.message(Command(commands=['stat']))
async def process_stat_command(message: Message):
    await message.answer(f'Всего игр сыграно: {users[message.from_user.id]["total_games"]}\n'
                         f'Количество побед: {users[message.from_user.id]["wins"]}')


# Хендлер для команды /cancel
@dp.message(Command(commands=['cancel']))
async def send_photo_echo(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('Игра закончена.')
        users[message.from_user.id]['in_game'] = False
    else:
        await message.answer('Мы еще не начинали игру чтобы ее заканчивать')


# Хендлер для обработки согласия пользователя сыграть в игру
@dp.message(Text(text=["Да", "Давай", "Сыграем", "Ok", "Игра", "Играть", "Хочу играть"], ignore_case=True))
async def process_positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer("Я загадал число от 1 до 100, слабо угадать за 7 попыток?")
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        users[message.from_user.id]['attempts'] = ATTEMPTS
    else:
        await message.answer('Пока мы играем в игру я могу '
                             'реагировать только на числа от 1 до 100 '
                             'и команды /cancel и /stat')


# Хендлер для обработки отказа играть в игру
@dp.message(Text(text=['Нет', 'Не', 'Не хочу', 'Не буду'], ignore_case=True))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer('Жаль :(\n\nЕсли захотите поиграть - просто '
                             'напишите об этом')
    else:
        await message.answer('Мы же сейчас с вами играем. Присылайте, '
                             'пожалуйста, числа от 1 до 100')


# Хендлер для обработки числовых ответов от пользователя
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            await message.answer("Ура вы угадали число!\n\n"
                                 "Может еще партию?")
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['wins'] += 1
            users[message.from_user.id]['total_games'] += 1
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            await message.answer("Загаданное число меньше вашего!")
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            await message.answer("Загаданное число больше вашего!")
        if users[message.from_user.id]['attempts'] == 0:
            await message.answer(f'К сожалению, у вас больше не осталось попыток'
                                 f'Вы проиграли!'
                                 f'Мое число было {users[message.from_user.id]["secret_number"]}'
                                 f'Сыграем еще?')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
    else:
        await message.answer("Мы еще не начали играть, хотите сыграть?")


# Хендлер обрабатывающий прочие запросы
@dp.message()
async def process_other_text_answer(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}

        await message.answer(f'Я довольно ограниченный бот, давайте  просто сыграем в игру?\n'
                             f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
                             f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
                             f'попыток\n\nДоступные команды:\n/help - правила '
                             f'игры и список команд\n/cancel - выйти из игры\n'
                             f'/stat - посмотреть статистику\n\nДавай сыграем?'
                             )

    elif users[message.from_user.id]['in_game']:
        await message.answer("Мы же сейчас играем в цифры\n"
                             "Присылайте пожалуйста числа от 1 до 100")


if __name__ == '__main__':
    dp.run_polling(bot)
