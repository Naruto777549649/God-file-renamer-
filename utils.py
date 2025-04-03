def progress_bar(done, total):
    percent = (done / total) * 100
    bar = "█" * int(percent / 10) + "░" * (10 - int(percent / 10))
    return f"╭━━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱━➣\n┣⪼ 🗃️ Sɪᴢᴇ: {done:.1f} Mʙ | {total:.1f} Mʙ\n┣⪼ ⏳️ Dᴏɴᴇ : {percent:.2f}%\n┣⪼ 🚀 Sᴩᴇᴇᴅ: 5.04 Mʙ/s\n┣⪼ ⏰️ Eᴛᴀ: 14ꜱ\n╰━━━━━━━━━━━━━━━➣"

def format_filename(name):
    return name.replace(" ", "_").replace("-", "_").lower()