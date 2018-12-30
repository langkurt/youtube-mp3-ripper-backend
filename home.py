from flask import Flask, request, jsonify, Response
from youtube_rip import download_and_convert
from urllib.parse import quote

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
        mp3_file_name = download_and_convert(youtube_url)
    except Exception as e:
        print(str(e))
        error = {
            'message': "Error converting url to mp3: %s" % str(e)
        }
        return jsonify(error), 500

    response = Response()

    print("/protected/{}".format(quote(mp3_file_name)))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(mp3_file_name)
    response.headers["X-Accel-Redirect"] = "/protected/{}".format(quote(mp3_file_name))  # "protected" is the nginx location
    response.headers["Content-Type"] = "application/octet-stream"

    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0')
