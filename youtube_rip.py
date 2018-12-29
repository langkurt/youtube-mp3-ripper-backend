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
        }],
        'progress_hooks': [hook],
        'prefer_ffmpeg': True
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


def find_file_path(name):
    print(name)
    name += "*"
    for file in os.listdir(WRITABLE_DIR):
        if fnmatch.fnmatch(file, name):
            print(os.path.join(WRITABLE_DIR, file))
            return os.path.join(WRITABLE_DIR, file)


def download_and_convert(url):
    status = 200

    # url = "https://www.youtube.com/watch?v=TOkQytFTD4E"

    title = download_from_youtube(url=url)
    print(title)

    file_path = find_file_path(title)
    print(file_path)

    return file_path

# download_and_convert("https://www.youtube.com/watch?v=TOkQytFTD4E")
