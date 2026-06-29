# X-AutoFollowBack

A Python automation tool that checks your X (Twitter) followers and automatically follows back users who follow you.

> ⚠️ Use responsibly. Automation on social platforms may violate platform rules or trigger rate limits. Keep your account safe and never share your cookies or tokens.

## Features

- Automatically detects new followers
- Follows back users who are not already followed
- Uses randomized delays to avoid robotic behavior
- Refreshes `ct0` automatically from `auth_token`
- Handles rate limits with cooldown
- Simple `config.json` setup
- Clean terminal logs with status messages

## Tech Stack

- Python
- `tls_client`
- `colorama`
- X/Twitter internal API endpoints

## Project Structure

```bash
X-AutoFollowBack/
├── main.py
└── config.json
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Deepthanush1337/X-AutoFollowBack.git
cd X-AutoFollowBack
```

Install dependencies:

```bash
pip install tls_client colorama
```

## Configuration

Open `config.json` and add your X `auth_token`:

```json
{
  "auth_token": "YOUR_AUTH_TOKEN_HERE",
  "ct0": ""
}
```

The tool will automatically derive and update the `ct0` value when it runs.

## How to Get `auth_token`

1. Open [x.com](https://x.com) in Chrome.
2. Press `F12` to open Developer Tools.
3. Go to **Application**.
4. Open **Cookies** → `https://x.com`.
5. Copy the value of `auth_token`.
6. Paste it into `config.json`.

## Usage

Run the script:

```bash
python main.py
```

The bot will:

1. Authenticate using your `auth_token`.
2. Derive a fresh `ct0`.
3. Fetch your followers.
4. Fetch your following list.
5. Follow back users who follow you but are not followed back yet.
6. Repeat checks after randomized intervals.

## Important Notes

- Do not upload your real `auth_token` to GitHub.
- Keep `config.json` private if it contains tokens.
- Too many follow actions can trigger rate limits.
- This project is intended for learning and personal automation experiments.

## Security Warning

Your `auth_token` gives access to your X account session. Treat it like a password.

Recommended:

```bash
echo config.json >> .gitignore
```

Then create a safe example config:

```json
{
  "auth_token": "",
  "ct0": ""
}
```

Save it as:

```bash
config.example.json
```

## Disclaimer

This project is for educational purposes only. Use it at your own risk. The developer is not responsible for account restrictions, rate limits, or misuse.
