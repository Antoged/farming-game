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
    
    # Создать простую клавиатуру только с основными кнопками
    keyboard = [
        [
            InlineKeyboardButton(
                "🌾 Играть в ферму", 
                web_app=WebAppInfo(url=f"{WEBAPP_URL}?user_id={user.id}")
            )
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
    
    if query.data == "help":
        help_text = """
ℹ️ Помощь по игре:

🎮 Основные команды:
/start - Начать игру

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

Все действия выполняются в игре через кнопку "🌾 Играть в ферму"!
"""
        await query.edit_message_text(help_text)

def main() -> None:
    """Запуск бота"""
    # Создать приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавить только необходимые обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Запустить планировщик
    scheduler.start()
    
    # Запустить бота
    print("🌾 Фермерская игра запущена!")
    application.run_polling()

if __name__ == '__main__':
    main()
