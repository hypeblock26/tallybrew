
<h1 align="center">tallybrew</h1>

<p align="center">
  A Discord bot that brews your follower counts<br/>
  and serves them right in your channel names.
</p>

<p align="center">
    <a href="https://github.com/hypeblock26/tallybrew/stargazers"><img src="https://img.shields.io/github/stars/hypeblock26/tallybrew?colorA=363a4f&colorB=f5a97f&style=for-the-badge"></a>
    <a href="https://github.com/hypeblock26/tallybrew/forks"><img src="https://img.shields.io/github/forks/hypeblock26/tallybrew?colorA=363a4f&colorB=b7bdf8&style=for-the-badge"></a>
    <a href="https://github.com/hypeblock26/tallybrew/issues"><img src="https://img.shields.io/github/issues/hypeblock26/tallybrew?colorA=363a4f&colorB=ed8796&style=for-the-badge"></a>
   <a href="https://github.com/hypeblock26/tallybrew/blob/main/LICENSE"><img src="https://img.shields.io/github/license/hypeblock26/tallybrew?colorA=363a4f&colorB=f5bde6&style=for-the-badge&v=2"></a>

</p>

<p align="center">
    <img src="https://img.shields.io/badge/python-3.8%2B-f5a97f?colorA=363a4f&style=for-the-badge&logo=python&logoColor=f5a97f">
    <img src="https://img.shields.io/badge/discord.py-bot-b7bdf8?colorA=363a4f&style=for-the-badge&logo=discord&logoColor=b7bdf8">
    <img src="https://img.shields.io/badge/playwright-scraping-a6da95?colorA=363a4f&style=for-the-badge">
</p>

<p align="center">
  <a href="#installation">Installation</a> &nbsp;/&nbsp;
  <a href="#configuration">Configuration</a> &nbsp;/&nbsp;
  <a href="#running-the-bot">Run it</a> &nbsp;/&nbsp;
  <a href="#customization">Customize</a> &nbsp;/&nbsp;
  <a href="#troubleshooting">Troubleshooting</a> &nbsp;/&nbsp;
  <a href="#faq">FAQ</a>
</p>

---

## Table of contents

