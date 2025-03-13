import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pyperclip
import yt_dlp
import threading

def progress_hook(d):
    if d['status'] == 'downloading':
        progress_label.config(text=f"Downloading: {d['_percent_str']} of {d.get('_total_bytes_str', 'Unknown')}")
    elif d['status'] == 'finished':
        progress_label.config(text="Download complete")

def download_media(url, output_path, quality, audio_only=False):
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': 'bestaudio' if audio_only else quality.split()[0],
        'progress_hooks': [progress_hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if audio_only:
                original_path = os.path.join(output_path, f"{info['title']}.{info['ext']}")
                new_path = os.path.join(output_path, f"{info['title']}.mp3")
                os.rename(original_path, new_path)  # Rename file to .mp3

        messagebox.showinfo("Success", "Download complete")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        progress_label.config(text="")

def start_download(audio_only=False):
    url = url_entry.get()
    output_path = output_path_var.get()
    quality = quality_var.get()
    
    if not url:
        messagebox.showwarning("Input Error", "Please enter a video URL")
        return
    if not output_path:
        messagebox.showwarning("Input Error", "Please select an output path")
        return

    threading.Thread(target=download_media, args=(url, output_path, quality, audio_only)).start()

def browse_directory():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_path_var.set(folder_selected)

def paste_url():
    url = pyperclip.paste()
    url_entry.delete(0, tk.END)
    url_entry.insert(0, url)

# Create the main window
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("550x250")
root.resizable(False, False)
root.iconbitmap("youtube_22742.ico")

# Use ttk for better styling
style = ttk.Style()
style.configure("Rounded.TButton", font=("Helvetica", 12, "bold"), padding=10, relief="flat", borderwidth=5)
style.map("Rounded.TButton", background=[("active", "#c1c1c1")])

# URL input
tk.Label(root, text="Video URL:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

# Paste URL button
paste_url_button = tk.Button(root, text="Paste URL", command=paste_url, bg="#FFA500", fg="black", font=("Helvetica", 10, "bold"), padx=10, pady=5)
paste_url_button.grid(row=0, column=3, padx=10, pady=10)

# Output path selection
tk.Label(root, text="Output Path:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
output_path_var = tk.StringVar()
output_path_entry = tk.Entry(root, textvariable=output_path_var, width=40)
output_path_entry.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
browse_button = tk.Button(root, text="Browse", command=browse_directory, bg="#4682B4", fg="white", font=("Helvetica", 10, "bold"), padx=10, pady=5)
browse_button.grid(row=1, column=3, padx=10, pady=10)

# Quality selection
tk.Label(root, text="Video Quality:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
quality_var = tk.StringVar()
quality_options = [
    'best (Highest quality available)',
    'worst (Lowest quality available)',
    '18 (360p)',
    '22 (720p)',
    '137+140 (1080p + audio)'
]
quality_menu = ttk.OptionMenu(root, quality_var, *quality_options)
quality_menu.grid(row=2, column=1, padx=10, pady=10, columnspan=2)
quality_var.set('best (Highest quality available)')

# Button Frame (for better layout)
button_frame = tk.Frame(root)
button_frame.grid(row=3, column=0, columnspan=4, pady=20)

# Download Video button
download_button = tk.Button(button_frame, text="Download Video", command=lambda: start_download(audio_only=False),
                            bg="green", fg="black", font=("Helvetica", 12, "bold"), padx=20, pady=10, width=18)
download_button.pack(side="left", padx=10)

# Download Audio button
audio_download_button = tk.Button(button_frame, text="Download Audio", command=lambda: start_download(audio_only=True),
                                  bg="orange", fg="black", font=("Helvetica", 12, "bold"), padx=20, pady=10, width=18)
audio_download_button.pack(side="left", padx=10)

# Progress label
progress_label = tk.Label(root, text="", font=("Helvetica", 10))
progress_label.grid(row=4, column=0, columnspan=4, pady=10)

# Start the GUI event loop
root.mainloop()
