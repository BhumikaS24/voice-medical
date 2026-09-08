import os
import uuid
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"response": "I didn't hear anything."})

    # Rime Text-to-Speech
    response = requests.post(
        "https://users.rime.ai/v1/rime-tts",
        headers={
            "Authorization": f"Bearer {os.environ['RIME_API_KEY']}",
            "Accept": "audio/mpeg",
        },
        json={
            "speaker": "astra",
            "text": f"I heard: {text}",
            "modelId": "coda",
            "lang": "en",
        },
    )

    response.raise_for_status()

    # Give every response a unique audio filename
    filename = f"response_{uuid.uuid4().hex}.mp3"
    audio_file = os.path.join("static", filename)

    with open(audio_file, "wb") as audio:
        audio.write(response.content)

    return jsonify({
        "response": f"I heard: {text}",
        "audio": f"/static/{filename}"
    })


if __name__ == "__main__":
    app.run(debug=True)