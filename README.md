<h1 align="center">tallybrew</h1>

<p align="center">
  A Discord bot that brews your follower counts like a fresh cup of coffee<br/>
  and serves them right in your channel names.
</p>

<p align="center">
    <a href="https://github.com/hypeblock26/tallybrew/stargazers"><img src="https://img.shields.io/github/stars/hypeblock26/tallybrew?colorA=363a4f&colorB=f5a97f&style=for-the-badge"></a>
    <a href="https://github.com/hypeblock26/tallybrew/forks"><img src="https://img.shields.io/github/forks/hypeblock26/tallybrew?colorA=363a4f&colorB=b7bdf8&style=for-the-badge"></a>
    <a href="https://github.com/hypeblock26/tallybrew/issues"><img src="https://img.shields.io/github/issues/hypeblock26/tallybrew?colorA=363a4f&colorB=ed8796&style=for-the-badge"></a>
    <a href="https://github.com/hypeblock26/tallybrew/commits/main"><img src="https://img.shields.io/github/last-commit/hypeblock26/tallybrew?colorA=363a4f&colorB=a6da95&style=for-the-badge"></a>
</p>

<p align="center">
    <img src="https://img.shields.io/badge/python-3.8%2B-f5a97f?colorA=363a4f&style=for-the-badge&logo=python&logoColor=f5a97f">
    <img src="https://img.shields.io/badge/discord.py-bot-b7bdf8?colorA=363a4f&style=for-the-badge&logo=discord&logoColor=b7bdf8">
    <img src="https://img.shields.io/badge/playwright-scraping-a6da95?colorA=363a4f&style=for-the-badge">
</p>

---

## What is this

Tallybrew checks how many followers you have on your social networks every 15 minutes and renames a few channels in your Discord server to show those numbers. Anyone who joins your server sees your stats at a glance, and you never have to type anything.

This is how the channels look:

```
Whowatch: 12.4K
TikTok: 85K
IG: 3.2K
X: 1.1K
Kick: 540
```

Supported platforms:

| Platform | How it gets the data |
|---|---|
| Whowatch | Whowatch public API |
| TikTok | Automated browser (Playwright) |
| Instagram | Apify service |
| X (Twitter) | Automated browser (Playwright) |
| Kick | Kick API through curl_cffi |

You do not have to use all 5. If you do not want one, just leave its channel ID at `0` (see the configuration section).

---

## Before you start

You need:

1. **Python 3.8 or higher.** Check with `python --version`.
2. **Git** to clone the repo.
3. **A Discord bot** and its token (explained below).
4. **An Apify account** and its token, only if you want Instagram.
5. **A Discord server** where you have admin permissions.

---

## Step-by-step installation

### 1. Clone the repository

```
git clone https://github.com/hypeblock26/tallybrew.git
cd tallybrew
```

### 2. Install the dependencies

```
pip install -r requirements.txt
```

### 3. Install the Playwright browser

This step is mandatory. Playwright needs to download its own Chromium to read TikTok and X. Without it, those two platforms fail.

```
playwright install chromium
```

If you are running it on a Linux server with no screen and you get missing library errors, also run:

```
playwright install-deps chromium
```

---

## Creating the Discord bot

1. Go to <https://discord.com/developers/applications> and click **New Application**.
2. Name it whatever you want and open the **Bot** tab.
3. Click **Reset Token** and copy the token. Save it, because Discord will not show it again.
4. You do not need to enable any Privileged Gateway Intent. The bot only uses the guilds intent, which is on by default.
5. Go to **OAuth2 → URL Generator**:
   - Under **Scopes**, check `bot`.
   - Under **Bot Permissions**, check `Manage Channels` and `View Channels`.
6. Copy the generated URL at the bottom, open it in your browser, and add the bot to your server.

---

## Configuration

Open `main.py` and fill in the variables at the top of the file.

### Tokens

```python
TOKEN = ''
APIFY_TOKEN = ''
```

- `TOKEN`: your Discord bot token, the one you copied above.
- `APIFY_TOKEN`: your Apify token. You can get it at <https://console.apify.com> under **Settings → API & Integrations**. It is only needed for Instagram.

### Discord channels

```python
CANALES = {
    "whowatch":  0,
    "tiktok":    0,
    "instagram": 0,
    "twitter":   0,
    "kick":      0,
}
```

These are the IDs of the channels the bot will rename. The easiest way is to create **voice channels** and remove the connect permission from `@everyone`, so they work as a stats panel.

To get a channel ID:

