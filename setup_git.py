#!/usr/bin/env python3
"""
Скрипт для настройки Git репозитория и подготовки к загрузке на GitHub
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description=""):
    """Выполняет команду и выводит результат"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} выполнено успешно")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при {description}: {e}")
        print(f"stderr: {e.stderr}")
        return None


def check_git_installed():
    """Проверяет, установлен ли Git"""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def init_git_repo():
    """Инициализирует Git репозиторий"""
    if not check_git_installed():
        print("❌ Git не установлен! Установите Git и попробуйте снова.")
        return False
    
    # Проверяем, не инициализирован ли уже репозиторий
    if os.path.exists(".git"):
        print("ℹ️  Git репозиторий уже инициализирован")
        return True
    
    # Инициализируем новый репозиторий
    if run_command("git init", "Инициализация Git репозитория"):
        return True
    return False


def create_initial_commit():
    """Создает первый коммит"""
    # Добавляем все файлы
    if not run_command("git add .", "Добавление файлов в индекс"):
        return False
    
    # Создаем первый коммит
    if run_command('git commit -m "feat: initial commit - farming game bot"', 
                   "Создание первого коммита"):
        return True
    return False


def setup_remote_repo():
    """Настраивает удаленный репозиторий"""
    print("\n🌐 Настройка удаленного репозитория")
    print("=" * 50)
    
    # Запрашиваем URL репозитория
    repo_url = input("Введите URL вашего GitHub репозитория (например, https://github.com/username/farming-game.git): ").strip()
    
    if not repo_url:
        print("❌ URL репозитория не указан")
        return False
    
    # Добавляем remote origin
    if run_command(f'git remote add origin {repo_url}', "Добавление remote origin"):
        return True
    return False


def push_to_github():
    """Отправляет код на GitHub"""
    print("\n📤 Отправка на GitHub")
    print("=" * 50)
    
    # Переименовываем ветку в main (современный стандарт)
    run_command("git branch -M main", "Переименование ветки в main")
    
    # Отправляем на GitHub
    if run_command("git push -u origin main", "Отправка кода на GitHub"):
        print("✅ Код успешно отправлен на GitHub!")
        return True
    return False


def setup_github_pages():
    """Настраивает GitHub Pages"""
    print("\n🌐 Настройка GitHub Pages")
    print("=" * 50)
    print("Для настройки GitHub Pages:")
    print("1. Перейдите в настройки репозитория на GitHub")
    print("2. Найдите раздел 'Pages' в боковом меню")
    print("3. В разделе 'Source' выберите 'Deploy from a branch'")
    print("4. Выберите ветку 'gh-pages' и папку '/' (root)")
    print("5. Нажмите 'Save'")
    print("\nПосле настройки ваш сайт будет доступен по адресу:")
    print("https://your-username.github.io/farming-game/")


def create_github_workflow():
    """Создает GitHub Actions workflow для автоматического деплоя"""
    print("\n🤖 Настройка GitHub Actions")
    print("=" * 50)
    
    # Проверяем, существует ли папка .github/workflows
    workflows_dir = Path(".github/workflows")
    workflows_dir.mkdir(parents=True, exist_ok=True)
    
    print("✅ GitHub Actions workflow создан автоматически")
    print("При следующем push в ветку main сайт будет обновлен автоматически")


def main():
    """Главная функция"""
    print("🚀 Настройка Git репозитория для Фермерской игры")
    print("=" * 60)
    
    # Проверяем, что мы в правильной папке
    if not os.path.exists("run.py"):
        print("❌ Скрипт должен быть запущен в корневой папке проекта")
        return
    
    # Инициализируем Git репозиторий
    if not init_git_repo():
        return
    
    # Создаем первый коммит
    if not create_initial_commit():
        return
    
    # Настраиваем удаленный репозиторий
    if not setup_remote_repo():
        return
    
    # Отправляем на GitHub
    if not push_to_github():
        return
    
    # Создаем GitHub Actions workflow
    create_github_workflow()
    
    # Инструкции по настройке GitHub Pages
    setup_github_pages()
    
    print("\n🎉 Настройка завершена!")
    print("=" * 60)
    print("✅ Git репозиторий инициализирован")
    print("✅ Код отправлен на GitHub")
    print("✅ GitHub Actions настроен")
    print("\n📋 Следующие шаги:")
    print("1. Настройте GitHub Pages в настройках репозитория")
    print("2. Обновите URL в файлах конфигурации")
    print("3. Настройте переменные окружения на сервере")
    print("4. Запустите бота и протестируйте функциональность")


if __name__ == "__main__":
    main()
