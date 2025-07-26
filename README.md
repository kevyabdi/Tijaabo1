📁 Telegram File Saver Bot (Like FiletoBot)

This Telegram bot allows users to send any file (document, video, audio, etc.) to the bot, and it will return a unique download link.
Anyone with that link can retrieve the file later by clicking the generated Telegram deep link.

Ideal for sharing files easily without hosting them externally. Files are stored securely using Telegram’s built-in file system.
🔑 Features

Upload any file → receive a unique download link
Supports documents, videos, and audio
No external hosting required — Telegram handles file storage
Files can be re-downloaded at any time via the same link
⚙️ How It Works

User sends a file to the bot
Bot saves the file_id and generates a custom deep link: https://t.me/YourBot?start=UNIQUE_ID
Anyone who clicks the link receives the file back from the bot automatically
🧠 Tech Stack

Python
Pyrogram
JSON (for file mapping)
Replit / Render for hosting
