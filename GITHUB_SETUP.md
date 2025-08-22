# 🚀 Настройка GitHub репозитория

Пошаговые инструкции по созданию GitHub репозитория и настройке GitHub Pages для Фермерской игры.

## 📋 Предварительные требования

1. **Установите Git:**
   - Windows: Скачайте с [git-scm.com](https://git-scm.com/download/win)
   - macOS: `brew install git`
   - Linux: `sudo apt install git`

2. **Создайте аккаунт на GitHub:**
   - Перейдите на [github.com](https://github.com)
   - Зарегистрируйтесь или войдите в аккаунт

## 🔧 Пошаговая настройка

### Шаг 1: Создание репозитория на GitHub

1. Перейдите на [GitHub](https://github.com)
2. Нажмите кнопку **"New"** или **"+"** → **"New repository"**
3. Заполните форму:
   - **Repository name:** `farming-game`
   - **Description:** `Интерактивная фермерская игра в Telegram с веб-интерфейсом`
   - **Visibility:** Public (или Private, если хотите)
   - ✅ **Add a README file**
   - ✅ **Add .gitignore** → Python
   - ✅ **Choose a license** → MIT License
4. Нажмите **"Create repository"**

### Шаг 2: Клонирование репозитория

```bash
# Откройте командную строку/терминал
# Перейдите в папку, где хотите разместить проект
cd /path/to/your/projects

# Клонируйте репозиторий
git clone https://github.com/YOUR_USERNAME/farming-game.git
cd farming-game
```

### Шаг 3: Копирование файлов проекта

Скопируйте все файлы из вашего проекта в клонированную папку:

```bash
# Скопируйте все файлы проекта
cp -r /path/to/your/farming/project/* .
```

### Шаг 4: Настройка Git

```bash
# Настройте ваше имя и email (если еще не настроено)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Добавьте все файлы в Git
git add .

# Создайте первый коммит
git commit -m "feat: initial commit - farming game bot"

# Отправьте изменения на GitHub
git push origin main
```

### Шаг 5: Настройка GitHub Pages

1. Перейдите в ваш репозиторий на GitHub
2. Нажмите **"Settings"** (вкладка с шестеренкой)
3. В левом меню найдите **"Pages"**
4. В разделе **"Source"** выберите:
   - **Deploy from a branch**
   - **Branch:** `gh-pages`
   - **Folder:** `/ (root)`
5. Нажмите **"Save"**

### Шаг 6: Настройка GitHub Actions

GitHub Actions уже настроен автоматически! При каждом push в ветку `main` сайт будет обновляться автоматически.

## 🔄 Обновление кода

После внесения изменений в код:

```bash
# Добавьте изменения
git add .

# Создайте коммит
git commit -m "feat: add new feature"

# Отправьте на GitHub
git push origin main
```

## 🌐 Настройка домена

### Вариант 1: GitHub Pages (бесплатно)

После настройки GitHub Pages ваш сайт будет доступен по адресу:
```
https://YOUR_USERNAME.github.io/farming-game/
```

### Вариант 2: Кастомный домен

1. Купите домен (например, на [Namecheap](https://namecheap.com))
2. В настройках GitHub Pages добавьте ваш домен
3. Настройте DNS записи у регистратора домена

## 📱 Настройка Telegram бота

### 1. Создание бота

1. Найдите @BotFather в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте токен бота

### 2. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
BOT_TOKEN=your_bot_token_here
WEBAPP_URL=https://YOUR_USERNAME.github.io/farming-game/
```

### 3. Настройка Menu Button

1. Отправьте @BotFather команду `/mybots`
2. Выберите вашего бота
3. Нажмите **"Bot Settings"** → **"Menu Button"**
4. Установите URL: `https://YOUR_USERNAME.github.io/farming-game/`

## 🧪 Тестирование

### 1. Локальное тестирование

```bash
# Установите зависимости
pip install -r requirements.txt

# Запустите приложение
python run.py
```

### 2. Тестирование в Telegram

1. Найдите вашего бота в Telegram
2. Отправьте команду `/start`
3. Нажмите кнопку "🌾 Играть в ферму"
4. Проверьте, что веб-интерфейс открывается

## 🔧 Полезные команды Git

```bash
# Проверка статуса
git status

# Просмотр истории коммитов
git log --oneline

# Создание новой ветки
git checkout -b feature/new-feature

# Переключение между ветками
git checkout main

# Слияние веток
git merge feature/new-feature

# Удаление ветки
git branch -d feature/new-feature
```

## 🚨 Устранение неполадок

### Проблема: "Git не найден"
**Решение:** Установите Git с [git-scm.com](https://git-scm.com/download/win)

### Проблема: "Permission denied"
**Решение:** 
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Проблема: "Repository not found"
**Решение:** Проверьте URL репозитория и права доступа

### Проблема: GitHub Pages не работает
**Решение:**
1. Проверьте настройки в Settings → Pages
2. Убедитесь, что ветка `gh-pages` существует
3. Проверьте логи в Actions

## 📊 Мониторинг

### GitHub Insights

В вашем репозитории доступны:
- **Traffic:** Просмотры и клоны
- **Contributors:** Участники проекта
- **Commits:** История изменений

### GitHub Actions

Проверьте статус деплоя:
1. Перейдите в репозиторий
2. Нажмите вкладку **"Actions"**
3. Просмотрите логи выполнения

## 🎯 Следующие шаги

После настройки:

1. **Обновите README.md** с вашими данными
2. **Добавьте описание** в репозитории
3. **Настройте Issues** и **Pull Requests**
4. **Добавьте метки** для Issues
5. **Настройте Wiki** (опционально)

## 📞 Поддержка

Если возникли проблемы:

1. Проверьте [GitHub Help](https://help.github.com/)
2. Создайте Issue в репозитории
3. Обратитесь в [GitHub Community](https://github.community/)

---

**Удачной разработки! 🚀**
