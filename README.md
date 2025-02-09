
# Discord Safe Browsing Bot

This Discord bot is designed to enhance server security by automatically detecting and removing suspicious links using the **Google Safe Browsing API**. Additionally, it mutes users who post unsafe links for **30 minutes** to prevent further risks.

## 🚀 Features

- **Real-Time Link Scanning:** Every posted link is checked against Google's Safe Browsing database.
- **Automatic Message Deletion:** Suspicious messages are immediately removed.
- **User Timeout:** Offending users are muted for 30 minutes to prevent further threats.
- **DM Notifications:** The bot notifies the user when their message has been deleted and when they have been muted.

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kyuubiddragon/Discord-AntiPhishingLinks.git
   cd Discord-AntiPhishingLinks
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Replace the placeholder in `bot.run()` with your actual Discord bot token.

4. Add your **Google Safe Browsing API key** to the script:
   - Sign up [here](https://developers.google.com/safe-browsing/v4) to get your API key.
   - Replace `API_KEY` with your own key.

## 🚨 Permissions Required

- **Read Messages**
- **Manage Messages** (to delete messages)
- **Moderate Members** (to mute users)

Ensure the bot role is above the roles of users it needs to moderate.

## 💡 Usage

Simply run the bot:
```bash
python bot.py
```

The bot will automatically monitor messages in all channels it's authorized to access.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
