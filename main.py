from pyrogram import filters
from pyrogram.client import Client
import json
import os
import uuid
import logging
from datetime import datetime
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get credentials from environment variables with fallbacks
API_ID = int(os.getenv("API_ID", "26176218"))
API_HASH = os.getenv("API_HASH", "4a50bc8acb0169930f5914eb88091736")
BOT_TOKEN = os.getenv("BOT_TOKEN", "6946655182:AAFitxLxNr0eUOfXPInNrEaWIFUS5AENKSU")

# Initialize the Pyrogram client
app = Client("filetobot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Ensure files.json exists
if not os.path.exists("files.json"):
    with open("files.json", "w") as f:
        json.dump({}, f)
        logger.info("Created new files.json database")

def load_files():
    """Load file mappings from JSON database"""
    try:
        with open("files.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading files.json: {e}")
        return {}

def save_file_mapping(file_id, unique_id, file_type):
    """Save file ID and type mapping to JSON database"""
    try:
        data = load_files()
        data[unique_id] = {
            "file_id": file_id,
            "file_type": file_type,
            "timestamp": datetime.utcnow().isoformat()
        }
        with open("files.json", "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved file mapping for unique_id: {unique_id}")
        return True
    except Exception as e:
        logger.error(f"Error saving file mapping: {e}")
        return False

@app.on_message(filters.document | filters.video | filters.audio | filters.photo)
async def file_handler(client, message):
    """Handle incoming file uploads"""
    try:
        file = None
        file_type = ""
        display_type = "📁 File"

        if message.document:
            file = message.document
            file_type = "document"
            display_type = "📄 Document"
        elif message.video:
            file = message.video
            file_type = "video"
            display_type = "🎥 Video"
        elif message.audio:
            file = message.audio
            file_type = "audio"
            display_type = "🎵 Audio"
        elif message.photo:
            file = message.photo
            file_type = "photo"
            display_type = "🖼️ Photo"

        if not file:
            await message.reply_text("❌ Unable to process this file type.")
            return

        file_id = file.file_id
        unique_id = file.file_unique_id

        if save_file_mapping(file_id, unique_id, file_type):
            bot_me = await app.get_me()
            bot_username = bot_me.username

            share_link = f"https://t.me/{bot_username}?start={unique_id}"

            file_size = ""
            if hasattr(file, 'file_size') and file.file_size:
                size_mb = file.file_size / (1024 * 1024)
                file_size = f" ({size_mb:.1f} MB)" if size_mb >= 1 else f" ({file.file_size} bytes)"

            file_name = ""
            if hasattr(file, 'file_name') and file.file_name:
                file_name = f"\n📝 Name: {file.file_name}"

            response_text = (
                f"✅ File uploaded successfully!\n\n"
                f"📂 Type: {display_type}{file_size}"
                f"{file_name}\n"
                f"🔗 Share Link:\n{share_link}\n\n"
                f"💡 Anyone with this link can download your file!"
            )

            await message.reply_text(response_text, parse_mode=None)
            logger.info(f"File uploaded by user {message.from_user.id}: {display_type}")
        else:
            await message.reply_text("❌ Failed to save file. Please try again.")

    except Exception as e:
        logger.error(f"Error handling file upload: {e}")
        await message.reply_text("❌ An error occurred while processing your file. Please try again.")

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    """Handle /start command and file retrieval"""
    try:
        args = message.text.split()

        if len(args) == 2:
            file_key = args[1]
            files = load_files()

            if file_key in files:
                file_data = files[file_key]
                file_id = file_data.get("file_id")
                file_type = file_data.get("file_type")

                await message.reply_text("📤 Sending your file...")

                try:
                    if file_type == "photo":
                        await client.send_photo(message.chat.id, file_id, caption="📥 File retrieved successfully!\n\n💡 Share the link with others to let them download this file too!")
                    elif file_type == "video":
                        await client.send_video(message.chat.id, file_id, caption="📥 File retrieved successfully!\n\n💡 Share the link with others to let them download this file too!")
                    elif file_type == "audio":
                        await client.send_audio(message.chat.id, file_id, caption="📥 File retrieved successfully!\n\n💡 Share the link with others to let them download this file too!")
                    else:
                        await client.send_document(message.chat.id, file_id, caption="📥 File retrieved successfully!\n\n💡 Share the link with others to let them download this file too!")

                    logger.info(f"File retrieved by user {message.from_user.id}: {file_key}")
                except Exception as e:
                    logger.error(f"Error sending file {file_key}: {e}")
                    await message.reply_text(
                        "❌ **File not accessible**\n\n"
                        "This file may have been deleted from Telegram's servers or is no longer available."
                    )
            else:
                await message.reply_text(
                    "❌ **File not found**\n\n"
                    "The file you're looking for doesn't exist or the link is invalid."
                )
        else:
            welcome_text = (
                "👋 Welcome to File Saver Bot!\n\n"
                "📁 How it works:\n"
                "1️⃣ Send me any file (document, video, audio, or photo)\n"
                "2️⃣ Get a unique shareable download link\n"
                "3️⃣ Anyone with the link can download your file\n\n"
                "🔒 Secure & Private\n"
                "• Files are stored using Telegram's infrastructure\n"
                "• No external hosting required\n"
                "• Links work indefinitely\n\n"
                "📤 Send me a file to get started!"
            )

            await message.reply_text(welcome_text, parse_mode=None)
            logger.info(f"New user started the bot: {message.from_user.id}")

    except Exception as e:
        logger.error(f"Error in start handler: {e}")
        await message.reply_text("❌ An error occurred. Please try again.")

@app.on_message(filters.command("help"))
async def help_handler(client, message):
    """Handle /help command"""
    help_text = (
        "📖 **Help - File Saver Bot**\n\n"
        "🔧 **Commands:**\n"
        "• `/start` - Start the bot or retrieve a file\n"
        "• `/help` - Show this help message\n\n"
        "📤 **Uploading Files:**\n"
        "• Send any document, video, audio, or photo\n"
        "• Get a unique shareable link instantly\n"
        "• Share the link with anyone\n\n"
        "📥 **Downloading Files:**\n"
        "• Click any file link you received\n"
        "• Files are sent back automatically\n\n"
        "💡 **Tips:**\n"
        "• Links work indefinitely\n"
        "• No file size limits (Telegram's limits apply)\n"
        "• All file types supported\n"
        "• Files stored securely on Telegram servers"
    )

    await message.reply_text(help_text, parse_mode=None)

@app.on_message(filters.text & ~filters.command(["start", "help"]))
async def text_handler(client, message):
    """Handle regular text messages"""
    await message.reply_text(
        "📁 **Send me a file to get started!**\n\n"
        "I can handle:\n"
        "• 📄 Documents (PDF, DOC, etc.)\n"
        "• 🎥 Videos (MP4, AVI, etc.)\n"
        "• 🎵 Audio files (MP3, WAV, etc.)\n"
        "• 🖼️ Photos (JPG, PNG, etc.)\n\n"
        "Use /help for more information."
    )

if __name__ == "__main__":
    logger.info("Starting File Saver Bot...")
    try:
        # If you have keep_alive.py for hosting, keep this; else remove these 2 lines
        from keep_alive import keep_alive
        keep_alive()

        app.run()
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
