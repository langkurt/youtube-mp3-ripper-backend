from flask import Flask, request
from youtube_rip import lambda_handler, serve_mp3_file

app = Flask(__name__)

@app.route("/",  methods=['GET'])
def rip():
    youtube_url = request.args.get('url')
    return f"Url is {youtube_url}", 200

    if not youtube_url:
        return {
            'statusCode': 400,
            'body': 'No Url Given'
        }

    try:
        mp3_file_location = lambda_handler(youtube_url)
    except Exception as e:
        print(str(e))
        return {
            'statusCode': 500,
            'body': "Error converting url to mp3: %s" % str(e)
        }

    serve_mp3_file(mp3_file_location)
    return "Hello World!", 200


if __name__ == "__main__":
    app.run(host='0.0.0.0')
