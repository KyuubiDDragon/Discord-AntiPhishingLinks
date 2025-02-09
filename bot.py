import discord
from discord.ext import commands, tasks
import datetime
from zoneinfo import ZoneInfo
import re
from urllib.parse import urlparse
import requests

# 📌 Discord Bot Setup
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ─────────────────────────────────────────────
# Funktion: Überprüfung eines Links mittels Google Safe Browsing API
def is_url_safe(url: str) -> bool:
    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key=AIzaSyCujwFJlaH6JtHLenLBP7F64ngDA-22OEI"
    payload = {
        "client": {
            "clientId": "StreamUnity Bot",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION"
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }
    try:
        response = requests.post(endpoint, json=payload)
    except Exception as e:
        print(f"Fehler bei Google Safe Browsing Anfrage: {e}")
        # Im Fehlerfall gehen wir davon aus, dass der Link sicher ist.
        return True
    if response.status_code != 200:
        print(f"Google Safe Browsing API Fehler: {response.status_code}")
        return True  # Bei API-Fehlern nehmen wir an, dass der Link sicher ist.
    data = response.json()
    if "matches" in data:
        # Es gibt verdächtige Treffer
        return False
    return True

@bot.event
async def on_message(message):
    # Ignoriere Nachrichten von Bots
    if message.author.bot:
        return await bot.process_commands(message)
    
    # Prüfe alle URLs in der Nachricht
    urls = re.findall(r"(https?://[^\s]+)", message.content)
    if urls:
        for url in urls:
            if not is_url_safe(url):
                # Lösche die Nachricht, falls ein unsicherer Link gefunden wurde
                try:
                    await message.delete()
                    print(f"Nachricht von {message.author} mit unsicherem Link wurde gelöscht: {url}")
                except Exception as e:
                    print(f"Fehler beim Löschen der verdächtigen Nachricht: {e}")
                try:
                    await message.author.send("Deine Nachricht wurde gelöscht, da ein unsicherer (möglicherweise Phishing-) Link enthalten war.")
                except discord.Forbidden:
                    pass

                # Mute den Benutzer für 30 Minuten (Timeout), wenn die Nachricht in einem Server gesendet wurde
                if message.guild:
                    try:
                        mute_duration = datetime.timedelta(minutes=30)
                        mute_until = discord.utils.utcnow() + mute_duration
                        await message.author.edit(communication_disabled_until=mute_until)
                        try:
                            await message.author.send("Du wurdest für 30 Minuten stummgeschaltet, weil du einen unsicheren Link gepostet hast.")
                        except discord.Forbidden:
                            pass
                    except Exception as e:
                        print(f"Fehler beim Timeout für {message.author}: {e}")
                return  # Weitere Verarbeitung der Nachricht unterbinden

    
    # Andernfalls verarbeite Befehle normal
    await bot.process_commands(message)


@bot.event
async def on_ready():
    print(f"Eingeloggt als {bot.user}")


bot.run('KEY')
