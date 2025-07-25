from pyrogram import Client, filters
import json, os

API_ID = 26176218
API_HASH = "4a50bc8acb0169930f5914eb88091736"
BOT_TOKEN = "6946655182:AAEzKh7e0lPz2of03897CVpRq8-tMzsjM24"

app = Client("filetobot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

if not os.path.exists("files.json"):
    with open("files.json", "w") as f:
        json.dump({}, f)

def load_files():
    with open("files.json") as f:
        return json.load(f)

def save_file(file_id, unique_id):
    data = load_files()
    data[unique_id] = file_id
    with open("files.json", "w") as f:
        json.dump(data, f)

@app.on_message(filters.document | filters.video | filters.audio)
async def file_handler(client, message):
    file = message.document or message.video or message.audio
    file_id = file.file_id
    unique_id = file.file_unique_id

    save_file(file_id, unique_id)

    await message.reply_text(
        f"✅ File saved!\n"
        f"🔗 Share link: https://t.me/{(await app.get_me()).username}?start={unique_id}"
    )

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    args = message.text.split()
    if len(args) == 2:
        file_key = args[1]
        files = load_files()
        if file_key in files:
            await client.send_document(message.chat.id, files[file_key])
        else:
            await message.reply_text("❌ File not found.")
    else:
        await message.reply_text("👋 Send me a file and I’ll give you a shareable download link.")

app.run()

