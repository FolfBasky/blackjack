from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import sqlite3
import os
import asyncio 
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage


class GameStatesBoomber(StatesGroup):
    main_page = State()
    game_started = State()

class BombGame:
    def __init__(self, difficulty: str = 'easy'):
        self.difficulty = difficulty
        self.keyboard = InlineKeyboardMarkup()
        self.buttons = [[InlineKeyboardButton(f"{i},{j}", callback_data=f"{i},{j}") for j in range(3)] for i in range(3)]
        for row in self.buttons:
            self.keyboard.row(*row)

        if difficulty == 'easy':
            num_bombs = 1
        elif difficulty == 'medium':
            num_bombs = 3
        else:
            num_bombs = 6

        self.bombs = random.sample([(i, j) for i in range(3) for j in range(3)], num_bombs)

        self.markup = ReplyKeyboardMarkup(resize_keyboard=True)
        self.markup.add(KeyboardButton("🎲 Начать игру 🎲"))
        self.markup.add(KeyboardButton("🔃 Вернутся к выбору игры 🔃"))


    async def start(self,message: Message):
        await message.answer('В разработке...')
        #await GameStatesBoomber.main_page.set()

    async def process_choice(self, call: types.CallbackQuery):
        await call.message.answer('Игра началась!', reply_markup=self.markup)
        i, j = map(int, call.data.split(','))
        if (i, j) in self.bombs:
            await call.message.answer("BOOM! Вы проиграли")
        else:
            await call.message.answer("Вы выиграли!")

    async def start_game(self, message: Message):
        await message.answer('Выберите ячейку:', reply_markup=self.keyboard)
        await GameStatesBoomber.game_started.set()

