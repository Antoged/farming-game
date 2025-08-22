# Настройка Telegram Бота

## Шаг 1: Получение токена бота

1. Откройте Telegram и найдите @BotFather
2. Отправьте команду `/newbot`
3. Следуйте инструкциям:
   - Введите имя бота (например: "Farming Game Bot")
   - Введите username бота (например: "farming_game_bot")
4. BotFather выдаст вам токен вида: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

## Шаг 2: Создание файла .env

Создайте файл `.env` в корневой папке проекта со следующим содержимым:

```env
# Telegram Bot Token (замените на ваш токен)
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# URL веб-приложения (GitHub Pages)
WEBAPP_URL=https://antoged.github.io/farming-game/

# Секретный ключ для Flask (сгенерируйте случайный)
SECRET_KEY=your_secret_key_here

# Режим отладки
DEBUG=False

# Настройки базы данных
DATABASE_URL=sqlite:///farm_game.db

# Настройки сервера
HOST=0.0.0.0
PORT=5000

# Настройки логирования
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Настройки безопасности
ALLOWED_HOSTS=antoged.github.io

# Настройки Telegram Web App
TELEGRAM_WEBAPP_URL=https://antoged.github.io/farming-game/telegram-app.html
```

## Шаг 3: Запуск бота

После создания файла `.env` с правильным токеном:

```bash
python bot.py
```

## Важно!

- **НЕ коммитьте файл .env в Git** - он содержит секретные данные
- Файл .env уже добавлен в .gitignore
- Храните токен в безопасности
- Если токен скомпрометирован, используйте `/revoke` у @BotFather

## Проверка работы

1. Запустите бота
2. Найдите вашего бота в Telegram
3. Отправьте команду `/start`
4. Бот должен ответить приветственным сообщением
