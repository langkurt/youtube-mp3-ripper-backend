from flask import Flask, request, send_from_directory, jsonify
from youtube_rip import download_and_convert, WRITABLE_DIR

app = Flask(__name__)


@app.route("/", methods=['GET'])
def rip():
    youtube_url = request.args.get('url')

    if not youtube_url:
        error = {
            'message': 'No Url Given'
        }
        return jsonify(error), 400

    try:
        mp3_file_location = download_and_convert(youtube_url)
    except Exception as e:
        print(str(e))
        error = {
            'message': "Error converting url to mp3: %s" % str(e)
        }
        return jsonify(error), 500

    send_from_directory(directory=WRITABLE_DIR, filename=mp3_file_location)
    return "Finished!", 200


if __name__ == "__main__":
    app.run(host='0.0.0.0')
