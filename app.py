from flask import Flask, request, render_template
from pytube import YouTube
from pathlib import Path
import os
import re

app = Flask(__name__)
@app.route("/")
def index():
    return render_template('index.html')
@app.route("/download", methods=["GET","POST"])

def downloadVideo():      
    mesage = ''
    errorType = 0
    if request.method == 'POST' and 'video_url' in request.form:
        youtubeUrl = request.form["video_url"]
        if(youtubeUrl):
            validateVideoUrl = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
            validVideoUrl = re.match(validateVideoUrl, youtubeUrl)
            if validVideoUrl:
                url = YouTube(youtubeUrl)
                video = url.streams.get_highest_resolution()
                downloadFolder = str(os.path.join(Path.home(), "Downloads"))
                video.download(downloadFolder)
                mesage = 'Video Downloaded Successfully!'
                errorType = 1
            else:
                mesage = 'Enter Valid YouTube Video URL!'
                errorType = 0
        else:
            mesage = 'Enter YouTube Video Url.'
            errorType = 0            
    return render_template('index.html', mesage = mesage, errorType = errorType)

if __name__ == "__main__":
    app.run()