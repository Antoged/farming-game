import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, WEBAPP_URL, SEEDS, WEATHER_EFFECTS
from game_logic import GameLogic
import threading
import time
from datetime import datetime, timedelta

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

game = GameLogic()

class GameScheduler:
    def __init__(self):
        self.running = False
    
    def start(self):
        self.running = True
        threading.Thread(target=self._run_scheduler, daemon=True).start()
    
    def stop(self):
        self.running = False
    
    def _run_scheduler(self):
        while self.running:
            try:
                # Обновить магазин каждые 5 минут
                game.refresh_shop()
                logger.info("Магазин обновлен")
                
                # Изменить погоду каждые 30 минут
                weather_type, weather_data = game.change_weather()
                logger.info(f"Погода изменена на: {weather_data['name']}")
                
                # Ждать 5 минут до следующего обновления
                time.sleep(300)  # 5 минут
                
            except Exception as e:
                logger.error(f"Ошибка в планировщике: {e}")
                time.sleep(60)  # Ждать минуту при ошибке

scheduler = GameScheduler()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user = update.effective_user
    
    # Создать или получить игрока
    player = game.db.get_or_create_player(user.id, user.username)
    
    # Создать клавиатуру с кнопками
    keyboard = [
        [
            InlineKeyboardButton(
                "🌾 Играть в ферму", 
                web_app=WebAppInfo(url=f"{WEBAPP_URL}?user_id={user.id}")
            )
        ],
        [
            InlineKeyboardButton("📊 Статистика", callback_data="stats"),
            InlineKeyboardButton("🛒 Магазин", callback_data="shop")
        ],
        [
            InlineKeyboardButton("🌤️ Погода", callback_data="weather"),
            InlineKeyboardButton("ℹ️ Помощь", callback_data="help")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""
🎮 Добро пожаловать в Фермерскую игру, {user.first_name}!

🌱 Вы начинающий фермер. У вас есть:
💰 {player['money']} монет
📊 Уровень {player['level']}

🎯 Как играть:
1. Нажмите "🌾 Играть в ферму" чтобы открыть игру
2. Покупайте семена в магазине
3. Сажайте их на участки фермы
4. Собирайте урожай и продавайте
5. Зарабатывайте деньги и развивайтесь!

🌤️ Погода влияет на рост растений и цены
🛒 Магазин обновляется каждые 5 минут
⏰ Урожай растет в реальном времени

Нажмите "🌾 Играть в ферму" чтобы начать!
"""
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    player = game.db.get_or_create_player(user.id, user.username)
    
    if query.data == "stats":
        stats = game.get_player_stats(user.id)
        stats_text = f"""
📊 Статистика игрока {user.first_name}:

💰 Монеты: {stats['money']}
📊 Уровень: {stats['level']}
⭐ Опыт: {stats['experience']}
📦 Предметов в инвентаре: {stats['inventory_count']}
🌱 Посажено культур: {stats['total_planted']}
🌾 Собрано урожая: {stats['total_harvested']}
"""
        await query.edit_message_text(stats_text)
        
    elif query.data == "shop":
        shop_items = game.get_shop_items()
        shop_text = "🛒 Магазин семян:\n\n"
        
        for item in shop_items:
            emoji = SEEDS[item['seed_type']]['emoji']
            name = item['name']
            price = item['price']
            shop_text += f"{emoji} {name}: 💰{price}\n"
        
        shop_text += "\nНажмите '🌾 Играть в ферму' чтобы купить!"
        await query.edit_message_text(shop_text)
        
    elif query.data == "weather":
        current_weather = game.get_current_weather_info()
        weather_emoji = WEATHER_EFFECTS[current_weather['type']]['emoji']
        weather_name = current_weather['name']
        
        weather_text = f"""
🌤️ Текущая погода:

{weather_emoji} {weather_name}

📈 Множитель роста: x{current_weather['growth_multiplier']}
💰 Множитель цен: x{current_weather['price_multiplier']}

Погода влияет на скорость роста растений и цены на рынке!
"""
        await query.edit_message_text(weather_text)
        
    elif query.data == "help":
        help_text = """
ℹ️ Помощь по игре:

🎮 Основные команды:
/start - Начать игру
/farm - Управление фермой
/market - Рынок
/stats - Статистика
/help - Эта справка

🌱 Как играть:
1. Откройте игру через кнопку "🌾 Играть в ферму"
2. Покупайте семена в магазине
3. Сажайте их на участки фермы
4. Ждите роста (время зависит от культуры)
5. Собирайте урожай и продавайте
6. Зарабатывайте деньги и развивайтесь!

🌤️ Погода:
- Солнечно: +20% рост, +10% цены
- Дождливо: +50% рост, +30% цены
- Облачно: обычные показатели
- Гроза: -20% рост, -10% цены

🛒 Магазин обновляется каждые 5 минут
⏰ Урожай растет в реальном времени
"""
        await query.edit_message_text(help_text)

async def farm_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /farm - показать статус фермы"""
    user = update.effective_user
    farm_status = game.get_farm_status(user.id)
    
    farm_text = f"🌱 Ферма игрока {user.first_name}:\n\n"
    
    for i, plot in enumerate(farm_status):
        if plot['status'] == 'empty':
            farm_text += f"🌱 Участок {i+1}: Пустой\n"
        elif plot['status'] == 'planted':
            time_left = plot['time_left']
            seed_name = plot['seed_name']
            farm_text += f"🌿 Участок {i+1}: {seed_name} (осталось {time_left}s)\n"
        elif plot['status'] == 'ready':
            seed_name = plot['seed_name']
            farm_text += f"🌾 Участок {i+1}: {seed_name} - готов к сбору!\n"
    
    farm_text += "\nНажмите '🌾 Играть в ферму' для управления!"
    
    await update.message.reply_text(farm_text)

async def market_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /market - показать рынок"""
    user = update.effective_user
    shop_items = game.get_shop_items()
    
    market_text = f"🛒 Рынок семян:\n\n"
    
    for item in shop_items:
        emoji = SEEDS[item['seed_type']]['emoji']
        name = item['name']
        price = item['price']
        market_text += f"{emoji} {name}: 💰{price}\n"
    
    market_text += "\nНажмите '🌾 Играть в ферму' чтобы купить!"
    
    await update.message.reply_text(market_text)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /stats - показать статистику"""
    user = update.effective_user
    stats = game.get_player_stats(user.id)
    
    stats_text = f"""
📊 Статистика игрока {user.first_name}:

💰 Монеты: {stats['money']}
📊 Уровень: {stats['level']}
⭐ Опыт: {stats['experience']}
📦 Предметов в инвентаре: {stats['inventory_count']}
🌱 Посажено культур: {stats['total_planted']}
🌾 Собрано урожая: {stats['total_harvested']}

Продолжайте играть чтобы улучшить статистику!
"""
    
    await update.message.reply_text(stats_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /help - показать справку"""
    help_text = """
ℹ️ Помощь по игре:

🎮 Основные команды:
/start - Начать игру
/farm - Управление фермой
/market - Рынок
/stats - Статистика
/help - Эта справка

🌱 Как играть:
1. Откройте игру через кнопку "🌾 Играть в ферму"
2. Покупайте семена в магазине
3. Сажайте их на участки фермы
4. Ждите роста (время зависит от культуры)
5. Собирайте урожай и продавайте
6. Зарабатывайте деньги и развивайтесь!

🌤️ Погода:
- Солнечно: +20% рост, +10% цены
- Дождливо: +50% рост, +30% цены
- Облачно: обычные показатели
- Гроза: -20% рост, -10% цены

🛒 Магазин обновляется каждые 5 минут
⏰ Урожай растет в реальном времени
"""
    
    await update.message.reply_text(help_text)

def main() -> None:
    """Запуск бота"""
    # Создать приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавить обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("farm", farm_command))
    application.add_handler(CommandHandler("market", market_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Запустить планировщик
    scheduler.start()
    
    # Запустить бота
    print("🌾 Фермерская игра запущена!")
    application.run_polling()

if __name__ == '__main__':
    main()
