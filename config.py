import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://antoged.github.io/farming/telegram-app.html')

# Game Configuration
SHOP_REFRESH_INTERVAL = 300  # 5 minutes in seconds
WEATHER_CHANGE_INTERVAL = 1800  # 30 minutes in seconds

# Seed Types and their properties
SEEDS = {
    'carrot': {
        'name': 'Морковь',
        'emoji': '🥕',
        'base_price': 10,
        'growth_time': 60,  # seconds
        'shop_chance': 0.8,
        'min_weight': 50,
        'max_weight': 200,
        'min_size': 10,
        'max_size': 25
    },
    'tomato': {
        'name': 'Помидор',
        'emoji': '🍅',
        'base_price': 25,
        'growth_time': 120,
        'shop_chance': 0.6,
        'min_weight': 80,
        'max_weight': 300,
        'min_size': 15,
        'max_size': 35
    },
    'potato': {
        'name': 'Картошка',
        'emoji': '🥔',
        'base_price': 15,
        'growth_time': 90,
        'shop_chance': 0.7,
        'min_weight': 100,
        'max_weight': 500,
        'min_size': 20,
        'max_size': 40
    },
    'cucumber': {
        'name': 'Огурец',
        'emoji': '🥒',
        'base_price': 20,
        'growth_time': 75,
        'shop_chance': 0.65,
        'min_weight': 60,
        'max_weight': 250,
        'min_size': 12,
        'max_size': 30
    },
    'strawberry': {
        'name': 'Клубника',
        'emoji': '🍓',
        'base_price': 50,
        'growth_time': 180,
        'shop_chance': 0.4,
        'min_weight': 20,
        'max_weight': 80,
        'min_size': 8,
        'max_size': 20
    },
    'watermelon': {
        'name': 'Арбуз',
        'emoji': '🍉',
        'base_price': 100,
        'growth_time': 300,
        'shop_chance': 0.2,
        'min_weight': 2000,
        'max_weight': 8000,
        'min_size': 50,
        'max_size': 100
    },
    'golden_apple': {
        'name': 'Золотое яблоко',
        'emoji': '🍎',
        'base_price': 500,
        'growth_time': 600,
        'shop_chance': 0.05,
        'min_weight': 150,
        'max_weight': 400,
        'min_size': 25,
        'max_size': 45
    }
}

# Weather effects
WEATHER_EFFECTS = {
    'sunny': {
        'name': 'Солнечно',
        'emoji': '☀️',
        'growth_multiplier': 1.2,
        'price_multiplier': 1.1,
        'chance': 0.4
    },
    'rainy': {
        'name': 'Дождливо',
        'emoji': '🌧️',
        'growth_multiplier': 1.5,
        'price_multiplier': 1.3,
        'chance': 0.3
    },
    'cloudy': {
        'name': 'Облачно',
        'emoji': '☁️',
        'growth_multiplier': 1.0,
        'price_multiplier': 1.0,
        'chance': 0.2
    },
    'stormy': {
        'name': 'Гроза',
        'emoji': '⛈️',
        'growth_multiplier': 0.8,
        'price_multiplier': 0.9,
        'chance': 0.1
    }
}

# Default weather
DEFAULT_WEATHER = 'normal'