1. In Discord, go to **User Settings → Advanced** and turn on **Developer Mode**.
2. Right-click the channel and choose **Copy Channel ID**.
3. Paste the number into the dictionary, without quotes.

If you do not want a platform, leave its ID at `0` and the bot will skip that channel.

### Usernames for each platform

```python
WHOWATCH_ID = ''
TIKTOK_USER = ''
IG_USER = ''
X_USER = ''
KICK_USER = ''
```

| Variable | What to put | Example |
|---|---|---|
| `WHOWATCH_ID` | The numeric user ID on Whowatch | `'12345678'` |
| `TIKTOK_USER` | TikTok username without the @ | `'yourusername'` |
| `IG_USER` | Instagram username without the @ | `'yourusername'` |
| `X_USER` | X username without the @ | `'yourusername'` |
| `KICK_USER` | Kick username | `'yourusername'` |

Everything goes inside single quotes, including the Whowatch ID.

### Whowatch header

```python
"X-Whowatch-Device-Id": ""
```

Put any text with this format, for example `"1700000000000-12345678"`. It does not have to be a real one, it just must not be empty.

---

## Running the bot

```
python main.py
```

If everything is fine, you will see this in the console:

```
[INFO] Bot online como YourBot#1234

[INFO] Iniciando...
[OK] TikTok scrape: 85K
[OK] Twitter scrape: 1.1K
[OK] Whowatch: 12.4K
```

The first round starts as soon as the bot connects, and then repeats every 15 minutes.

### Keeping it running 24/7

If you close the terminal, the bot stops. To keep it alive on a Linux server you have a few options:

- **screen** or **tmux**, the simplest:
  ```
  screen -S tallybrew
  python main.py
  ```
  Detach with `Ctrl + A` and then `D`. To come back: `screen -r tallybrew`.
- **pm2**:
  ```
  pm2 start main.py --interpreter python3 --name tallybrew
  ```
- **systemd**, if you want it to start automatically when the machine boots.

---

## How it works

1. Every 15 minutes it runs a scraping round in a separate thread, so the bot is never blocked.
2. It queries each platform with the method listed in the table above.
3. It converts the numbers to a short format: `1500` becomes `1.5K` and `2000000` becomes `2M`.
4. If the number changed, it renames the channel. If not, it does nothing, to avoid wasting Discord's rate limit.
5. It waits 10 seconds between each channel so it does not hit Discord's rate limit.

---

## Changing the channel names

In the `update_stats` function there is a dictionary with the labels:

```python
nombres = {"whowatch": "Whowatch", "tiktok": "TikTok", "instagram": "IG", "twitter": "X", "kick": "Kick"}
```

Change the text on the right to whatever you want. For example, if you set `"tiktok": "TT Followers"`, the channel will be named `TT Followers: 85K`.

---

## Common problems

**The bot starts but the channels do not change.**
Check that the bot has the `Manage Channels` permission and that its role is above the channels you want it to edit. Also confirm that you pasted the IDs correctly.

**`playwright._impl._errors.Error: Executable doesn't exist`**
You forgot to run `playwright install chromium`.

**TikTok or X fail with a timeout error.**
These sites change their pages often and sometimes block scraping. Try again later. If it always fails, they probably changed the HTML selector and it needs to be updated in the code.

**Instagram does not update.**
Check that your `APIFY_TOKEN` is correct and that you have credits left in your Apify account. Also make sure you have `apify-client` version 2.0.0 or higher.

**Kick throws an error or returns nothing.**
Kick has anti-bot protection. The bot uses `curl_cffi` to imitate a real browser, but it can still get blocked sometimes. Try again later.

**A channel keeps the old name.**
Discord limits channel renames to 2 every 10 minutes. The bot already waits between changes, but if you restart it many times in a row it can hit that limit.

---

## Security

- **Never push your real tokens to GitHub.** If you put your `TOKEN` or `APIFY_TOKEN` in `main.py` and commit it, anyone who sees the repo can use them.
- If you push a token by mistake, regenerate it immediately in the Discord developer portal or the Apify console. Deleting the commit is not enough, because the token stays in the git history.
- Before every push, check with `git diff` that the variables are still empty.

---

## Disclaimer

This project gets public data from social networks through scraping and unofficial APIs. Those platforms can change or block these methods at any time, and scraping may go against their terms of service. Use it at your own risk.

---

## Contributing

If you find a bug or have an idea, open an [issue](https://github.com/hypeblock26/tallybrew/issues) or send a pull request.
