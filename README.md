# 🌾 Фермерская Игра - Telegram Bot

Интерактивная фермерская игра в Telegram с веб-интерфейсом для управления фермой.

## 🌐 Веб-сайт проекта

**🌾 [Farming Game - Live Demo](https://antoged.github.io/farming-game/)**

Полнофункциональный веб-сайт проекта с подробным описанием возможностей, технологического стека и инструкциями по установке.

## 🎮 Особенности

- 🌱 Выращивание различных культур
- 🐄 Разведение животных
- 🏪 Торговля на рынке
- 💰 Экономическая система
- 🌐 Веб-интерфейс для управления
- 📊 Статистика и достижения
- 🏆 Система уровней и опыта

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.8+
- Telegram Bot Token
- Ngrok (для локальной разработки)

### Установка

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/Antoged/farming-game.git
cd farming-game
```

2. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

3. **Настройте переменные окружения:**
```bash
cp env_example.txt .env
```

Отредактируйте файл `.env`:
```env
BOT_TOKEN=your_telegram_bot_token
WEBAPP_URL=your_webapp_url
```

4. **Запустите приложение:**
```bash
python run.py
```

## 📁 Структура проекта

```
farming/
├── bot.py              # Telegram бот
├── webapp.py           # Веб-приложение
├── game_logic.py       # Игровая логика
├── database.py         # Работа с базой данных
├── config.py           # Конфигурация
├── run.py              # Главный скрипт запуска
├── requirements.txt    # Зависимости Python
├── templates/          # HTML шаблоны
│   └── index.html
├── static/             # Статические файлы
└── tests/             # Тесты
```

## 🛠️ Разработка

### Локальная разработка

1. **Настройте ngrok для туннелирования:**
```bash
python setup_ngrok.py
```

2. **Запустите в режиме разработки:**
```bash
python run.py
```

### Тестирование

```bash
# Запуск всех тестов
python -m pytest

# Запуск конкретного теста
python test_bot.py
python test_game.py
```

## 🌐 Веб-интерфейс

### Локальная разработка
Веб-интерфейс доступен по адресу: `http://localhost:5000`

### GitHub Pages
- **Статический лендинг**: [https://antoged.github.io/farming/](https://antoged.github.io/farming/)
- **Telegram Mini App**: [https://antoged.github.io/farming/telegram-app.html](https://antoged.github.io/farming/telegram-app.html)

### Функции веб-интерфейса:
- 📊 Просмотр статистики фермы
- 🌱 Управление посадками
- 🐄 Управление животными
- 🏪 Торговля на рынке
- 📈 Графики и аналитика

## 📱 Telegram Bot

### Команды бота:
- `/start` - Начать игру
- `/farm` - Управление фермой
- `/market` - Рынок
- `/stats` - Статистика
- `/help` - Помощь

## 🚀 Развертывание

### Heroku

1. Создайте приложение на Heroku
2. Настройте переменные окружения
3. Разверните код

### VPS

1. Установите Python и зависимости
2. Настройте nginx для проксирования
3. Запустите через systemd

## 📊 Мониторинг

- Логи приложения: `logs/app.log`
- Статистика базы данных: `logs/db_stats.log`
- Ошибки: `logs/errors.log`

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE)

## 🆘 Поддержка

- 💬 Telegram: @growfarm_support_bot
- 🐛 Issues: [GitHub Issues](https://github.com/Antoged/farming-game/issues)

## 🙏 Благодарности

- Telegram Bot API
- Flask Framework
- SQLite Database
- Все участники проекта

---

⭐ Если проект вам понравился, поставьте звездочку!
