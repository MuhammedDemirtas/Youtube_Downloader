import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import yt_dlp
import threading
import os

# Developer: M. Demirtas
# Application: YouTube Video Downloader
# Description: This application allows users to download YouTube videos and audio in various formats and resolutions.

output_folder = "Download"
os.makedirs(output_folder, exist_ok=True)

root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("450x740")
root.configure(bg="#221F1F")

resolution_listbox_formats = []
selected_resolution = tk.StringVar()

def clear_ui():
    """Clear the UI components for a new download."""
    url_entry.delete(0, tk.END)
    video_title.set("")
    resolution_menu["menu"].delete(0, "end")
    selected_resolution.set("Select")
    thumbnail_label.config(image="")
    thumbnail_label.image = None
    progress_bar["value"] = 0

def fetch_video_info():
    """Fetch video details from the given YouTube URL."""
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL!")
        return

    try:
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            video_title.set(info["title"])
            video_thumbnail_url = info["thumbnail"]

            format_list = []
            global resolution_listbox_formats
            resolution_listbox_formats.clear()

            resolution_dict = {}
            for f in info["formats"]:
                if f.get("vcodec") != "none" and f.get("acodec") == "none" and f.get("height") and f.get("width"):
                    height = f.get("height")
                    width = f.get("width")
                    format_id = f.get("format_id", "N/A")
                    resolution = f"{height}x{width}"
                    format_note = f.get("format_note", "N/A")
                    fps = f.get("fps", "N/A")
                    resolution_dict[resolution] = (format_id, format_note, fps)

            resolution_menu["menu"].delete(0, "end")
            for resolution, (format_id, format_note, fps) in sorted(resolution_dict.items(), key=lambda x: int(x[0].split('x')[0])):
                display_text = f"{resolution} ({format_note}, {fps} fps)"
                resolution_menu["menu"].add_command(label=display_text, command=lambda value=format_id: selected_resolution.set(value))
                resolution_listbox_formats.append(format_id)

            response = requests.get(video_thumbnail_url)
            img_data = Image.open(BytesIO(response.content))
            img_data = img_data.resize((150, 100), Image.LANCZOS)
            img = ImageTk.PhotoImage(img_data)
            thumbnail_label.config(image=img)
            thumbnail_label.image = img
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while fetching video info: {e}")

def download_video():
    """Download selected video resolution."""
    def _download():
        url = url_entry.get()
        if not url or not selected_resolution.get():
            messagebox.showerror("Error", "Please select a video and resolution!")
            return

        try:
            selected_format = selected_resolution.get()
            video_file_name = video_title.get().replace(" ", "_").replace("/", "_")
            output_path = os.path.join(output_folder, f"{video_file_name}.webm")

            ydl_opts = {
                "format": f"{selected_format}+bestaudio/best",
                "outtmpl": output_path,
                "progress_hooks": [progress_hook],
                "merge_output_format": "webm",
                "noplaylist": True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            messagebox.showinfo("Success", f"Video successfully downloaded: {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during download: {e}")

        clear_ui()

    progress_bar["value"] = 0
    threading.Thread(target=_download).start()

def download_audio():
    """Download audio-only version of the video."""
    def _download_audio():
        url = url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL!")
            return

        try:
            audio_file_name = video_title.get().replace(" ", "_").replace("/", "_")
            output_path = os.path.join(output_folder, f"{audio_file_name}.mp3")

            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": output_path,
                "progress_hooks": [progress_hook],
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
                "noplaylist": True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            messagebox.showinfo("Success", f"Audio successfully downloaded: {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while downloading audio: {e}")

        clear_ui()

    progress_bar["value"] = 0
    threading.Thread(target=_download_audio).start()

def multiple_download_audio():
    """Download audio files for multiple YouTube URLs."""
    def _multiple_download():
        urls = url_text.get("1.0", tk.END).strip().split("\n")
        if not urls:
            messagebox.showerror("Error", "Please enter at least one YouTube URL!")
            return

        try:
            for url in urls:
                if url.strip():
                    with yt_dlp.YoutubeDL({
                        "format": "bestaudio/best",
                        "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
                        "postprocessors": [{
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }],
                    }) as ydl:
                        ydl.download([url.strip()])

            messagebox.showinfo("Success", "All audio files successfully downloaded!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during multiple audio download: {e}")

    threading.Thread(target=_multiple_download).start()

def progress_hook(d):
    """Update progress bar based on download progress."""
    if d["status"] == "downloading":
        downloaded_bytes = d.get("downloaded_bytes", 0)
        total_bytes = d.get("total_bytes", 1)
        progress_percentage = (downloaded_bytes / total_bytes) * 100
        progress_bar["value"] = progress_percentage
    elif d["status"] == "finished":
        progress_bar["value"] = 100

title_frame = tk.Frame(root, bg="#221F1F")
title_frame.pack(pady=10)

logo_path = "downimg.png"
if os.path.exists(logo_path):
    logo_img = Image.open(logo_path)
    logo_img = logo_img.resize((20, 20), Image.LANCZOS)
    logo_tk = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(title_frame, image=logo_tk, bg="#221F1F")
    logo_label.image = logo_tk
    logo_label.pack(side="left", padx=5)

title_label = tk.Label(title_frame, text="YouTube Video Downloader", font=("Arial", 16, "bold"), bg="#221F1F", fg="white")
title_label.pack(side="left")

url_label = tk.Label(root, text="YouTube URL:", bg="#221F1F", fg="white")
url_label.pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

fetch_button = ttk.Button(root, text="Fetch Video Info", command=fetch_video_info)
fetch_button.pack(pady=5)

video_title = tk.StringVar()
title_display = tk.Label(root, textvariable=video_title, wraplength=450, font=("Arial", 12), fg="white", bg="#221F1F")
title_display.pack(pady=5)

thumbnail_label = tk.Label(root, bg="#221F1F")
thumbnail_label.pack(pady=10)

resolution_label = tk.Label(root, text="Select Resolution:", bg="#221F1F", fg="white")
resolution_label.pack()
resolution_menu = ttk.OptionMenu(root, selected_resolution, "Select")
resolution_menu.pack(pady=5)

download_button = ttk.Button(root, text="Download Video", command=download_video)
download_button.pack(pady=10)

audio_button = ttk.Button(root, text="Download Audio (MP3)", command=download_audio)
audio_button.pack(pady=10)

multiple_audio_label = tk.Label(root, text="Multiple YouTube URLs (One URL per line):", bg="#221F1F", fg="white")
multiple_audio_label.pack(pady=10)
url_text = tk.Text(root, height=10, width=50)
url_text.pack(pady=5)

multiple_download_button = ttk.Button(root, text="Multiple Download Audio (MP3)", command=multiple_download_audio)
multiple_download_button.pack(pady=10)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

root.mainloop()
