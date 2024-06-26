# Игра Блэкджек

Добро пожаловать в проект игры Блэкджек! Это простая реализация классической карточной игры Блэкджек, также известной как 21. Игра написана на Python и включает интеграцию с Telegram ботом для взаимодействия.

## Содержание

- [Особенности](#особенности)
- [Установка](#установка)
- [Использование](#использование)
- [Правила](#правила)
- [Вклад](#вклад)
- [Лицензия](#лицензия)

## Особенности

- Однопользовательский режим против компьютерного дилера
- Основные механики игры Блэкджек, включая взятие карт, остановку и перебор
- Интеграция с Telegram ботом для удобного взаимодействия

## Установка

1. **Клонируйте репозиторий:**

    ```sh
    git clone https://github.com/FolfBasky/blackjack.git
    cd blackjack
    ```

2. **Создайте виртуальное окружение (опционально, но рекомендуется):**

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # На Windows используйте `venv\Scripts\activate`
    ```

3. **Установите необходимые зависимости:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Создайте бота в Telegram и получите токен API.**

5. **Создайте файл `.env` и добавьте в него токен вашего бота:**

    ```
    API_TOKEN=YOUR_API_TOKEN_HERE
    ```

## Использование

1. **Запустите игру:**

    ```sh
    python main.py
    ```

2. **Используйте команды в Telegram для взаимодействия с ботом:**
    - `/start` или `/new` - начать новую игру
    - `/hit` - взять карту
    - `/stand` - остановиться
    - `/help` - показать список команд

## Правила

- Цель Блэкджека — набрать больше очков, чем у дилера, не превышая 21 очко.
- Картинки стоят 10 очков, тузы могут стоить 1 или 11 очков, а все остальные карты стоят по своему номиналу.
- Игроки могут "взять" карту (hit) или "остановиться" (stand).
- Если сумма очков игрока превышает 21, он "перебирает" и проигрывает.
- Дилер берет карты до тех пор, пока сумма его карт не достигнет 17 или более очков.

## Вклад

Приветствуются любые вклады в проект! Если вы хотите внести свой вклад, пожалуйста, выполните следующие шаги:

1. **Сделайте форк репозитория**
2. **Создайте новую ветку:**

    ```sh
    git checkout -b feature/YourFeatureName
    ```

3. **Внесите изменения и зафиксируйте их:**

    ```sh
    git commit -m 'Add some feature'
    ```

4. **Отправьте изменения в удаленный репозиторий:**

    ```sh
    git push origin feature/YourFeatureName
    ```

5. **Создайте новый пулл-реквест**

## Лицензия

Этот проект лицензирован на условиях лицензии MIT. Подробности см. в файле [LICENSE](LICENSE).
