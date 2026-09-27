import json
import os
from datetime import datetime, timezone
from pathlib import Path

import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
DATA_FILE = Path(__file__).parent / "data" / "users.json"

if not TOKEN or not GUILD_ID:
    raise RuntimeError("Заполни DISCORD_TOKEN и GUILD_ID в файле .env")

GUILD = discord.Object(id=int(GUILD_ID))


def read_users():
    if not DATA_FILE.exists():
        return []

    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        print("Не удалось прочитать data/users.json. Используется пустой список.")
        return []


def save_users(users):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(users, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


class RegistrationBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)

    async def on_ready(self):
        print(f"Бот запущен: {self.user}")


bot = RegistrationBot()


@bot.tree.command(name="register", description="Зарегистрироваться в проекте")
async def register(interaction: discord.Interaction):
    users = read_users()

    if any(user["discord_id"] == interaction.user.id for user in users):
        await interaction.response.send_message(
            "Ты уже зарегистрирован.", ephemeral=True
        )
        return

    users.append(
        {
            "discord_id": interaction.user.id,
            "username": interaction.user.name,
            "registered_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    save_users(users)

    await interaction.response.send_message(
        "Регистрация прошла успешно!", ephemeral=True
    )


bot.run(TOKEN)