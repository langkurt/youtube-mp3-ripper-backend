import fnmatch
import os
import youtube_dl

WRITABLE_DIR = "/tmp"


def download_from_youtube(url):
    print("calling download_from_youtube with " + url)

    outpath = WRITABLE_DIR + '/%(title)s.%(ext)s'

    ydl_opts = {
        'outtmpl': outpath,
        'forcefilename': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0',
        }, {
            'key': 'EmbedThumbnail'
        }
        ],
        'progress_hooks': [hook],
        'prefer_ffmpeg': True,
        'writethumbnail': True
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        title = info_dict.get('title')
        return title


def hook(download):
    print("download is: ")
    print(download)
    if download['status'] == 'finished':
        print('Done downloading, now converting ...')


def find_file_name(name):
    print(name)
    name += "*"
    for file in os.listdir(WRITABLE_DIR):
        if fnmatch.fnmatch(file, name):
            return file


def download_and_convert(url):
    # url = "https://www.youtube.com/watch?v=TOkQytFTD4E"

    title = download_from_youtube(url=url)
    print(title)

    file_name = find_file_name(title)
    print(file_name)

    return file_name

# download_and_convert("https://www.youtube.com/watch?v=TOkQytFTD4E")
