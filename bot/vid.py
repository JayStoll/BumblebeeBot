from __future__ import unicode_literals
import youtube_dl
import os

class VideoBroker():
    DB_PATH = "./db"
    MP3_PATH = os.path.join(DB_PATH, "mp3")

    def __init__(self):
        
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{self.MP3_PATH}/%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
    def setup(self):
        print ("VideoBroker initializing...")

        #Checks for database and folders
        if not os.path.isdir("./db/"):
            os.mkdir(self.DB_PATH)
            os.mkdir(os.path.join(self.MP3_PATH))

        print ("VideoBroker initialized!")
    
    def download_vids(self, urls):
    
        if not isinstance(urls, list):
            urls = [urls]

        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download(urls)