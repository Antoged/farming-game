import sqlite3
import json
from datetime import datetime
import threading

class Database:
    def __init__(self, db_path='farm_game.db'):
        self.db_path = db_path
        self.lock = threading.Lock()
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Таблица игроков
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    money INTEGER DEFAULT 100,
                    experience INTEGER DEFAULT 0,
                    level INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Таблица фермы (посаженные культуры)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS farm_plots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    plot_id INTEGER,
                    seed_type TEXT,
                    planted_at TIMESTAMP,
                    growth_time INTEGER,
                    status TEXT DEFAULT 'empty',
                    FOREIGN KEY (user_id) REFERENCES players (user_id)
                )
            ''')
            
            # Таблица инвентаря (собранные плоды)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    item_type TEXT,
                    weight REAL,
                    size REAL,
                    quality REAL,
                    price INTEGER,
                    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES players (user_id)
                )
            ''')
            
            # Таблица магазина
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS shop_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    seed_type TEXT,
                    price INTEGER,
                    available_until TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Таблица погоды
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weather (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    weather_type TEXT,
                    multiplier REAL,
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ends_at TIMESTAMP
                )
            ''')
            
            # Создать участки фермы для каждого игрока (если их нет)
            cursor.execute('SELECT DISTINCT user_id FROM players')
            players = cursor.fetchall()
            
            for player in players:
                user_id = player[0]
                # Проверить, есть ли уже участки для этого игрока
                cursor.execute('SELECT COUNT(*) FROM farm_plots WHERE user_id = ?', (user_id,))
                plot_count = cursor.fetchone()[0]
                
                if plot_count == 0:
                    # Создать 6 участков для игрока
                    for plot_id in range(1, 7):
                        cursor.execute('''
                            INSERT INTO farm_plots (user_id, plot_id, status)
                            VALUES (?, ?, 'empty')
                        ''', (user_id, plot_id))
            
            conn.commit()
            conn.close()
    
    def get_or_create_player(self, user_id, username=None):
        """Получить или создать игрока"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM players WHERE user_id = ?
            ''', (user_id,))
            
            player = cursor.fetchone()
            
            if not player:
                cursor.execute('''
                    INSERT INTO players (user_id, username, money, experience, level)
                    VALUES (?, ?, 100, 0, 1)
                ''', (user_id, username))
                
                # Создать участки фермы для нового игрока
                for plot_id in range(1, 7):
                    cursor.execute('''
                        INSERT INTO farm_plots (user_id, plot_id, status)
                        VALUES (?, ?, 'empty')
                    ''', (user_id, plot_id))
                
                conn.commit()
                conn.close()
                
                # Получить созданного игрока
                return self.get_or_create_player(user_id, username)
            
            conn.close()
            
            return {
                'user_id': player[0],
                'username': player[1],
                'money': player[2],
                'experience': player[3],
                'level': player[4],
                'created_at': player[5],
                'last_active': player[6]
            }
    
    def update_player_money(self, user_id, amount):
        """Обновить деньги игрока"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE players SET money = money + ?, last_active = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (amount, user_id))
            
            conn.commit()
            conn.close()
    
    def get_farm_plots(self, user_id):
        """Получить участки фермы игрока"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM farm_plots WHERE user_id = ? ORDER BY plot_id
            ''', (user_id,))
            
            plots = cursor.fetchall()
            conn.close()
            
            return [{
                'id': plot[0],
                'user_id': plot[1],
                'plot_id': plot[2],
                'seed_type': plot[3],
                'planted_at': plot[4],
                'growth_time': plot[5],
                'status': plot[6]
            } for plot in plots]
    
    def plant_seed(self, user_id, plot_id, seed_type, growth_time):
        """Посадить семечко на участок"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Проверить, что участок свободен
            cursor.execute('''
                SELECT status FROM farm_plots 
                WHERE user_id = ? AND plot_id = ?
            ''', (user_id, plot_id))
            
            plot = cursor.fetchone()
            if not plot:
                # Создать участок, если его нет
                cursor.execute('''
                    INSERT INTO farm_plots (user_id, plot_id, seed_type, planted_at, growth_time, status)
                    VALUES (?, ?, ?, ?, ?, 'planted')
                ''', (user_id, plot_id, seed_type, datetime.now(), growth_time))
                conn.commit()
                conn.close()
                return True, "Семечко посажено"
            elif plot[0] == 'empty':
                # Посадить на свободный участок
                cursor.execute('''
                    UPDATE farm_plots 
                    SET seed_type = ?, planted_at = ?, growth_time = ?, status = 'planted'
                    WHERE user_id = ? AND plot_id = ?
                ''', (seed_type, datetime.now(), growth_time, user_id, plot_id))
                conn.commit()
                conn.close()
                return True, "Семечко посажено"
            else:
                conn.close()
                return False, "Участок уже занят"
    
    def harvest_plot(self, plot_id):
        """Собрать урожай с участка"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Получить информацию об участке
            cursor.execute('''
                SELECT user_id, seed_type FROM farm_plots 
                WHERE id = ? AND status = 'ready'
            ''', (plot_id,))
            
            plot = cursor.fetchone()
            if not plot:
                conn.close()
                return False, "Участок не готов к сбору"
            
            user_id, seed_type = plot
            
            # Очистить участок
            cursor.execute('''
                UPDATE farm_plots 
                SET seed_type = NULL, planted_at = NULL, growth_time = NULL, status = 'empty'
                WHERE id = ?
            ''', (plot_id,))
            
            conn.commit()
            conn.close()
            return True, f"Урожай собран с участка {plot_id}"
    
    def add_to_inventory(self, user_id, item_type, weight, size, quality, price):
        """Добавить предмет в инвентарь"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO inventory (user_id, item_type, weight, size, quality, price)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, item_type, weight, size, quality, price))
            
            conn.commit()
            conn.close()
    
    def get_inventory(self, user_id):
        """Получить инвентарь игрока"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM inventory WHERE user_id = ? ORDER BY collected_at DESC
            ''', (user_id,))
            
            items = cursor.fetchall()
            conn.close()
            
            return [{
                'id': item[0],
                'user_id': item[1],
                'item_type': item[2],
                'weight': item[3],
                'size': item[4],
                'quality': item[5],
                'price': item[6],
                'collected_at': item[7]
            } for item in items]
    
    def sell_item(self, item_id):
        """Продать предмет из инвентаря"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT user_id, price FROM inventory WHERE id = ?
            ''', (item_id,))
            
            item = cursor.fetchone()
            if item:
                user_id, price = item
                
                cursor.execute('''
                    DELETE FROM inventory WHERE id = ?
                ''', (item_id,))
                
                cursor.execute('''
                    UPDATE players SET money = money + ? WHERE user_id = ?
                ''', (price, user_id))
                
                conn.commit()
                conn.close()
                return price
            
            conn.close()
            return 0
    
    def get_shop_items(self):
        """Получить товары в магазине"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM shop_items WHERE available_until > CURRENT_TIMESTAMP
            ''')
            
            items = cursor.fetchall()
            conn.close()
            
            return [{
                'id': item[0],
                'seed_type': item[1],
                'price': item[2],
                'available_until': item[3],
                'created_at': item[4]
            } for item in items]
    
    def add_shop_item(self, seed_type, price, available_until):
        """Добавить товар в магазин"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO shop_items (seed_type, price, available_until)
                VALUES (?, ?, ?)
            ''', (seed_type, price, available_until))
            
            conn.commit()
            conn.close()
    
    def clear_expired_shop_items(self):
        """Очистить просроченные товары из магазина"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM shop_items WHERE available_until <= CURRENT_TIMESTAMP
            ''')
            
            conn.commit()
            conn.close()
    
    def get_current_weather(self):
        """Получить текущую погоду"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM weather WHERE ends_at > CURRENT_TIMESTAMP ORDER BY started_at DESC LIMIT 1
            ''')
            
            weather = cursor.fetchone()
            conn.close()
            
            if weather:
                return {
                    'id': weather[0],
                    'weather_type': weather[1],
                    'multiplier': weather[2],
                    'started_at': weather[3],
                    'ends_at': weather[4]
                }
            return None
    
    def set_weather(self, weather_type, multiplier, ends_at):
        """Установить погоду"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO weather (weather_type, multiplier, ends_at)
                VALUES (?, ?, ?)
            ''', (weather_type, multiplier, ends_at))
            
            conn.commit()
            conn.close()

    def buy_seed(self, user_id, seed_type, price):
        """Купить семечко"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Проверить, есть ли у игрока деньги
            cursor.execute('SELECT money FROM players WHERE user_id = ?', (user_id,))
            player = cursor.fetchone()
            
            if not player or player[0] < price:
                conn.close()
                return False
            
            # Списать деньги
            cursor.execute('''
                UPDATE players SET money = money - ? WHERE user_id = ?
            ''', (price, user_id))
            
            # Удалить товар из магазина
            cursor.execute('''
                DELETE FROM shop_items 
                WHERE seed_type = ? AND price = ? 
                LIMIT 1
            ''', (seed_type, price))
            
            conn.commit()
            conn.close()
            return True

    def update_plot_status(self, plot_id, status):
        """Обновить статус участка"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE farm_plots SET status = ? WHERE id = ?
            ''', (status, plot_id))
            
            conn.commit()
            conn.close()
