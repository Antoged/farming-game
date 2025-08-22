import random
import time
from datetime import datetime, timedelta
from database import Database
from config import SEEDS, WEATHER_EFFECTS, SHOP_REFRESH_INTERVAL, WEATHER_CHANGE_INTERVAL

class GameLogic:
    def __init__(self):
        self.db = Database()
    
    def calculate_harvest(self, seed_type, weather_multiplier=1.0):
        """Рассчитать урожай с учетом погоды"""
        seed_data = SEEDS[seed_type]
        
        # Случайный вес и размер
        weight = random.uniform(seed_data['min_weight'], seed_data['max_weight'])
        size = random.uniform(seed_data['min_size'], seed_data['max_size'])
        
        # Качество зависит от размера и веса
        quality = min(1.0, (weight / seed_data['max_weight'] + size / seed_data['max_size']) / 2)
        
        # Базовая цена с учетом качества
        base_price = seed_data['base_price']
        price = int(base_price * quality * weather_multiplier)
        
        return {
            'weight': round(weight, 2),
            'size': round(size, 2),
            'quality': round(quality, 2),
            'price': price
        }
    
    def plant_seed(self, user_id, plot_id, seed_type):
        """Посадить семечко"""
        if seed_type not in SEEDS:
            return False, "Неизвестный тип семечка"
        
        # Проверить, что участок свободен
        plots = self.db.get_farm_plots(user_id)
        for plot in plots:
            if plot['plot_id'] == plot_id:
                return False, "Участок уже занят"
        
        # Получить данные семечка
        seed_data = SEEDS[seed_type]
        
        # Получить текущую погоду
        weather = self.db.get_current_weather()
        weather_multiplier = weather['multiplier'] if weather else 1.0
        
        # Рассчитать время роста с учетом погоды
        growth_time = int(seed_data['growth_time'] / weather_multiplier)
        
        # Посадить семечко
        self.db.plant_seed(user_id, plot_id, seed_type, growth_time)
        
        return True, f"Посажено {seed_data['name']} на участок {plot_id}"
    
    def harvest_plot(self, user_id, plot_id):
        """Собрать урожай с участка"""
        plots = self.db.get_farm_plots(user_id)
        
        for plot in plots:
            if plot['plot_id'] == plot_id:
                # Проверить, готов ли урожай
                planted_time = datetime.fromisoformat(plot['planted_at'].replace('Z', '+00:00'))
                current_time = datetime.now()
                growth_time = timedelta(seconds=plot['growth_time'])
                
                if current_time - planted_time >= growth_time:
                    # Собрать урожай
                    seed_type = plot['seed_type']
                    
                    # Получить текущую погоду
                    weather = self.db.get_current_weather()
                    weather_multiplier = weather['multiplier'] if weather else 1.0
                    
                    # Рассчитать урожай
                    harvest = self.calculate_harvest(seed_type, weather_multiplier)
                    
                    # Добавить в инвентарь
                    self.db.add_to_inventory(
                        user_id, 
                        seed_type, 
                        harvest['weight'], 
                        harvest['size'], 
                        harvest['quality'], 
                        harvest['price']
                    )
                    
                    # Удалить с участка
                    self.db.harvest_plot(plot['id'])
                    
                    return True, f"Собран урожай: {SEEDS[seed_type]['name']} (Цена: {harvest['price']} монет)"
                else:
                    remaining_time = growth_time - (current_time - planted_time)
                    return False, f"Урожай еще не готов. Осталось: {int(remaining_time.total_seconds())} секунд"
        
        return False, "Участок пуст"
    
    def get_farm_status(self, user_id):
        """Получить статус фермы"""
        plots = self.db.get_farm_plots(user_id)
        current_time = datetime.now()
        
        farm_status = []
        for plot in plots:
            if plot['status'] == 'empty':
                farm_status.append({
                    'plot_id': plot['plot_id'],
                    'seed_type': None,
                    'seed_name': None,
                    'status': 'empty',
                    'progress': 0
                })
            elif plot['status'] == 'planted':
                planted_time = datetime.fromisoformat(plot['planted_at'].replace('Z', '+00:00'))
                growth_time = timedelta(seconds=plot['growth_time'])
                time_passed = current_time - planted_time
                
                if time_passed >= growth_time:
                    status = "ready"
                    progress = 100
                    time_left = 0
                else:
                    progress = min(100, (time_passed.total_seconds() / plot['growth_time']) * 100)
                    remaining_time = growth_time - time_passed
                    status = "planted"
                    time_left = int(remaining_time.total_seconds())
                
                farm_status.append({
                    'plot_id': plot['plot_id'],
                    'seed_type': plot['seed_type'],
                    'seed_name': SEEDS[plot['seed_type']]['name'],
                    'status': status,
                    'progress': round(progress, 1),
                    'time_left': time_left
                })
            elif plot['status'] == 'ready':
                farm_status.append({
                    'plot_id': plot['plot_id'],
                    'seed_type': plot['seed_type'],
                    'seed_name': SEEDS[plot['seed_type']]['name'],
                    'status': 'ready',
                    'progress': 100,
                    'time_left': 0
                })
        
        return farm_status
    
    def buy_seed(self, user_id, seed_type):
        """Купить семечко в магазине"""
        shop_items = self.db.get_shop_items()
        
        for item in shop_items:
            if item['seed_type'] == seed_type:
                # Проверить, хватает ли денег
                player = self.db.get_or_create_player(user_id)
                if player['money'] >= item['price']:
                    # Купить семечко
                    self.db.update_player_money(user_id, -item['price'])
                    return True, f"Куплено {SEEDS[seed_type]['name']} за {item['price']} монет"
                else:
                    return False, "Недостаточно денег"
        
        return False, "Товар не найден в магазине"
    
    def sell_item(self, user_id, item_id):
        """Продать предмет из инвентаря"""
        price = self.db.sell_item(item_id)
        if price > 0:
            return True, f"Предмет продан за {price} монет"
        else:
            return False, "Предмет не найден"
    
    def refresh_shop(self):
        """Обновить магазин"""
        # Очистить просроченные товары
        self.db.clear_expired_shop_items()
        
        # Добавить новые товары
        current_time = datetime.now()
        available_until = current_time + timedelta(seconds=SHOP_REFRESH_INTERVAL)
        
        for seed_type, seed_data in SEEDS.items():
            # Проверить шанс появления в магазине
            if random.random() < seed_data['shop_chance']:
                # Цена может варьироваться
                price_variation = random.uniform(0.8, 1.2)
                price = int(seed_data['base_price'] * price_variation)
                
                self.db.add_shop_item(seed_type, price, available_until)
    
    def change_weather(self):
        """Изменить погоду"""
        # Выбрать погоду на основе шансов
        weather_types = list(WEATHER_EFFECTS.keys())
        chances = [WEATHER_EFFECTS[wt]['chance'] for wt in weather_types]
        
        # Нормализовать шансы
        total_chance = sum(chances)
        normalized_chances = [c / total_chance for c in chances]
        
        # Выбрать погоду
        weather_type = random.choices(weather_types, weights=normalized_chances)[0]
        weather_data = WEATHER_EFFECTS[weather_type]
        
        # Установить погоду
        current_time = datetime.now()
        ends_at = current_time + timedelta(seconds=WEATHER_CHANGE_INTERVAL)
        
        self.db.set_weather(weather_type, weather_data['price_multiplier'], ends_at)
        
        return weather_type, weather_data
    
    def get_player_stats(self, user_id):
        """Получить статистику игрока"""
        player = self.db.get_or_create_player(user_id)
        inventory = self.db.get_inventory(user_id)
        
        # Подсчитать общую стоимость инвентаря
        total_inventory_value = sum(item['price'] for item in inventory)
        
        # Подсчитать количество каждого типа предметов
        item_counts = {}
        for item in inventory:
            item_type = item['item_type']
            if item_type not in item_counts:
                item_counts[item_type] = 0
            item_counts[item_type] += 1
        
        # Получить статистику по посадкам и сбору урожая
        farm_plots = self.db.get_farm_plots(user_id)
        total_planted = sum(1 for plot in farm_plots if plot['status'] == 'planted')
        total_harvested = sum(1 for plot in farm_plots if plot['status'] == 'ready')
        
        return {
            'money': player['money'],
            'experience': player['experience'],
            'level': player['level'],
            'total_inventory_value': total_inventory_value,
            'inventory_count': len(inventory),
            'item_counts': item_counts,
            'total_planted': total_planted,
            'total_harvested': total_harvested
        }
    
    def get_shop_items(self):
        """Получить товары магазина"""
        shop_items = self.db.get_shop_items()
        
        items_with_names = []
        for item in shop_items:
            seed_data = SEEDS[item['seed_type']]
            items_with_names.append({
                **item,
                'name': seed_data['name'],
                'growth_time': seed_data['growth_time']
            })
        
        return items_with_names
    
    def get_shop_items_with_names(self):
        """Получить товары магазина с названиями"""
        shop_items = self.db.get_shop_items()
        
        items_with_names = []
        for item in shop_items:
            seed_data = SEEDS[item['seed_type']]
            items_with_names.append({
                **item,
                'name': seed_data['name'],
                'growth_time': seed_data['growth_time']
            })
        
        return items_with_names
    
    def get_current_weather_info(self):
        """Получить информацию о текущей погоде"""
        weather = self.db.get_current_weather()
        
        if weather:
            weather_data = WEATHER_EFFECTS[weather['weather_type']]
            return {
                'type': weather['weather_type'],
                'name': weather_data['name'],
                'multiplier': weather['multiplier'],
                'growth_multiplier': weather_data['growth_multiplier'],
                'price_multiplier': weather_data['price_multiplier']
            }
        else:
            return {
                'type': 'normal',
                'name': 'Обычная погода',
                'multiplier': 1.0,
                'growth_multiplier': 1.0,
                'price_multiplier': 1.0
            }
