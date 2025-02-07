import re
import nest_asyncio
import asyncio
from flask import Flask, render_template, request
from telethon import TelegramClient
from datetime import datetime, timedelta
import threading

nest_asyncio.apply()

# Paramètres de configuration
API_ID = 22491096
API_HASH = "770f00ae81b7347f7b49a32522090219"
SESSION_NAME = "telegram_session"

app = Flask(__name__)

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
bot_thread = None
running = False  # Indicateur d'état du bot

async def bot_task():
    await client.start()
    print("✅ Bot en ligne !")
    while running:
        await asyncio.sleep(5)  # Simule une boucle de traitement
    await client.disconnect()
    print("❌ Bot arrêté.")

def start_bot():
    global bot_thread, running
    if not running:
        running = True
        bot_thread = threading.Thread(target=lambda: asyncio.run(bot_task()))
        bot_thread.start()

def stop_bot():
    global running
    running = False

@app.route("/")
def index():
    return f"""
    <h1>Bot Telegram</h1>
    <p>Status: {'En cours' if running else 'Arrêté'}</p>
    <form action="/start" method="post"><button type="submit">Démarrer</button></form>
    <form action="/stop" method="post"><button type="submit">Arrêter</button></form>
    """

@app.route("/start", methods=["POST"])
def start():
    start_bot()
    return index()

@app.route("/stop", methods=["POST"])
def stop():
    stop_bot()
    return index()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
