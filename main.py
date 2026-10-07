import discord
from discord.ext import tasks
from playwright.sync_api import sync_playwright
from apify_client import ApifyClient
from curl_cffi import requests as curl_requests
import requests
import asyncio
import time

TOKEN = ''
APIFY_TOKEN = ''

CANALES = {
    "whowatch":  0,
    "tiktok":    0,
    "instagram": 0,
    "twitter":   0,
    "kick":      0,
}

WHOWATCH_ID = ''
TIKTOK_USER = ''
IG_USER = ''
X_USER = ''
KICK_USER = ''

WHOWATCH_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Mobile Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://whowatch.tv/",
    "Origin": "https://whowatch.tv",
    "X-Whowatch-Device-Id": ""
}

def format_num(num):
    if num is None: return "?"
    try:
        n = int(str(num).replace(',', '').replace('.', '').replace(' ', ''))
        if n == 0: return None
        if n >= 1000000:
            return f"{n/1000000:.1f}M".replace(".0M", "M")
        if n >= 1000:
            return f"{n/1000:.1f}K".replace(".0K", "K")
        return str(n)
    except:
        return str(num)

def ejecutar_ronda_scraping():
    data = {"whowatch": None, "tiktok": None, "instagram": None, "twitter": None, "kick": None}

    try:
        r = requests.get(f"https://api.whowatch.tv/users/{WHOWATCH_ID}/profile", headers=WHOWATCH_HEADERS, timeout=10)
        data["whowatch"] = format_num(r.json().get("follower_count"))
    except Exception as e:
        print(f" error Whowatch: {e}")

    try:
        apify = ApifyClient(APIFY_TOKEN)
        run = apify.actor("apify/instagram-followers-count-scraper").call(
            run_input={"usernames": [IG_USER]},
            memory_mbytes=256
        )
        items = apify.dataset(run.default_dataset_id).list_items().items
        if items:
            data["instagram"] = format_num(items[0].get("followersCount"))
    except Exception as e:
        print(f"error Instagram: {e}")

    try:
        r = curl_requests.get(
            f"https://kick.com/api/v1/channels/{KICK_USER}",
            impersonate="chrome",
            timeout=30
        )
        if r.status_code == 200:
            data["kick"] = format_num(r.json().get("followersCount"))
    except Exception as e:
        print(f"error Kick: {e}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                ]
            )

            try:
                page = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36").new_page()
                page.goto(f"https://www.tiktok.com/@{TIKTOK_USER}", wait_until="domcontentloaded", timeout=60000)
                page.wait_for_selector('[data-e2e="followers-count"]', timeout=20000)
                data["tiktok"] = page.inner_text('[data-e2e="followers-count"]')
                print(f"ok TikTok scrape: {data['tiktok']}")
                page.close()
            except Exception as e:
                print(f"error TikTok: {e}")

            time.sleep(10)

            try:
                page = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36").new_page()
                page.goto(f"https://x.com/{X_USER}", wait_until="domcontentloaded", timeout=60000)
                selector = f'a[href="/{X_USER}/verified_followers"]'
                page.wait_for_selector(selector, timeout=20000)
                count = page.locator(selector).inner_text().split('\n')[0].split(' ')[0]
                data["twitter"] = format_num(count)
                print(f"ok Twitter scrape: {data['twitter']}")
                page.close()
            except Exception as e:
                print(f"error Twitter: {e}")

            browser.close()
    except Exception as e:
        print(f" Error critico Playwright: {e}")

    return data

intents = discord.Intents.default()
intents.guilds = True
client = discord.Client(intents=intents)

@tasks.loop(minutes=15)
async def update_stats():
    print("\nIniciando...")
    loop = asyncio.get_event_loop()
    resultados = await loop.run_in_executor(None, ejecutar_ronda_scraping)
    nombres = {"whowatch": "Whowatch", "tiktok": "TikTok", "instagram": "IG", "twitter": "X", "kick": "Kick"}

    for key, valor in resultados.items():
        if valor and valor != "?":
            try:
                canal = client.get_channel(CANALES[key])
                if canal:
                    nuevo_nombre = f"{nombres[key]}: {valor}"
                    if canal.name != nuevo_nombre:
                        await canal.edit(name=nuevo_nombre)
                        print(f"ok {nombres[key]}: {valor}")
                    else:
                        print(f"info {nombres[key]} sin cambios")
                await asyncio.sleep(10)
            except Exception as e:
                print(f"error Canal {key}: {e}")

@client.event
async def on_ready():
    print(f" Bot online como {client.user}")
    if not update_stats.is_running():
        update_stats.start()

client.run(TOKEN)
