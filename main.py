import customtkinter as ctk
import requests
import os, io
import win32clipboard as clip
import win32con as con
from PIL import Image, ImageGrab
from bs4 import BeautifulSoup

def extractVideoCode(link: str):
    replaceList = ["https://www.youtube.com/watch?v=", "https://youtu.be/", "https://www.youtube.com/shorts/",]
    _ = "" 
    for i in replaceList:
        link = link.replace(i, "")
    
    for i in link:
        if i != "?" and i != "&":
            _ += i
        else:
            break
    return _
def getThumbnail(link: str):
    videocode = extractVideoCode(link)
    thumbnail_link = f"https://i.ytimg.com/vi/{videocode}/maxresdefault.jpg"
    temp = os.getenv('temp')
    with open(fr'{temp}\\{videocode}.png', 'ab') as f:
        f.write(requests.get(thumbnail_link).content)
        f.close()
    return f'{temp}\\{videocode}.png'

def gui():
    app = ctk.CTk()
    ctk.set_default_color_theme('green')
    app.geometry("800x600")
    app.resizable(False, False)
    app.title("GetYoutubeThumbnail")

    ctk.CTkLabel(app, text="Version 1.0", text_color="#383838").place(anchor='se', relx=0.99, rely=1)
    searchEntry = ctk.CTkEntry(app, placeholder_text="Youtube video URL", width=512)
    thumbnail_label = ctk.CTkLabel(app, image=None, text="")

    def onCopyButton():
        thumbnail = Image.open(getThumbnail(searchEntry.get()))
        buf = io.BytesIO()
        thumbnail.convert("RGB").save(buf, "BMP")
        data = buf.getvalue()[14:]
        buf.close()
        
        clip.OpenClipboard()
        clip.EmptyClipboard()
        clip.SetClipboardData(con.CF_DIB, data)
        clip.CloseClipboard()
        
    def onDownloadButton():
        thumbnail = Image.open(getThumbnail(searchEntry.get()))
        thumbnail.save(f"{extractVideoCode(searchEntry.get())}.png")
    def onClickSearch():
        if "youtu" in searchEntry.get():
            thumbnail = Image.open(getThumbnail(searchEntry.get()))
            size = (round(thumbnail.size[0]//2.5), round(thumbnail.size[1]//2.5))
            _thumbnail = ctk.CTkImage(thumbnail, size=(size))

            copyButton = ctk.CTkButton(app, text="Copy to clipboard", width=110, height=40, command=lambda:onCopyButton())
            downloadButton = ctk.CTkButton(app, text="Download", width=110, height=40, command=lambda:onDownloadButton())
            downloadButton.place(anchor='center', relx=0.6, rely=0.65)
            copyButton.place(anchor='center', relx=0.6, rely=0.75)
            searchButton.place_configure(relx=0.4, rely=0.7)
            thumbnail_label.configure(image=_thumbnail)
        
    
    searchButton = ctk.CTkButton(app, text="Search", width=140, height=40, command=lambda: onClickSearch())
    searchEntry.place(anchor='center', relx=0.5, rely=0.55)
    thumbnail_label.place(anchor='center', relx=0.5, rely=0.27)
    
    searchButton.place(anchor='center', relx=0.5, rely=0.7)
    app.mainloop()

gui()