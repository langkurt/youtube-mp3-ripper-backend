import fnmatch
import os
import json
import youtube_dl

writable_dir = "/tmp"


def download_from_youtube(url):
    print("calling download_from_youtube with " + url)

    outpath = writable_dir + '/%(title)s.%(ext)s'

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
    for file in os.listdir(writable_dir):
        if fnmatch.fnmatch(file, name):
            print(os.path.join(writable_dir, file))
            return os.path.join(writable_dir, file)


def lambda_handler(url):
    status = 200

    # url = "https://www.youtube.com/watch?v=TOkQytFTD4E"
    if not url:
        return {
            'statusCode': 400,
            'body': 'No Url Given'
        }

    try:
        result = download_from_youtube(url=url)
    except Exception as e:
        result = "Error downloading file: " + str(e)
        status = 500

    print(result)

    try:
        file_path = find_file_path(result)
        print(file_path)
    except Exception as e:
        result = "Error locating filepath: " + str(e)
        status = 500

    return {
        'statusCode': status,
        'body': json.dumps(result)
    }
