from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from blackjack import BlackJack, GameStatesBlackdjack
from boombers import BombGame, GameStatesBoomber
import asyncio
import random
from config import token
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from DB import *

bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())

markup = ReplyKeyboardMarkup(resize_keyboard=True)
markup1 = ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(KeyboardButton("🎲 Начать игру 🎲"))
markup.add(KeyboardButton("💰Пополнить баланс💰"), KeyboardButton("💸 Вывести деньги 💸"))
markup.add(KeyboardButton("🚹 Профиль 🚹"), KeyboardButton("🏆 Топ игроков 🏆"))
markup.add(KeyboardButton("👓 О разработчике 👓"))
markup1.add(KeyboardButton("Взять карту"), KeyboardButton("Пасс"))

class Game(StatesGroup):
    choice = State()

class Main:
    def __init__(self):
        self.markup = ReplyKeyboardMarkup(resize_keyboard=True)
        self.markup.add(KeyboardButton('БлекДжек'), KeyboardButton('Бомбочки'))

    async def start(self, message: Message):
        await message.answer('Выберите игру:', reply_markup=self.markup)
        await Game.choice.set()

async def start(message: Message):
    await message.answer('Игра в BlackJack')
    await message.answer('В блэкджеке десятки, валеты, дамы и короли стоят по 10 очков.\nТуз стоит 11 очков\nЗадача набрать максимально близкое число очков к 21, но не переборщить с этим!',reply_markup=markup)

    add_or_update_user(message.from_user.id, message.from_user.first_name, 0, 1.0, 0, 0)

async def start_game(message: Message):
    increment_count_games(message.from_user.id)
    player_balance = get_user_info(message.from_user.id)[2]
    if player_balance < 100:
        await message.answer(f'Баланс слишком мал ({player_balance}), пополните его', reply_markup=markup)
        return None
    else:
        await message.answer(f'Баланс {player_balance}')
        await GameStatesBlackdjack.game_started.set()

    global blackjack
    blackjack = BlackJack()

    await message.answer('Игра в BlackJack началась', reply_markup=markup1)
    blackjack.take_card()
    await asyncio.sleep(0.1)
    global msgP, msgB
    msgP = await message.answer(f'Вам попалась карта - {str(blackjack.card) + random.choice(blackjack.card_suits)}\nВаше кол-во очков = {blackjack.score}')

    blackjack.take_card_bot()
    await asyncio.sleep(0.1)
    msgB = await message.answer( f'Дилеру попалась карта - {str(blackjack.bot_card)  + random.choice(blackjack.card_suits)}\nКол-во очков дилера = {blackjack.bot_score}')
    await message.answer('Выберите действие на клавиатуре, чтобы продолжить')

async def take_a_card(message: Message,state: FSMContext):
    result = get_user_info(message.from_user.id)
    player_balance = result[2]
    count_games = result[-2]
    wins = result[-1]

    blackjack.take_card()
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    global editMessageP
    try:
        if editMessageP:
            val = str(editMessageP.text).split("\n")[0].split("-")[1].strip()
            val2 = str(editMessageP.text).split('\n')[1].replace('(','').replace(')','').strip()
            lst_cards = '('+ val + ' ' + val2 + ' ' + ')'
        else:
            val = str(msgP.text).split("\n")[0].split("-")[1].strip()
            lst_cards = f'({val})'
    except:
        val = str(msgP.text).split("\n")[0].split("-")[1].strip()
        lst_cards = f'({val})'

    ttx = f'Вам попалась карта - {str(blackjack.card) + random.choice(blackjack.card_suits)}\n{lst_cards}\nВаше кол-во очков = {blackjack.score}'
    editMessageP = await bot.edit_message_text(chat_id=msgP.chat.id, message_id=msgP.message_id ,text=ttx)
    if blackjack.score > 21:
        await message.answer('Вы проиграли!', reply_markup=markup)
        player_balance -= 100
        await message.answer(f'Ваш баланс {player_balance}')
        await state.finish()
        editMessageP = None
    elif blackjack.score == 21:
        await message.answer('У вас блекджек!', reply_markup=markup)
        player_balance += 150
        wins += 1
        await message.answer(f'Ваш баланс {player_balance}')
        await state.finish()
        editMessageP = None


    update_user(message.from_user.id, message.from_user.first_name, player_balance,  round(wins/count_games,2), count_games, wins)

