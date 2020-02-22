import fnmatch
import os
import youtube_dl

WRITABLE_DIR = "/tmp"


class NameStorage:
    def __init__(self):
        self.filename = ""

    def save_name(self, download):
        name = download['filename']
        name = name.rsplit(".", 1)[0]
        self.filename = name


name_container = NameStorage()


def make_youtube_dl_call(url, skip_download=False):
    print("calling download_from_youtube with " + url + ". Skip_download is set to " + str(skip_download))

    outpath = WRITABLE_DIR + '/%(title)s.%(ext)s'

    if skip_download:
        ydl_opts = {
            'outtmpl': outpath,  # Template for output names
            'forcefilename': True,  # Force printing final filename.
            'skip_download': True
        }
    else:
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
            }],
            'progress_hooks': [post_download_callback],
            'prefer_ffmpeg': True,
            'writethumbnail': True
        }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        download = not skip_download
        info_dict = ydl.extract_info(url, download=download)
        title = info_dict.get('title')
        return title


def post_download_callback(download):
    print("download is: ")
    print(download)
    name_container.save_name(download)
    # webm location in temp is located at download['filename']. capture with closure?
    if download['status'] == 'finished':
        print('Done downloading, now converting ...')


def find_file_name(name):
    print("Passed in file name to find: {}".format(name))
    print("Screw it, using some name container class to find: " + name_container.filename)
    name = name_container.filename
    name = name.split('/')[-1]
    glob_name = name + "*"
    for file in os.listdir(WRITABLE_DIR):
        print(f"Seaching file: '{file}'")
        if fnmatch.fnmatch(file, glob_name):
            print("File located: {}".format(file))
            return file
    else:
        print("Warning: Could not find file `{}`, using hardcoded .mp3".format(name))
        return name + ".mp3"


def download_and_convert(url):
    # url = "https://www.youtube.com/watch?v=TOkQytFTD4E"

    title = make_youtube_dl_call(url=url)
    print(title)

    file_name = find_file_name(title)
    print(file_name)

    return file_name

# download_and_convert("https://www.youtube.com/watch?v=TOkQytFTD4E")