- [What is this](#what-is-this)
- [Features](#features)
- [Supported platforms](#supported-platforms)
- [Requirements](#requirements)
- [Installation](#installation)
- [Creating the Discord bot](#creating-the-discord-bot)
- [Setting up the Discord channels](#setting-up-the-discord-channels)
- [Configuration](#configuration)
- [Running the bot](#running-the-bot)
- [Keeping it running 24/7](#keeping-it-running-247)
- [How it works](#how-it-works)
- [Customization](#customization)
- [Project structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Disclaimer](#disclaimer)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)

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

The whole bot is a single Python file. There is no database, no web panel and no slash commands to learn. You fill in a few variables, run it, and it keeps your channels up to date.

---

## Features

- Follower counts for 5 platforms in one bot.
- Counts are shown right in the channel names, so nobody has to run a command.
- Short number format: `1500` becomes `1.5K` and `2000000` becomes `2M`.
- Renames a channel only when the number actually changed, which saves Discord's rate limit.
- Scraping runs in a separate thread, so the bot never freezes.
- Updates every 15 minutes, and the interval is easy to change.
- Works on Windows, macOS and Linux.
- Only needs the basic guilds intent. No privileged intents.

---

## Supported platforms

| Platform | How it gets the data | Needs an extra account |
|---|---|---|
| Whowatch | Whowatch public API | No |
| TikTok | Automated browser (Playwright) | No |
| Instagram | Apify service | Yes, an Apify account |
| X (Twitter) | Automated browser (Playwright) | No |
| Kick | Kick API through curl_cffi | No |

You can run it with only the platforms you care about. See [Customization](#customization) for how to remove the ones you do not use.

---

## Requirements

| Requirement | Details |
|---|---|
| Python | 3.8 or higher. Check with `python --version`. |
| Git | To clone the repo. |
| Discord bot | A bot application and its token (explained below). |
| Discord server | A server where you can manage channels. |
| Apify account | Only if you want Instagram. |
| Disk and memory | Playwright downloads its own Chromium, so leave some free disk space and at least 1 GB of free RAM. |
| Internet | The bot has to reach Discord and each platform. |

Python packages (installed for you from `requirements.txt`):

```
discord.py
playwright
apify-client>=2.0.0
curl_cffi
requests
```

---

## Installation

### 1. Clone the repository

```
git clone https://github.com/hypeblock26/tallybrew.git
cd tallybrew
```

### 2. Create a virtual environment (recommended)

A virtual environment keeps the bot's packages separate from the rest of your system.

Windows:

```
python -m venv venv
venv\Scripts\activate
```

Linux and macOS:

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the dependencies

```
pip install -r requirements.txt
```

### 4. Install the Playwright browser

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
3. Click **Reset Token** and copy the token. Save it somewhere, because Discord will not show it again.
4. You do not need to enable any Privileged Gateway Intent. The bot only uses the guilds intent, which is on by default.
5. Go to **OAuth2, URL Generator**:
   - Under **Scopes**, check `bot`.
   - Under **Bot Permissions**, check `Manage Channels` and `View Channels`.
6. Copy the generated URL at the bottom, open it in your browser, pick your server and authorize.

You can also build the invite link by hand. Replace `YOUR_CLIENT_ID` with the **Application ID** from the **General Information** tab:

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot&permissions=1040
```

The number `1040` is `Manage Channels` plus `View Channels`, which is everything the bot needs.

---

## Setting up the Discord channels

The bot renames channels, so you need to create the channels first. The cleanest setup is a small stats panel made of voice channels.

1. Create a category, for example `Stats`.
2. Inside it, create one **voice channel** per platform you want. Any name works, the bot will rename them.
3. For each channel, open **Edit Channel, Permissions** and, for `@everyone`, deny **Connect** while leaving **View Channel** allowed. This way everybody can see the numbers but nobody can join the channel.
4. Make sure the bot can see the category and has **Manage Channels** on it.
5. Copy each channel's ID:
   1. In Discord, go to **User Settings, Advanced** and turn on **Developer Mode**.
   2. Right-click the channel and choose **Copy Channel ID**.

Text channels also work, but remember that Discord turns spaces in text channel names into dashes and lowercases everything, so `TikTok: 85K` would look different. Voice channels keep the name exactly as the bot writes it.

---

## Configuration

Open `main.py` and fill in the variables at the top of the file.

### Tokens

```python
TOKEN = ''
APIFY_TOKEN = ''
```

- `TOKEN`: your Discord bot token, the one you copied when creating the bot.
- `APIFY_TOKEN`: your Apify token. You can get it at <https://console.apify.com> under **Settings, API & Integrations**. It is only needed for Instagram.

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

Paste the channel IDs you copied, as plain numbers without quotes.

Leaving an ID at `0` stops the bot from renaming that channel, but the bot **still scrapes that platform**. If you do not want a platform at all, remove it completely (see [Removing a platform](#removing-a-platform)), especially Instagram, since every Apify run uses credits.

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
| `WHOWATCH_ID` | The numeric user ID on Whowatch, the number the Whowatch API uses in `/users/<id>/profile` | `'12345678'` |
| `TIKTOK_USER` | TikTok username without the @ | `'yourusername'` |
| `IG_USER` | Instagram username without the @ | `'yourusername'` |
| `X_USER` | X username without the @ | `'yourusername'` |
| `KICK_USER` | Kick username, as it appears in your channel URL | `'yourusername'` |

Everything goes inside single quotes, including the Whowatch ID.

### Whowatch header

```python
"X-Whowatch-Device-Id": ""
```

Put any text with this format, for example `"1700000000000-12345678"`. It does not have to be a real one, it just must not be empty.

### A complete example

```python
TOKEN = 'your-discord-bot-token'
APIFY_TOKEN = 'your-apify-token'

CANALES = {
    "whowatch":  111111111111111111,
    "tiktok":    222222222222222222,
    "instagram": 333333333333333333,
    "twitter":   444444444444444444,
    "kick":      555555555555555555,
}

WHOWATCH_ID = '12345678'
TIKTOK_USER = 'yourusername'
IG_USER = 'yourusername'
X_USER = 'yourusername'
KICK_USER = 'yourusername'
```

---

## Running the bot

```
python main.py
```

If everything is fine, you will see something like this in the console:

```
Bot online como YourBot#1234

Iniciando...
[OK] TikTok scrape: 85K
[OK] Twitter scrape: 1.1K
ok Whowatch: 12.4K
ok TikTok: 85K
ok X: 1.1K
```

The log messages are in Spanish, but they are easy to follow: `ok` means a channel was renamed, `info ... sin cambios` means the number did not change, and `error` shows what failed.

The first round starts as soon as the bot connects. A full round can take around a minute, because it starts a browser, waits between the TikTok and X checks and waits for the Apify run. After that, it repeats every 15 minutes.

To stop the bot, press `Ctrl + C` in the terminal.

---

## Keeping it running 24/7

If you close the terminal, the bot stops. To keep it alive on a server you have several options.

### screen or tmux

The simplest way on Linux:

```
screen -S tallybrew
python main.py
```

Detach with `Ctrl + A` and then `D`. To come back later:

```
screen -r tallybrew
```

### pm2

```
pm2 start main.py --interpreter python3 --name tallybrew
pm2 save
pm2 startup
```

If you use a virtual environment, point `--interpreter` to its Python, for example `./venv/bin/python`. See the logs with `pm2 logs tallybrew`.

### systemd

Use this if you want the bot to start by itself when the machine boots and to restart if it crashes.

Create `/etc/systemd/system/tallybrew.service`:

```ini
[Unit]
Description=tallybrew Discord bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/home/youruser/tallybrew
ExecStart=/home/youruser/tallybrew/venv/bin/python -u main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Replace `youruser` and the paths with your own, then:

```
sudo systemctl daemon-reload
sudo systemctl enable --now tallybrew
journalctl -u tallybrew -f
```

The `-u` flag makes Python print logs right away instead of buffering them.

### Windows

Run `python main.py` in a terminal and leave it open, or use **Task Scheduler** to start it when you log in.

---

## How it works

1. Every 15 minutes, a Discord task starts a scraping round in a separate thread, so the bot is never blocked.
2. Each platform is queried with the method listed in [Supported platforms](#supported-platforms):
   - **Whowatch**: a request to the Whowatch API profile endpoint.
   - **Instagram**: the `apify/instagram-followers-count-scraper` actor, run through the Apify client.
   - **Kick**: a request to the Kick channel API using `curl_cffi`, which imitates a real Chrome browser to get past basic anti-bot checks.
   - **TikTok and X**: a headless Chromium opened with Playwright that reads the follower number from the profile page.
3. Numbers are converted to a short format: `1500` becomes `1.5K` and `2000000` becomes `2M`.
4. For every platform that returned a number, the bot looks up the channel by ID. If its current name is different from the new one, it renames it. If not, it does nothing, to avoid wasting Discord's rate limit.
5. It waits 10 seconds after each channel so it does not hit Discord's rate limit.

A few things worth knowing:

- If a platform fails, the bot prints the error and keeps going with the others. One broken platform does not stop the rest.
- A platform that returns `0` followers is skipped, so its channel keeps the old name.
- TikTok and X numbers that already come abbreviated from the site, like `85.3K`, are shown exactly as the site shows them.

---

## Customization

All the options below are small edits in `main.py`.

### Changing the channel names

In the `update_stats` function there is a dictionary with the labels:

```python
nombres = {"whowatch": "Whowatch", "tiktok": "TikTok", "instagram": "IG", "twitter": "X", "kick": "Kick"}
```

Change the text on the right to whatever you want. For example, if you set `"tiktok": "TT Followers"`, the channel will be named `TT Followers: 85K`.

To change the whole format, edit this line in the same function:

```python
nuevo_nombre = f"{nombres[key]}: {valor}"
```

For example, `f"{nombres[key]} | {valor}"` gives `TikTok | 85K`.

### Changing the update interval

The interval is set in the decorator of `update_stats`:

```python
@tasks.loop(minutes=15)
```

Change `15` to any number of minutes. Do not set it too low: TikTok and X can block you if you scrape them too often, and every Instagram update uses Apify credits.

### Removing a platform

If you do not use a platform, do both of these so it is not scraped at all:

1. Delete its `try` block inside `ejecutar_ronda_scraping`.
2. Delete its line in the `CANALES` dictionary and its entry in the `data` dictionary at the top of the same function.

### Adding a new platform

1. Add a key to the `data` dictionary in `ejecutar_ronda_scraping`, for example `"youtube": None`.
2. Add a block that gets the follower count and stores it with `data["youtube"] = format_num(count)`.
3. Add the channel to `CANALES`: `"youtube": 0`.
4. Add its label to the `nombres` dictionary in `update_stats`.

---

## Project structure

```
tallybrew/
├── main.py            the whole bot
├── requirements.txt   Python dependencies
├── .gitignore
├── LICENSE            MIT license
├── assets/
│   └── divider.svg    the cat at the bottom of this README
└── README.md
```

---

## Troubleshooting

<details>
<summary><b>The bot starts but the channels do not change</b></summary>
<br/>

- Check that the channel IDs in `CANALES` are correct and are plain numbers. A wrong ID is skipped silently.
- Make sure the bot is in the server where those channels live.
- Make sure the bot has **Manage Channels**, and that no permission override on the channel or category denies it.
- Check that the platform actually returned a number. Look for `error` lines in the console.
</details>

<details>
<summary><b>discord.errors.LoginFailure: Improper token has been passed</b></summary>
<br/>

The `TOKEN` is empty, has extra spaces or is wrong. Go to the Discord developer portal, open your bot, click **Reset Token** and paste the new one between the quotes.
</details>

<details>
<summary><b>discord.errors.Forbidden: 403 Forbidden (error code: 50013): Missing Permissions</b></summary>
<br/>

The bot is in the server but cannot edit that channel. Give it **Manage Channels** and check the channel's permission overrides.
</details>

<details>
<summary><b>playwright._impl._errors.Error: Executable doesn't exist</b></summary>
<br/>

You forgot to run `playwright install chromium`. On a Linux server you might also need `playwright install-deps chromium`.
</details>

<details>
<summary><b>TikTok or X fail with a timeout error</b></summary>
<br/>

These sites change their pages often and sometimes block automated browsers. Try again later. If it always fails, they probably changed the HTML selector and it needs to be updated in the code:

- TikTok uses the selector `[data-e2e="followers-count"]`.
- X uses a link to `/<username>/verified_followers`.
</details>

<details>
<summary><b>Instagram does not update</b></summary>
<br/>

- Check that your `APIFY_TOKEN` is correct.
- Check that you still have credits in your Apify account.
- Make sure you have `apify-client` version 2.0.0 or higher: `pip install -U apify-client`.
</details>

<details>
<summary><b>Kick throws an error or returns nothing</b></summary>
<br/>

Kick has anti-bot protection. The bot uses `curl_cffi` to imitate a real browser, but it can still get blocked sometimes. Try again later and make sure `KICK_USER` matches the name in your channel URL.
</details>

<details>
<summary><b>Whowatch returns nothing</b></summary>
<br/>

Check that `WHOWATCH_ID` is the numeric user ID, between quotes, and that the `X-Whowatch-Device-Id` header is not empty.
</details>

<details>
<summary><b>A channel keeps the old name</b></summary>
<br/>

Discord limits channel renames to 2 every 10 minutes. The bot already waits between changes, but if you restart it many times in a row it can hit that limit. Wait a few minutes and it will catch up.
</details>

<details>
<summary><b>A platform with 0 followers never shows up</b></summary>
<br/>

On purpose, the bot skips a result of `0` so a failed request does not wipe your channel. Once the account has at least one follower, it will appear.
</details>

---

## FAQ

**Does it cost money?**
The bot, Discord, Playwright and curl_cffi are free. Only Instagram goes through Apify, which has its own plans and credit system. Check Apify's pricing and raise the update interval if you want to spend less.

**Do I have to use all 5 platforms?**
No. Remove the ones you do not need, as explained in [Removing a platform](#removing-a-platform).

**Can I track several accounts of the same platform?**
Not out of the box. You would need to duplicate that platform's block and add another channel for each account.

**Can I use it in more than one server?**
Not out of the box. Channel IDs are tied to one server, so you would need to run one copy of the bot per server, or extend the code to loop over several channel sets.

**Does it work on Windows?**
Yes. Use the Windows commands from the [installation](#installation) section.

**Why do some numbers look like `85.3K` and others like `1.1K`?**
TikTok and X sometimes give the number already abbreviated. The bot cannot turn `85.3K` back into an integer, so it shows it as the site does.

**Can I change how often it updates?**
Yes, see [Changing the update interval](#changing-the-update-interval).

**Does the bot need to be online all the time?**
Only to keep the numbers fresh. If it goes offline, the channels simply keep their last name until the bot comes back.

---

## Disclaimer

This project gets public data from social networks through scraping and unofficial APIs. Those platforms can change or block these methods at any time, and scraping may go against their terms of service. Use it at your own risk.

---

## Contributing

Bug reports and ideas are welcome.

1. Open an [issue](https://github.com/hypeblock26/tallybrew/issues) describing the problem or the idea.
2. To send code, fork the repository and create a branch:
   ```
   git checkout -b my-change
   ```
3. Make your change and test it with your own tokens, without committing them.
4. Open a pull request explaining what you changed and why.

---

## License

Released under the [MIT License](LICENSE).

---

## Credits

Built with:

- [discord.py](https://github.com/Rapptz/discord.py)
- [Playwright for Python](https://playwright.dev/python/)
- [Apify](https://apify.com) and its [Python client](https://github.com/apify/apify-client-python)
- [curl_cffi](https://github.com/lexiforest/curl_cffi)
- [Requests](https://requests.readthedocs.io)


&nbsp;

<p align="center">
  <img alt="divider" src="https://github.com/user-attachments/assets/ca28f237-9658-4460-905a-f32996d3659d" />
</p>

<p align="center">
  Brewed by <a href="https://github.com/hypeblock26">hypeblock26</a>
</p>


























