from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Backend Running Successfully"


@app.route("/download", methods=["POST"])
def download():

    try:

        data = request.get_json()

        if not data or "url" not in data:
            return jsonify({
                "success": False,
                "error": "URL is required"
            })

        url = data.get("url")

        ydl_opts = {
            "quiet": True,
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                url,
                download=False,
            )

        media_list = []

        # Carousel Post
        if "entries" in info and info["entries"]:

            for item in info["entries"]:

                media_url = (
                    item.get("url")
                    or item.get("webpage_url")
                    or item.get("original_url")
                )

                media_list.append({
                    "media_url": media_url,
                    "thumbnail": item.get("thumbnail"),
                    "type":
                        "image"
                        if item.get("ext") in ["jpg", "jpeg", "png"]
                        else "video",
                })

        # Single Post / Reel
        else:

            media_url = (
                info.get("url")
                or info.get("webpage_url")
                or info.get("original_url")
            )

            media_list.append({
                "media_url": media_url,
                "thumbnail": info.get("thumbnail"),
                "type":
                    "image"
                    if info.get("ext") in ["jpg", "jpeg", "png"]
                    else "video",
            })

        return jsonify({
            "success": True,
            "media": media_list,
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e),
        })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
    )