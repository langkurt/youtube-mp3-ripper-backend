import logging

from flask import Flask, request, jsonify, Response
from youtube_rip import download_and_convert, make_youtube_dl_call
from urllib.parse import quote_plus, quote

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route("/", methods=['GET'])
def home():
    if request.method == 'HEAD':
        return get_url_metadata()
    else:
        return rip()


def rip():
    logger.info("Received call: {}".format(request))
    youtube_url = request.args.get('url')

    if not youtube_url:
        error = {
            'message': 'No Url Given'
        }
        return jsonify(error), 400

    try:
        mp3_file_name = download_and_convert(youtube_url)
        print(f"In rip(): got the mp3 file name: '{mp3_file_name}'")
        mp3_file_name = quote(mp3_file_name)
        print(f"In rip(): encoded mp3 file name: '{mp3_file_name}'")
    except Exception as e:
        print(str(e))
        error = {
            'message': "Error converting url to mp3: %s" % str(e)
        }
        return jsonify(error), 500

    response = Response()

    # "protected" is the nginx location
    response.headers["X-Accel-Redirect"] = "/protected/{}".format(mp3_file_name)
    response.headers["Content-Disposition"] = "attachment; filename={}".format(mp3_file_name)
    response.headers["Content-Type"] = "application/octet-stream"
    print("In rip() headers are: " + str(response.headers))

    return response


def get_url_metadata():
    logger.info("Received call: {}".format(request))
    youtube_url = request.args.get('url')

    if not youtube_url:
        error = {
            'message': 'No Url Given'
        }
        return jsonify(error), 400

    try:
        youtube_title = make_youtube_dl_call(youtube_url, skip_download=True)
    except Exception as e:
        print(str(e))
        error = {
            'message': "Error converting url to mp3: %s" % str(e)
        }
        return jsonify(error), 500

    # Title wont include file extension. Add it here. For now, use hardcoded "mp3"
    youtube_title = youtube_title + ".mp3"

    response = Response("{}")
    response.headers["youtube_title"] = youtube_title

    print("Returning HEAD request: {}".format(response))
    print(response.headers)
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0')
