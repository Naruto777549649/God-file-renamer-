# utils.py
import subprocess
import os

def change_thumbnail(video_path, thumbnail_path, new_file_name):
    """
    FFmpeg ka use karke video file ka thumbnail change karta hai.
    video_path: Original video file path.
    thumbnail_path: User ke provided thumbnail image path.
    new_file_name: New file name (with extension) jismein thumbnail change karke output milega.
    Returns: Output file path agar successful, else None.
    """
    directory = os.path.dirname(video_path)
    output_path = os.path.join(directory, new_file_name)
    
    # FFmpeg command: input video, input thumbnail, copy streams, aur set thumbnail as attached_pic
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-i", thumbnail_path,
        "-map", "0",
        "-map", "1",
        "-c", "copy",
        "-disposition:1", "attached_pic",
        output_path,
        "-y"
    ]
    try:
        subprocess.run(cmd, check=True)
        return output_path
    except Exception as e:
        print("Error in ffmpeg:", e)
        return None

def simulate_progress(task_name, total_size, current, speed, eta):
    """
    Simulated progress bar message.
    task_name: Naam of the task (Downloading/Uploading).
    total_size, current: Size details in MB.
    speed: Speed in MB/s.
    eta: Estimated time in seconds.
    Returns: Formatted progress message.
    """
    progress_message = f"╭━━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱━➣\n"
    progress_message += f"┣⪼ 🗃️ Sɪᴢᴇ: {current:.2f} Mʙ | {total_size:.2f} Mʙ\n"
    progress_message += f"┣⪼ ⏳️ Dᴏɴᴇ : {((current/total_size)*100):.2f}%\n"
    progress_message += f"┣⪼ 🚀 Sᴩᴇᴇᴅ: {speed:.2f} Mʙ/s\n"
    progress_message += f"┣⪼ ⏰️ Eᴛᴀ: {eta}ꜱ\n"
    progress_message += "╰━━━━━━━━━━━━━━━➣"
    return progress_message