async def Pass(message: Message,state: FSMContext):
    result = get_user_info(message.from_user.id)
    player_balance = result[2]
    count_games = result[-2]
    wins = result[-1]
    global editMessageP
    editMessageP = None
    #await message.answer( f'Ваше кол-во очков = {blackjack.score}')
    while (blackjack.bot_score < 18):
        await asyncio.sleep(0.15)
        if blackjack.bot_score <= 18:
            blackjack.take_card_bot()

            global editMessageB
            try:
                if editMessageB:
                    val = str(editMessageB.text).split("\n")[0].split("-")[1].strip()
                    val2 = str(editMessageB.text).split('\n')[1].replace('(','').replace(')','').strip()
                    lst_cards = '('+ val + ' ' + val2 + ' ' + ')'
                else:
                    val = str(msgP.text).split("\n")[0].split("-")[1].strip()
                    lst_cards = f'({val})'
            except:
                val = str(msgB.text).split("\n")[0].split("-")[1].strip()
                lst_cards = f'({val})'

            ttx = f'Дилеру попалась карта - {str(blackjack.bot_card) + random.choice(blackjack.card_suits)}\n{lst_cards}\nКол-во очков дилера = {blackjack.bot_score}'
            editMessageB = await bot.edit_message_text(chat_id=msgB.chat.id, message_id=msgB.message_id ,text=ttx)

            if blackjack.bot_score > 21:
                await message.answer('Вы выиграли!', reply_markup=markup)
                player_balance += 100
                wins += 1
                await message.answer(f'Ваш баланс {player_balance}')
                await state.finish()
                update_user(message.from_user.id, message.from_user.first_name, player_balance, round(wins/count_games,2), count_games, wins)
                editMessageB = None
                return None


    if blackjack.score > blackjack.bot_score:
        await message.answer('Вы выиграли!', reply_markup=markup)
        player_balance += 100
        wins += 1
        await message.answer(f'Ваш баланс {player_balance}')
        await state.finish()
    elif blackjack.score == blackjack.bot_score:
        await message.answer('Ничья!',reply_markup=markup)
        await message.answer(f'Ваш баланс {player_balance}')
        await state.finish()
    else:
        await message.answer('Вы проиграли!',reply_markup=markup)
        player_balance -= 100
        await message.answer(f'Ваш баланс {player_balance}')
        await state.finish()

    update_user(message.from_user.id, message.from_user.first_name, player_balance, round(wins/count_games,2), count_games, wins)
    editMessageB = None

async def add_money(message: Message):
    player_balance = get_user_info(message.from_user.id)[2]
    player_balance += 1000
    await message.answer( 'Ваш баланс был успешно пополнен!')
    await message.answer( f'Баланс = {player_balance}')

    update_user(message.from_user.id, message.from_user.first_name, player_balance, *get_user_info(message.from_user.id)[3:])

async def withdraw_money(message: Message):
    player_balance = get_user_info(message.from_user.id)[2]
    player_balance = 0
    await message.answer( 'Все средства были успешно выведены!')
    await message.answer( f'Баланс = {player_balance}')

    update_user(message.from_user.id, message.from_user.first_name, player_balance, *get_user_info(message.from_user.id)[3:])

async def get_profile_info(message: Message):
    await message.answer('Баланс = {}, процент побед = {}, кол-во игр = {}'.format(*get_user_info(message.from_user.id)[2:-1]))

async def get_top10(message: Message):
    g = get_top_players()
    for i,x in enumerate(g):
        username, count_games, kd = x
        await message.answer(f'{i+1}. {username} - {count_games} игр (КД = {kd})')

async def develop(message: Message):
    txt = '''Hi! I am a Russian developer and I have been writing in Python for almost 2 years. I have completed many courses and am writing my own projects. (They are shown in the profile) In parallel, I solve logical problems on sites such as codewars.com , codingame.com and others. I have worked with SQL, API, Flask, aiogram, http, regular strings, captchas, AI, images, sounds videos in python. I like to write bots for automating work with websites. I can make simple websites.'''
    await message.answer(txt)
    await message.answer('https://github.com/FolfBasky')

if __name__ == '__main__':
    main = Main()
    dp.register_message_handler(start,commands='start')

    dp.register_message_handler(start, text="БлекДжек", state=Game.choice)
    dp.register_message_handler(start_game, text="🎲 Начать игру 🎲")
    dp.register_message_handler(take_a_card, text="Взять карту", state=GameStatesBlackdjack.game_started)
    dp.register_message_handler(Pass, text="Пасс", state=GameStatesBlackdjack.game_started)
    dp.register_message_handler(add_money, text="💰Пополнить баланс💰")
    dp.register_message_handler(withdraw_money, text="💸 Вывести деньги 💸")
    dp.register_message_handler(get_profile_info, text="🚹 Профиль 🚹")
    dp.register_message_handler(get_top10, text="🏆 Топ игроков 🏆")
    dp.register_message_handler(develop, text="👓 О разработчике 👓")

    boomber = BombGame()
    dp.register_message_handler(boomber.start, text="Бомбочки", state=Game.choice)
    dp.callback_query_handler(boomber.process_choice, text="0,0", state=GameStatesBoomber.game_started)
    dp.register_message_handler(main.start, text="🔃 Вернутся к выбору игры 🔃", state=GameStatesBoomber.main_page)

    executor.start_polling(dp, skip_updates=True)
