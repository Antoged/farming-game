#!/usr/bin/env python3
"""
Скрипт для тестирования игровой логики
"""

from game_logic import GameLogic
from config import SEEDS, WEATHER_EFFECTS
import time

def test_game_logic():
    """Тестирование игровой логики"""
    print("🧪 Тестирование игровой логики...")
    
    game = GameLogic()
    
    # Тестовый пользователь
    test_user_id = 12345
    
    print("\n1. Создание игрока...")
    player = game.db.get_or_create_player(test_user_id, "test_user")
    print(f"✅ Игрок создан: {player['username']}, Деньги: {player['money']}")
    
    print("\n2. Тестирование посадки семечка...")
    success, message = game.plant_seed(test_user_id, 1, "carrot")
    print(f"Посадка моркови: {message}")
    
    print("\n3. Тестирование магазина...")
    game.refresh_shop()
    shop_items = game.get_shop_items_with_names()
    print(f"Товаров в магазине: {len(shop_items)}")
    for item in shop_items[:3]:  # Показать первые 3
        print(f"  - {item['name']}: {item['price']} монет")
    
    print("\n4. Тестирование погоды...")
    weather_type, weather_data = game.change_weather()
    print(f"Погода изменена на: {weather_data['name']}")
    
    print("\n5. Тестирование покупки семечка...")
    if shop_items:
        seed_type = shop_items[0]['seed_type']
        success, message = game.buy_seed(test_user_id, seed_type)
        print(f"Покупка {seed_type}: {message}")
    
    print("\n6. Тестирование статистики...")
    stats = game.get_player_stats(test_user_id)
    print(f"Статистика игрока:")
    print(f"  - Деньги: {stats['money']}")
    print(f"  - Уровень: {stats['level']}")
    print(f"  - Предметов в инвентаре: {stats['inventory_count']}")
    
    print("\n7. Тестирование расчета урожая...")
    harvest = game.calculate_harvest("tomato", 1.2)
    print(f"Урожай помидора: {harvest}")
    
    print("\n✅ Тестирование завершено!")

def test_seeds():
    """Тестирование конфигурации семян"""
    print("\n🌱 Тестирование конфигурации семян...")
    
    for seed_type, seed_data in SEEDS.items():
        print(f"\n{seed_data['name']}:")
        print(f"  - Цена: {seed_data['base_price']} монет")
        print(f"  - Время роста: {seed_data['growth_time']} секунд")
        print(f"  - Шанс в магазине: {seed_data['shop_chance'] * 100}%")
        print(f"  - Вес: {seed_data['min_weight']}-{seed_data['max_weight']}g")
        print(f"  - Размер: {seed_data['min_size']}-{seed_data['max_size']}cm")

def test_weather():
    """Тестирование системы погоды"""
    print("\n🌤️ Тестирование системы погоды...")
    
    for weather_type, weather_data in WEATHER_EFFECTS.items():
        print(f"\n{weather_data['name']}:")
        print(f"  - Множитель роста: x{weather_data['growth_multiplier']}")
        print(f"  - Множитель цен: x{weather_data['price_multiplier']}")
        print(f"  - Шанс: {weather_data['chance'] * 100}%")

if __name__ == "__main__":
    print("🌾 Тестирование Фермерской игры")
    print("=" * 40)
    
    try:
        test_seeds()
        test_weather()
        test_game_logic()
        
        print("\n🎉 Все тесты пройдены успешно!")
        
    except Exception as e:
        print(f"\n❌ Ошибка тестирования: {e}")
        import traceback
        traceback.print_exc()
