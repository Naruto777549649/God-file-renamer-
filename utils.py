# utils.py
import subprocess 
import os

def change_thumbnail(video_path, thumbnail_path, new_file_name): """ FFmpeg ka use karke video file ka thumbnail change karta hai. """ directory = os.path.dirname(video_path) output_path = os.path.join(directory, new_file_name)

cmd = [
    "ffmpeg", "-i", video_path, "-i", thumbnail_path,
    "-map", "0", "-map", "1", "-c", "copy", "-disposition:1", "attached_pic",
    output_path, "-y"
]
try:
    subprocess.run(cmd, check=True)
    return output_path
except Exception as e:
    print("Error in ffmpeg:", e)
    return None

def progress_bar(current, total, length=20): """ Progress bar banane ka function. """ progress = int((current / total) * length) bar = "█" * progress + "-" * (length - progress) return f"[{bar}] {current}%"

def simulate_progress(task_name, total_size, current, speed, eta): """ Simulated progress bar message. """ return ( f"╭━━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱━➣\n" f"┣⪼ 🗃️ Sɪᴢᴇ: {current:.2f} Mʙ | {total_size:.2f} Mʙ\n" f"┣⪼ ⏳️ Dᴏɴᴇ : {((current/total_size)*100):.2f}%\n" f"┣⪼ 🚀 Sᴩᴇᴇᴅ: {speed:.2f} Mʙ/s\n" f"┣⪼ ⏰️ Eᴛᴀ: {eta}ꜱ\n" "╰━━━━━━━━━━━━━━━➣" )

