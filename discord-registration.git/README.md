# Discord Registration

Простой Discord-бот на Python с командой `/register`. После вызова команды пользователь сохраняется в `data/users.json`.

## Запуск локально

Нужен Python 3.9 или новее.

1. Создай приложение и бота в [Discord Developer Portal](https://discord.com/developers/applications).
2. Скопируй `.env.example` в `.env`.
3. Заполни в `.env`:
   - `DISCORD_TOKEN` — токен бота;
   - `GUILD_ID` — ID Discord-сервера для тестирования.
4. Пригласи бота на сервер со scopes `bot` и `applications.commands`.
5. Создай виртуальное окружение, установи зависимости и запусти:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python bot.py
```

На сервере появится команда `/register`.

## Публикация на GitHub

```bash
git init
git add .
git commit -m "Initial Discord registration bot"
git branch -M main
git remote add origin https://github.com/USERNAME/REPOSITORY.git
git push -u origin main
```

Файл `.env` и данные пользователей исключены из Git, поэтому токен и локальная база не попадут в репозиторий.