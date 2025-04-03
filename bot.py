import os
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, API_ID, API_HASH, WELCOME_IMAGE
from database import init_db, save_thumbnail, get_thumbnail
from utils import change_thumbnail, simulate_progress

# Bot client initialization using Pyrogram
app = Client("telegram_thumbnail_bot",
             bot_token=BOT_TOKEN,
             api_id=API_ID,
             api_hash=API_HASH)

# Initialize database
init_db()

# Dictionary to store pending jobs per user (user_id -> job info)
app.pending_jobs = {}

# /start command: Send welcome message with inline buttons and welcome image
@app.on_message(filters.command("start"))
def start(client, message):
    user_first_name = message.from_user.first_name
    welcome_text = (
        f"Hᴀɪ {user_first_name}\n\n"
        "◈ I Aᴍ A Pᴏᴡᴇʀғᴜʟ Fɪʟᴇ Rᴇɴᴀᴍᴇʀ Bᴏᴛ.\n"
        "◈ I Cᴀɴ Rᴇɴᴀᴍᴇ Fɪʟᴇs, Cʜᴀɴɢᴇ Tʜᴜᴍʙɴᴀɪʟs, Cᴏɴᴠᴇʀᴛ Bᴇᴛᴡᴇᴇɴ Vɪᴅᴇᴏ Aɴᴅ Fɪʟᴇ, "
        "Aɴᴅ Sᴜᴘᴘᴏʀᴛ Cᴜsᴛᴏᴍ Tʜᴜᴍʙɴᴀɪʟs Aɴᴅ Cᴀᴘᴛɪᴏɴs.\n\n"
        "• Mᴀɪɴᴛᴀɪɴᴇᴅ Bʏ : @YourUsername"
    )
    # Inline buttons: 3 buttons (Rename File, Change Thumbnail, Convert)
    buttons = [
        [InlineKeyboardButton("Rename File", callback_data="rename_file")],
        [InlineKeyboardButton("Change Thumbnail", callback_data="change_thumbnail")],
        [InlineKeyboardButton("Convert", callback_data="convert")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    if os.path.exists(WELCOME_IMAGE):
        message.reply_photo(photo=WELCOME_IMAGE, caption=welcome_text, reply_markup=reply_markup)
    else:
        message.reply_text(welcome_text, reply_markup=reply_markup)

# Handling user thumbnail image: Save thumbnail in DB
@app.on_message(filters.photo)
def save_user_thumbnail(client, message):
    user_id = message.from_user.id
    file_path = client.download_media(message)
    save_thumbnail(user_id, file_path)
    message.reply_text("✅️ Tʜᴜᴍʙɴᴀɪʟ Sᴀᴠᴇᴅ")

# Handling video file messages (video or document)
@app.on_message(filters.video | filters.document)
def handle_video(client, message):
    user_id = message.from_user.id
    thumb_path = get_thumbnail(user_id)
    if not thumb_path:
        message.reply_text("Please send a thumbnail image first.")
        return

    # Download video
    video_path = client.download_media(message)
    # Old file name extraction
    old_file_name = (message.document.file_name 
                     if message.document and message.document.file_name 
                     else message.video.file_name)
    # Store pending job info for this user
    app.pending_jobs[user_id] = {
        "video_path": video_path,
        "old_file_name": old_file_name,
        "message_id": message.message_id
    }
    message.reply_text(f"Pʟᴇᴀꜱᴇ Eɴᴛᴇʀ Nᴇᴡ Fɪʟᴇɴᴀᴍᴇ...\n\n"
                       f"Oʟᴅ Fɪʟᴇ Nᴀᴍᴇ :- [{old_file_name}]")

# Handling new file name input (user replies with new file name)
@app.on_message(filters.text & filters.reply)
def handle_new_file_name(client, message):
    user_id = message.from_user.id
    if user_id not in app.pending_jobs:
        return
    pending = app.pending_jobs[user_id]
    new_file_name = message.text.strip()
    pending["new_file_name"] = new_file_name
    # Inline buttons for output file type selection: Document, Video, Cancel
    buttons = [
        [
            InlineKeyboardButton("Document", callback_data="output_doc"),
            InlineKeyboardButton("Video", callback_data="output_video"),
            InlineKeyboardButton("Cancel", callback_data="cancel")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    message.reply_text(f"Sᴇʟᴇᴄᴛ Tʜᴇ Oᴜᴛᴩᴜᴛ Fɪʟᴇ Tyᴩᴇ\n• Fɪʟᴇ Nᴀᴍᴇ :- {new_file_name}", reply_markup=reply_markup)

# Handling inline button callbacks for output type selection and cancellation
@app.on_callback_query()
def callback_query_handler(client, callback_query):
    data = callback_query.data
    user_id = callback_query.from_user.id
    if user_id not in app.pending_jobs:
        callback_query.answer("No pending job found.", show_alert=True)
        return

    pending = app.pending_jobs[user_id]

    if data == "cancel":
        callback_query.answer("Operation Cancelled.", show_alert=True)
        app.pending_jobs.pop(user_id, None)
        return

    # Simulate download progress
    callback_query.edit_message_text("Tʀyɪɴɢ Tᴏ Dᴏᴡɴʟᴏᴀᴅɪɴɢ....")
    time.sleep(2)
    progress_msg = simulate_progress("Downloading", 74.73, 14.72, 2.16, 35)
    callback_query.edit_message_text(progress_msg)
    time.sleep(2)
    # Simulate upload progress
    callback_query.edit_message_text("Tʀyɪɴɢ Tᴏ Uᴩʟᴏᴀᴅɪɴɢ....")
    time.sleep(2)
    progress_msg = simulate_progress("Uploading", 74.73, 70.26, 5.04, 14)
    callback_query.edit_message_text(progress_msg)
    time.sleep(2)
    callback_query.edit_message_text("Processing thumbnail change...")

    # Get user's saved thumbnail
    thumb_path = get_thumbnail(user_id)
    video_path = pending["video_path"]
    new_file_name = pending["new_file_name"]

    # Change thumbnail using FFmpeg via utils.change_thumbnail
    output_path = change_thumbnail(video_path, thumb_path, new_file_name)
    if output_path:
        if data == "output_doc":
            client.send_document(callback_query.message.chat.id,
                                 document=output_path,
                                 caption=f"Fɪʟᴇ Renamed to: {new_file_name}")
        elif data == "output_video":
            client.send_video(callback_query.message.chat.id,
                              video=output_path,
                              caption=f"Fɪʟᴇ Renamed to: {new_file_name}")
        # Send deletion alert message
        client.send_message(callback_query.message.chat.id,
                            "｡°⚠️°｡ 𝗔𝗹𝗲𝗿𝘁 ｡°⚠️°｡\n\n"
                            "Tʜɪꜱ Fɪʟᴇ/Vɪᴅᴇᴏ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ɪɴ 20 𝗠𝗶𝗻𝘀 🫥\n"
                            "(𝘿𝙪𝙚 𝙩𝙤 𝘾𝙤𝙥𝙮𝙧𝙞𝙜𝙝𝙩 𝙄𝙨𝙨𝙪𝙚𝙨).")
    else:
        client.send_message(callback_query.message.chat.id, "Thumbnail change failed.")
    # Clear pending job
    app.pending_jobs.pop(user_id, None)
    callback_query.answer()