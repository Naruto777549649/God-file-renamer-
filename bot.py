import os import sqlite3 import asyncio from pyrogram import Client, filters from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import Database from utils import progress_bar, format_filename from config import API_ID, API_HASH, BOT_TOKEN, ADMIN_ID

bot = Client("FileRenamerBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN) db = Database("files.db")

@bot.on_message(filters.command("start")) async def start(bot, message): await message.reply_photo( "https://telegra.ph/file/valid-image-url.jpg",  # Ensure this is a valid URL caption=f"Hᴀɪ {message.from_user.mention}\n\n◈ I Aᴍ A Pᴏᴡᴇʀғᴜʟ Fɪʟᴇ Rᴇɴᴀᴍᴇʀ Bᴏᴛ.", reply_markup=InlineKeyboardMarkup([ [InlineKeyboardButton("🔹 Updates", url="https://t.me/your_channel")], [InlineKeyboardButton("🔹 Support", url="https://t.me/your_support")], [InlineKeyboardButton("🔹 About", callback_data="about")] ]) )

@bot.on_message(filters.photo) async def save_thumbnail(bot, message): file_id = message.photo.file_id db.save_thumbnail(message.from_user.id, file_id) await message.reply_text("✅️ Tʜᴜᴍʙɴᴀɪʟ Sᴀᴠᴇᴅ")

@bot.on_message(filters.video | filters.document) async def rename_request(bot, message): file_name = message.document.file_name if message.document else message.video.file_name db.set_user_state(message.from_user.id, "waiting_for_filename")

await message.reply_text(
    f"Pʟᴇᴀꜱᴇ Eɴᴛᴇʀ Nᴇᴡ Fɪʟᴇɴᴀᴍᴇ...\n\nOʟᴅ Fɪʟᴇ Nᴀᴍᴇ :- `{file_name}`"
)

@bot.on_message(filters.text) async def get_filename(bot, message): user_id = message.from_user.id state = db.get_user_state(user_id)

if state == "waiting_for_filename":
    db.set_filename(user_id, message.text)
    await message.reply_text(
        f"Sᴇʟᴇᴄᴛ Tʜᴇ Oᴜᴛᴩᴜᴛ Fɪʟᴇ Tyᴩᴇ\n\nFɪʟᴇ Nᴀᴍᴇ :- `{message.text}`",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📂 Document", callback_data="rename_document")],
            [InlineKeyboardButton("📹 Video", callback_data="rename_video")]
        ])
    )

@bot.on_callback_query() async def callback_handler(bot, query): user_id = query.from_user.id file_type = "document" if query.data == "rename_document" else "video"

await query.message.edit_text("Downloading started...")
await asyncio.sleep(2)
await query.message.edit_text("Download in progress...\n\n" + progress_bar(20, 100))
await asyncio.sleep(5)  # Simulating download

await query.message.edit_text("Uploading started...")
await asyncio.sleep(2)
await query.message.edit_text("Upload in progress...\n\n" + progress_bar(80, 100))
await asyncio.sleep(3)

await bot.send_message(user_id, "⚠️ This file will be deleted in 20 mins ⚠️")

bot.run()

