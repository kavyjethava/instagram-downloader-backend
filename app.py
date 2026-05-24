from flask import Flask, request, jsonify
import yt_dlp
app = Flask(__name__)

@app.route("/download", methods=["POST"])
def download():
    data  = request.get_json()
    url = data.get("url")
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      info = ydl.extract_info(url, download=False)
    video_url = info.get("url")
    print(video_url)
    print(url)
    return jsonify({
    "video_url": video_url
})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)