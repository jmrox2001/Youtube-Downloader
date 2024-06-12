import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import pyperclip  # You need to install the pyperclip module (pip install pyperclip)
import yt_dlp
import os

def download_video(url, output_path, quality):
    def progress_hook(d):
        if d['status'] == 'downloading':
            progress_label.config(text=f"Downloading: {d['_percent_str']} of {d['_total_bytes_str']}")
        elif d['status'] == 'finished':
            progress_label.config(text="Download complete")

    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': quality.split()[0],
        'progress_hooks': [progress_hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Video downloaded successfully")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        progress_label.config(text="")

def fetch_video_info(url):
    ydl_opts = {
        'format': 'best',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

def browse_directory():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_path_var.set(folder_selected)

def open_youtube():
    webbrowser.open("https://www.youtube.com")

def paste_url():
    url = pyperclip.paste()
    url_entry.delete(0, tk.END)
    url_entry.insert(0, url)

def start_download():
    url = url_entry.get()
    output_path = output_path_var.get()
    quality = quality_var.get()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a video URL")
        return
    if not output_path:
        messagebox.showwarning("Input Error", "Please select an output path")
        return
    if not quality:
        messagebox.showwarning("Input Error", "Please select a video quality")
        return
    
    info = fetch_video_info(url)
    if info:
        size = info.get('filesize_approx', 'Unknown')
        size_str = f"{size / (1024 ** 2):.2f} MB" if size != 'Unknown' else size
        title = info.get('title', 'Unknown')
        if messagebox.askyesno("Confirm Download", f"Title: {title}\nSize: {size_str}\nQuality: {quality}\nDo you want to download this video?"):
            download_video(url, output_path, quality)

# Create the main window
root = tk.Tk()
root.title("YouTube Video Downloader")

# URL input
tk.Label(root, text="Video URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

# Open YouTube button
open_youtube_button = tk.Button(root, text="Open YouTube", command=open_youtube)
open_youtube_button.grid(row=0, column=2, padx=10, pady=10)

# Paste URL button
paste_url_button = tk.Button(root, text="Paste URL", command=paste_url)
paste_url_button.grid(row=0, column=3, padx=10, pady=10)

# Output path selection
tk.Label(root, text="Output Path:").grid(row=1, column=0, padx=10, pady=10)
output_path_var = tk.StringVar()
output_path_entry = tk.Entry(root, textvariable=output_path_var, width=40)
output_path_entry.grid(row=1, column=1, padx=10, pady=10)
browse_button = tk.Button(root, text="Browse", command=browse_directory)
browse_button.grid(row=1, column=2, padx=10, pady=10)

# Quality selection
tk.Label(root, text="Video Quality:").grid(row=2, column=0, padx=10, pady=10)
quality_var = tk.StringVar()
quality_options = [
    'best (Highest quality available)',
    'worst (Lowest quality available)',
    '18 (360p)',
    '22 (720p)',
    '137+140 (1080p + audio)'
]
quality_menu = tk.OptionMenu(root, quality_var, *quality_options)
quality_menu.grid(row=2, column=1, padx=10, pady=10)
quality_var.set('best (Highest quality available)')  # Default value

# Download button
download_button = tk.Button(root, text="Download", command=start_download)
download_button.grid(row=3, column=0, columnspan=4, pady=10)

# Progress label
progress_label = tk.Label(root, text="")
progress_label.grid(row=4, column=0, columnspan=4, pady=10)

# Start the GUI event loop
root.mainloop()
