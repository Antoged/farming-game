"""
Тесты для игровой логики
"""

import pytest
import time
from unittest.mock import Mock, patch
import sys
import os

# Добавляем корневую папку в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_logic import GameLogic


class TestGameLogic:
    """Тесты для класса GameLogic"""
    
    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.game = GameLogic()
        self.user_id = 12345
        
    def test_init_user(self):
        """Тест инициализации пользователя"""
        result = self.game.init_user(self.user_id)
        assert result['success'] is True
        assert 'user_id' in result
        assert result['user_id'] == self.user_id
        
    def test_get_farm_status(self):
        """Тест получения статуса фермы"""
        # Сначала инициализируем пользователя
        self.game.init_user(self.user_id)
        
        result = self.game.get_farm_status(self.user_id)
        assert result['success'] is True
        assert 'plots' in result
        assert len(result['plots']) == 9
        
    def test_plant_seed(self):
        """Тест посадки семечка"""
        # Инициализируем пользователя
        self.game.init_user(self.user_id)
        
        # Тестируем посадку на пустой участок
        result = self.game.plant_seed(self.user_id, 0, "carrot")
        assert result['success'] is True
        assert result['plot'] == 0
        assert result['seed'] == "carrot"
        
    def test_plant_seed_invalid_plot(self):
        """Тест посадки на несуществующий участок"""
        self.game.init_user(self.user_id)
        
        result = self.game.plant_seed(self.user_id, 10, "carrot")
        assert result['success'] is False
        assert 'error' in result
        
    def test_plant_seed_occupied_plot(self):
        """Тест посадки на занятый участок"""
        self.game.init_user(self.user_id)
        
        # Сажаем первое семечко
        self.game.plant_seed(self.user_id, 0, "carrot")
        
        # Пытаемся посадить еще одно на тот же участок
        result = self.game.plant_seed(self.user_id, 0, "potato")
        assert result['success'] is False
        assert 'error' in result
        
    def test_harvest_crop(self):
        """Тест сбора урожая"""
        self.game.init_user(self.user_id)
        
        # Сажаем семечко
        self.game.plant_seed(self.user_id, 0, "carrot")
        
        # Мокаем время, чтобы урожай был готов
        with patch('time.time') as mock_time:
            mock_time.return_value = time.time() + 70  # Больше времени роста моркови
            
            result = self.game.harvest_crop(self.user_id, 0)
            assert result['success'] is True
            assert 'harvest' in result
            assert result['plot'] == 0
            
    def test_harvest_crop_not_ready(self):
        """Тест сбора неготового урожая"""
        self.game.init_user(self.user_id)
        
        # Сажаем семечко
        self.game.plant_seed(self.user_id, 0, "carrot")
        
        # Пытаемся собрать сразу
        result = self.game.harvest_crop(self.user_id, 0)
        assert result['success'] is False
        assert 'error' in result
        
    def test_harvest_empty_plot(self):
        """Тест сбора с пустого участка"""
        self.game.init_user(self.user_id)
        
        result = self.game.harvest_crop(self.user_id, 0)
        assert result['success'] is False
        assert 'error' in result
        
    def test_get_shop_items(self):
        """Тест получения товаров магазина"""
        result = self.game.get_shop_items()
        assert result['success'] is True
        assert 'items' in result
        assert len(result['items']) > 0
        
    def test_buy_seed(self):
        """Тест покупки семечка"""
        self.game.init_user(self.user_id)
        
        # Получаем товары магазина
        shop_items = self.game.get_shop_items()
        if shop_items['items']:
            seed_name = shop_items['items'][0]['name']
            
            result = self.game.buy_seed(self.user_id, seed_name)
            assert result['success'] is True
            assert result['seed'] == seed_name
            
    def test_buy_seed_not_in_shop(self):
        """Тест покупки семечка, которого нет в магазине"""
        self.game.init_user(self.user_id)
        
        result = self.game.buy_seed(self.user_id, "nonexistent_seed")
        assert result['success'] is False
        assert 'error' in result
        
    def test_get_user_stats(self):
        """Тест получения статистики пользователя"""
        self.game.init_user(self.user_id)
        
        result = self.game.get_user_stats(self.user_id)
        assert result['success'] is True
        assert 'stats' in result
        assert 'total_harvests' in result['stats']
        assert 'total_earnings' in result['stats']
        
    def test_get_weather(self):
        """Тест получения информации о погоде"""
        result = self.game.get_weather()
        assert result['success'] is True
        assert 'weather' in result
        assert 'condition' in result['weather']
        assert 'multiplier' in result['weather']
        
    def test_invalid_user_id(self):
        """Тест работы с несуществующим пользователем"""
        result = self.game.get_farm_status(99999)
        assert result['success'] is False
        assert 'error' in result


if __name__ == "__main__":
    pytest.main([__file__])
