import random


from aiogram.dispatcher.filters.state import StatesGroup, State
from DB import create_db





class GameStatesBlackdjack(StatesGroup):
    main_page = State()
    game_started = State()

class BlackJack:
    def __init__(self):
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Валет', 'Королева', 'Король', 'Туз']  * 4
        self.card_suits = [' ♠️', ' ♥️', ' ♦️', ' ♣️']
        self.score = 0
        self.bot_score = 0
        self.card = None
        self.bot_card = None
        create_db()

    def take_card(self):
        self.card = self.deck.pop(self.deck.index(random.choice(self.deck)))
        if isinstance(self.card,int):
            self.score += self.card
        else:
            if self.card in ['Валет', 'Королева', 'Король']:
                self.score += 10
            else:
                self.score += 11

    def take_card_bot(self):
        self.bot_card = self.deck.pop(self.deck.index(random.choice(self.deck)))
        if isinstance(self.bot_card,int):
            self.bot_score += self.bot_card
        else:
            if self.bot_card in ['Валет', 'Королева', 'Король']:
                self.bot_score += 10
            else:
                self.bot_score += 11
