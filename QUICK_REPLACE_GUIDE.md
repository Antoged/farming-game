# 🚀 Полная замена старого проекта на antoged.github.io

## 🎯 Цель: Заменить старый проект на фермерскую игру

**Результат:** `https://antoged.github.io/` будет показывать вашу фермерскую игру

## 📋 Пошаговый план

### Шаг 1: Создайте резервную копию (опционально)

Если хотите сохранить старый проект:

1. Перейдите в репозиторий `antoged.github.io` на GitHub
2. Нажмите **Code** → **Download ZIP**
3. Сохраните архив как `old-project-backup.zip`

### Шаг 2: Очистите репозиторий

1. **Перейдите в репозиторий** `antoged.github.io` на GitHub
2. **Выделите все файлы** (Ctrl+A)
3. **Нажмите Delete** (корзина)
4. **Commit:** "feat: clean repository for new project"

### Шаг 3: Загрузите новый проект

1. **Нажмите "Upload files"**
2. **Перетащите ВСЕ файлы** из папки `D:\tgbots\farming`
3. **Commit:** "feat: add farming game project"

### Шаг 4: Настройте GitHub Pages

1. **Settings** → **Pages**
2. **Source:** Deploy from a branch
3. **Branch:** main
4. **Folder:** `/docs`
5. **Сохраните настройки**

## ⚡ Быстрый способ через Git (если установлен)

Если у вас есть Git, можете сделать так:

```bash
# 1. Перейдите в папку с проектом
cd D:\tgbots\farming

# 2. Клонируйте старый репозиторий
git clone https://github.com/antoged/antoged.github.io.git temp-old
cd temp-old

# 3. Удалите все файлы кроме .git
Get-ChildItem -Exclude .git | Remove-Item -Recurse -Force

# 4. Скопируйте новый проект
Copy-Item -Path "D:\tgbots\farming\*" -Destination "." -Recurse -Force

# 5. Добавьте все файлы
git add .
git commit -m "feat: replace with farming game project"
git push origin main

# 6. Очистите
cd ..
Remove-Item -Recurse -Force temp-old
```

## 🔧 Обновление конфигурации

После замены обновите файлы:

### 1. Создайте .env файл:

```env
BOT_TOKEN=your_bot_token_here
WEBAPP_URL=https://antoged.github.io/
DATABASE_PATH=farm_game.db
```

### 2. Обновите Menu Button в @BotFather:

1. Откройте @BotFather в Telegram
2. `/mybots` → выберите вашего бота
3. **Edit Bot** → **Menu Button**
4. **URL:** `https://antoged.github.io/`

## 🎉 Результат

После выполнения всех шагов:

- ✅ **Сайт:** `https://antoged.github.io/` будет показывать фермерскую игру
- ✅ **Бот:** Будет работать с новым веб-интерфейсом
- ✅ **Старый проект:** Полностью заменен

## 🚨 Если что-то пошло не так

### Проблема: Сайт не обновляется
**Решение:** Подождите 5-10 минут, GitHub Pages обновляется не мгновенно

### Проблема: Ошибка 404
**Решение:** Проверьте настройки Pages - папка должна быть `/docs`

### Проблема: Бот не работает
**Решение:** Проверьте .env файл и Menu Button URL

## 📞 Поддержка

Если нужна помощь с конкретным шагом - скажите, на каком этапе возникли сложности!

---

**Время выполнения:** 10-15 минут  
**Сложность:** Легко  
**Риск:** Минимальный (если сделали бэкап)


