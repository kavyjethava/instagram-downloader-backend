from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend Running"

@app.route("/download", methods=["POST"])
def download():

    try:

        data = request.get_json()
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
        if "entries" in info:

            for item in info["entries"]:

                media_list.append({

                    "media_url":
                    item.get("url"),

                    "thumbnail":
                    item.get("thumbnail"),

                    "type":
                    "image"
                    if item.get("ext")
                       in ["jpg", "jpeg", "png"]

                    else "video",
                })

        # Single Media
        else:

            media_list.append({

                "media_url":
                info.get("url"),

                "thumbnail":
                info.get("thumbnail"),

                "type":
                "image"
                if info.get("ext")
                   in ["jpg", "jpeg", "png"]

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

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )