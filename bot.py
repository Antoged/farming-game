import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, WEBAPP_URL, SEEDS
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
            InlineKeyboardButton("📊 Статистика", callback_data="stats")
        ],
        [
            InlineKeyboardButton("🛒 Магазин", callback_data="shop")
        ],
        [
            InlineKeyboardButton("🌤️ Погода", callback_data="weather")
        ],
        [
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
1. Нажмите "Играть в ферму" чтобы открыть игру
2. Покупайте семена в магазине
3. Сажайте их на участки фермы
4. Собирайте урожай и продавайте
5. Зарабатывайте деньги и развивайтесь!

🌤️ Погода влияет на рост растений и цены
🛒 Магазин обновляется каждые 5 минут
⏰ Урожай растет в реальном времени

Нажмите "Играть в ферму" чтобы начать!
    """
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "help":
        help_text = """
🎮 Помощь по игре:

🏠 Ферма:
• У вас есть 9 участков для посадки
• Нажмите на пустой участок чтобы посадить семечко
• Когда урожай готов, участок подсвечивается оранжевым
• Нажмите на готовый участок чтобы собрать урожай

🛒 Магазин:
• Покупайте семена разных типов
• Чем дороже семечко, тем реже оно появляется
• Магазин обновляется каждые 5 минут
• Цены могут варьироваться

📦 Инвентарь:
• Здесь хранятся собранные плоды
• Каждый плод имеет случайный вес, размер и качество
• Продавайте плоды чтобы получить деньги
• Качество влияет на цену

🌤️ Погода:
• Погода меняется каждые 30 минут
• Влияет на скорость роста и цены
• Солнечная погода: +20% к росту, +10% к ценам
• Дождливая погода: +50% к росту, +30% к ценам
• Гроза: -20% к росту, +50% к ценам

💰 Экономика:
• Начните с дешевых семян (морковь, картошка)
• Постепенно покупайте более дорогие
• Золотое яблоко - самый редкий и дорогой урожай
• Развивайте ферму и становитесь богатым фермером!
        """
        keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(help_text, reply_markup=reply_markup)
    elif query.data == "back_to_main":
        # Возвращаемся к главному меню
        user = update.effective_user
        welcome_text = f"""
🌾 Добро пожаловать в Фермерскую игру, {user.first_name}!

🎮 Управляйте своей фермой:
🌱 Сажайте семена и собирайте урожай
🛒 Покупайте новые семена в магазине
📦 Продавайте урожай в инвентаре
🌤️ Следите за погодой и её влиянием

💰 Начните с 100 монет
🌱 У вас есть 9 участков земли
🛒 Магазин обновляется каждые 5 минут
⏰ Урожай растет в реальном времени

Нажмите "Играть в ферму" чтобы начать!
    """
        keyboard = [
            [InlineKeyboardButton("🎮 Играть в ферму", web_app=WebAppInfo(url=WEBAPP_URL))],
            [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
            [InlineKeyboardButton("🛒 Магазин", callback_data="shop")],
            [InlineKeyboardButton("🌤️ Погода", callback_data="weather")],
            [InlineKeyboardButton("❓ Помощь", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(welcome_text, reply_markup=reply_markup)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда для просмотра статистики"""
    user = update.effective_user
    stats = game.get_player_stats(user.id)
    
    stats_text = f"""
📊 Статистика игрока {user.first_name}:

💰 Деньги: {stats['money']} монет
📈 Уровень: {stats['level']}
📦 Предметов в инвентаре: {stats['inventory_count']}
💎 Общая стоимость инвентаря: {stats['total_inventory_value']} монет

🎯 Количество каждого типа:
"""
    
    for item_type, count in stats['item_counts'].items():
        seed_name = SEEDS.get(item_type, {}).get('name', item_type)
        stats_text += f"• {seed_name}: {count} шт.\n"
    
    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(stats_text, reply_markup=reply_markup)

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда для просмотра магазина"""
    shop_items = game.get_shop_items_with_names()
    
    if not shop_items:
        await update.message.reply_text("🛒 Магазин пуст. Загляните позже!")
        return
    
    shop_text = "🛒 Текущие товары в магазине:\n\n"
    
    for item in shop_items:
        shop_text += f"🌱 {item['name']}\n"
        shop_text += f"💰 Цена: {item['price']} монет\n"
        shop_text += f"⏰ Время роста: {item['growth_time']} секунд\n"
        shop_text += "─" * 20 + "\n"
    
    shop_text += "\n💡 Нажмите 'Играть в ферму' чтобы купить!"
    
    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(shop_text, reply_markup=reply_markup)

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда для просмотра погоды"""
    weather_info = game.get_current_weather_info()
    
    weather_emoji = {
        'sunny': '☀️',
        'rainy': '🌧️', 
        'cloudy': '☁️',
        'stormy': '⛈️',
        'normal': '🌤️'
    }
    
    emoji = weather_emoji.get(weather_info['type'], '🌤️')
    
    weather_text = f"""
{emoji} Текущая погода: {weather_info['name']}

📈 Множитель цен: x{weather_info['price_multiplier']}
🌱 Множитель роста: x{weather_info['growth_multiplier']}

💡 Погода влияет на:
• Скорость роста растений
• Цены на урожай
• Общую экономику игры
    """
    
    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(weather_text, reply_markup=reply_markup)

def main() -> None:
    """Запуск бота"""
    # Создать приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавить обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("shop", shop))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Запустить планировщик игровых событий
    scheduler.start()
    
    # Запустить бота
    logger.info("Бот запущен!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
