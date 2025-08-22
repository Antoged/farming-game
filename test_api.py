#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

BASE_URL = 'http://localhost:5000'
TEST_USER_ID = 12345

def test_api():
    """Тестирование API игры"""
    print("🧪 Начинаем тестирование API...")
    
    # Тест 1: Инициализация пользователя
    print("\n1️⃣ Тестируем инициализацию пользователя...")
    response = requests.post(f'{BASE_URL}/api/init', json={
        'user_id': TEST_USER_ID,
        'username': 'TestPlayer'
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Пользователь инициализирован: {data}")
    else:
        print(f"❌ Ошибка инициализации: {response.text}")
        return
    
    # Тест 2: Получение фермы
    print("\n2️⃣ Тестируем получение фермы...")
    response = requests.get(f'{BASE_URL}/api/farm?user_id={TEST_USER_ID}')
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Ферма загружена: {len(data.get('farm', []))} участков")
        print(f"🌤️ Погода: {data.get('weather', {})}")
    else:
        print(f"❌ Ошибка загрузки фермы: {response.text}")
    
    # Тест 3: Получение магазина
    print("\n3️⃣ Тестируем получение магазина...")
    response = requests.get(f'{BASE_URL}/api/shop')
    
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', [])
        print(f"✅ Магазин загружен: {len(items)} товаров")
        for item in items[:3]:  # Показать первые 3 товара
            print(f"   🌱 {item.get('seed_type')}: {item.get('price')} монет")
    else:
        print(f"❌ Ошибка загрузки магазина: {response.text}")
    
    # Тест 4: Покупка семени
    if response.status_code == 200 and items:
        print("\n4️⃣ Тестируем покупку семени...")
        first_item = items[0]
        response = requests.post(f'{BASE_URL}/api/buy', json={
            'user_id': TEST_USER_ID,
            'seed_type': first_item['seed_type']
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Покупка: {data}")
        else:
            print(f"❌ Ошибка покупки: {response.text}")
    
    # Тест 5: Посадка семени
    print("\n5️⃣ Тестируем посадку семени...")
    response = requests.post(f'{BASE_URL}/api/plant', json={
        'user_id': TEST_USER_ID,
        'plot_id': 1,
        'seed_type': 'carrot'
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Посадка: {data}")
    else:
        print(f"❌ Ошибка посадки: {response.text}")
    
    # Тест 6: Получение инвентаря
    print("\n6️⃣ Тестируем получение инвентаря...")
    response = requests.get(f'{BASE_URL}/api/inventory?user_id={TEST_USER_ID}')
    
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', [])
        print(f"✅ Инвентарь загружен: {len(items)} предметов")
    else:
        print(f"❌ Ошибка загрузки инвентаря: {response.text}")
    
    # Тест 7: Получение статистики
    print("\n7️⃣ Тестируем получение статистики...")
    response = requests.get(f'{BASE_URL}/api/stats?user_id={TEST_USER_ID}')
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Статистика: Деньги: {data.get('money')}, Уровень: {data.get('level')}")
    else:
        print(f"❌ Ошибка загрузки статистики: {response.text}")
    
    # Тест 8: Получение погоды
    print("\n8️⃣ Тестируем получение погоды...")
    response = requests.get(f'{BASE_URL}/api/weather')
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Погода: {data.get('name')} {data.get('emoji')}")
    else:
        print(f"❌ Ошибка загрузки погоды: {response.text}")
    
    print("\n🎉 Тестирование завершено!")

if __name__ == '__main__':
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Не удается подключиться к серверу. Убедитесь, что webapp.py запущен на порту 5000")
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
