#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from database import Database

def reset_database():
    """Сброс базы данных"""
    print("🗑️ Сброс базы данных...")
    
    # Удалить файл базы данных
    db_file = 'farm_game.db'
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"✅ Удален файл {db_file}")
    
    # Создать новую базу данных
    db = Database()
    print("✅ Создана новая база данных")
    
    print("🎉 База данных сброшена!")

if __name__ == '__main__':
    reset_database()
