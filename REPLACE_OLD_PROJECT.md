# 🔄 Замена старого проекта на antoged.github.io

Инструкция по замене вашего старого проекта на `antoged.github.io` новой фермерской игрой.

## 📋 Варианты действий

### Вариант 1: Полная замена (рекомендуется)
Заменить весь старый проект новым.

### Вариант 2: Сохранение старого проекта
Переместить старый проект в подпапку и сделать главной страницей новый проект.

### Вариант 3: Архивирование
Сохранить старый проект в отдельном репозитории.

## 🚀 Вариант 1: Полная замена

### Шаг 1: Создайте резервную копию старого проекта

```bash
# Клонируйте старый репозиторий для резервной копии
git clone https://github.com/antoged/antoged.github.io.git backup-old-project
cd backup-old-project
zip -r ../old-project-backup.zip .
```

### Шаг 2: Очистите старый репозиторий

1. Перейдите в репозиторий `antoged.github.io` на GitHub
2. **Settings** → прокрутите вниз → **Danger Zone**
3. **Delete this repository** (если хотите начать с нуля)

**ИЛИ** очистите содержимое:

```bash
# Клонируйте старый репозиторий
git clone https://github.com/antoged/antoged.github.io.git
cd antoged.github.io

# Удалите все файлы кроме .git
find . -not -path './.git*' -delete

# Скопируйте файлы нового проекта
cp -r /path/to/farming/* .

# Закоммитьте изменения
git add .
git commit -m "feat: replace with farming game project"
git push origin main
```

### Шаг 3: Обновите настройки GitHub Pages

1. **Settings** → **Pages**
2. **Source**: Deploy from a branch
3. **Branch**: main
4. **Folder**: / (root)
5. Сохраните настройки

## 🗂️ Вариант 2: Сохранение старого проекта

Если вы хотите сохранить доступ к старому проекту:

### Шаг 1: Переместите старый проект

```bash
# Клонируйте репозиторий
git clone https://github.com/antoged/antoged.github.io.git
cd antoged.github.io

# Создайте папку для старого проекта
mkdir old-project
mv * old-project/ 2>/dev/null || true
mv .* old-project/ 2>/dev/null || true

# Верните .git обратно
mv old-project/.git .

# Скопируйте новый проект
cp -r /path/to/farming/* .

# Обновите индексную страницу для навигации
```

### Шаг 2: Создайте навигацию

Создайте файл `index.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Проекты Antoged</title>
</head>
<body>
    <h1>Мои проекты</h1>
    <ul>
        <li><a href="/docs/">🌾 Фермерская игра (новая)</a></li>
        <li><a href="/old-project/">📁 Старый проект</a></li>
    </ul>
</body>
</html>
```

## 📦 Вариант 3: Архивирование в отдельный репозиторий

### Шаг 1: Создайте новый репозиторий для старого проекта

1. Создайте репозиторий `antoged-old-project` на GitHub
2. Переместите туда старый проект:

```bash
# Клонируйте старый проект
git clone https://github.com/antoged/antoged.github.io.git old-backup
cd old-backup

# Измените remote на новый репозиторий
git remote set-url origin https://github.com/antoged/antoged-old-project.git
git push -u origin main
```

### Шаг 2: Замените основной репозиторий

```bash
# Очистите основной репозиторий
git clone https://github.com/antoged/antoged.github.io.git
cd antoged.github.io

# Удалите все файлы
rm -rf * .*[!.git]*

# Скопируйте новый проект
cp -r /path/to/farming/* .

# Закоммитьте
git add .
git commit -m "feat: replace with farming game"
git push origin main
```

## 🔧 Обновление конфигурации

После замены обновите конфигурацию:

### 1. Обновите .env файл:

```env
BOT_TOKEN=your_bot_token_here
WEBAPP_URL=https://antoged.github.io/
DATABASE_PATH=farm_game.db
```

### 2. Обновите файлы проекта:

```bash
# Замените в env_example.txt
sed -i 's|https://your-custom-domain.com|https://antoged.github.io/|' env_example.txt

# Замените в docs/index.html
sed -i 's|YOUR_USERNAME|antoged|g' docs/index.html
```

### 3. Если используете docs/ папку:

GitHub Pages может служить файлы из:
- **Корня репозитория** (`/`)
- **Папки docs/** (`/docs`)

Если ваш проект в папке `docs/`, URL будет:
- `https://antoged.github.io/` (если настроить корень)
- `https://antoged.github.io/docs/` (если папка docs)

## ⚡ Быстрый способ

Если вы готовы полностью заменить старый проект:

```bash
# 1. Перейдите в папку с вашим новым проектом
cd /d/tgbots/farming

# 2. Клонируйте старый репозиторий во временную папку
git clone https://github.com/antoged/antoged.github.io.git temp-old-repo

# 3. Скопируйте .git папку
cp -r temp-old-repo/.git .

# 4. Удалите временную папку
rm -rf temp-old-repo

# 5. Добавьте все файлы нового проекта
git add .
git commit -m "feat: replace with farming game project"
git push origin main

# 6. Обновите URL в конфигурации
```

## 📞 Что выбрать?

### ✅ **Полная замена** - если:
- Старый проект больше не нужен
- Хотите чистый URL `antoged.github.io`
- Не планируете возвращаться к старому проекту

### ✅ **Сохранение в подпапке** - если:
- Хотите сохранить доступ к старому проекту
- Планируете несколько проектов на одном домене

### ✅ **Архивирование** - если:
- Старый проект важен для истории
- Хотите сохранить его в отдельном репозитории

## 🎯 Рекомендация

Я рекомендую **полную замену**, потому что:
- ✅ Чистый URL для фермерской игры
- ✅ Лучше для SEO и запоминания
- ✅ Проще в обслуживании
- ✅ Старый проект можно сохранить в архиве

Какой вариант вам больше подходит?
