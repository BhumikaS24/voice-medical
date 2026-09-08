import os
import uuid
import re
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Synthetic patient data for the hackathon demo
patients = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({
            "response": "I didn't hear anything."
        })

    lower_text = text.lower()

    # --------------------------------
    # FIX COMMON SPEECH RECOGNITION ERRORS
    # --------------------------------
    if "patient is" in lower_text:
        lower_text = lower_text.replace("patient is", "patient a")

    if "patient ay" in lower_text:
        lower_text = lower_text.replace("patient ay", "patient a")

    # --------------------------------
    # 1. HANDLE SPOKEN CORRECTIONS
    # --------------------------------
    if "correction" in lower_text:

        # Correct temperature
        if "temperature" in lower_text:
            temp_match = re.search(
                r"temperature\s*(?:is|of)?\s*(\d+(?:\.\d+)?)",
                lower_text
            )

            if temp_match:
                new_temperature = temp_match.group(1)

                # For the demo, correction applies to Patient A
                if "a" not in patients:
                    patients["a"] = {}

                patients["a"]["temperature"] = new_temperature

                response_text = (
                    f"Patient A's temperature has been corrected to "
                    f"{new_temperature} degrees Celsius."
                )
            else:
                response_text = (
                    "I could not identify the corrected temperature."
                )

        # Correct pulse
        elif "pulse" in lower_text or "heart rate" in lower_text:
            pulse_match = re.search(
                r"(?:pulse|heart rate)\s*(?:is|of)?\s*(\d+)",
                lower_text
            )

            if pulse_match:
                new_pulse = pulse_match.group(1)

                if "a" not in patients:
                    patients["a"] = {}

                patients["a"]["pulse"] = new_pulse

                response_text = (
                    f"Patient A's pulse has been corrected to "
                    f"{new_pulse}."
                )
            else:
                response_text = (
                    "I could not identify the corrected pulse."
                )

        else:
            response_text = (
                "Please specify what patient information should be corrected."
            )

    # --------------------------------
    # 2. RETRIEVE PATIENT INFORMATION
    # --------------------------------
    elif (
        ("what" in lower_text or "tell" in lower_text or "show" in lower_text)
        and "patient" in lower_text
    ):
        match = re.search(
            r"patient\s+([a-z0-9]+)",
            lower_text
        )

        if match:
            patient_name = match.group(1)
            patient = patients.get(patient_name, {})

            if patient:
                details = []

                if "temperature" in patient:
                    details.append(
                        f"temperature {patient['temperature']} degrees"
                    )

                if "pulse" in patient:
                    details.append(
                        f"pulse {patient['pulse']}"
                    )

                response_text = (
                    f"Patient {patient_name.upper()} has "
                    + " and ".join(details)
                    + "."
                )

            else:
                response_text = (
                    f"I don't have any recorded information for Patient "
                    f"{patient_name.upper()}."
                )

        else:
            response_text = "Please specify the patient."

    # --------------------------------
    # 3. STORE PATIENT INFORMATION
    # --------------------------------
    elif (
        "patient" in lower_text
        and (
            "temperature" in lower_text
            or "pulse" in lower_text
            or "heart rate" in lower_text
        )
    ):
        match = re.search(
            r"patient\s+([a-z0-9]+)",
            lower_text
        )

        if match:
            patient_name = match.group(1)

            if patient_name not in patients:
                patients[patient_name] = {}

            # Temperature
            temp_match = re.search(
                r"temperature\s*(?:is|of)?\s*(\d+(?:\.\d+)?)",
                lower_text
            )

            if temp_match:
                patients[patient_name]["temperature"] = (
                    temp_match.group(1)
                )

            # Pulse / heart rate
            pulse_match = re.search(
                r"(?:pulse|heart rate)\s*(?:is|of)?\s*(\d+)",
                lower_text
            )

            if pulse_match:
                patients[patient_name]["pulse"] = (
                    pulse_match.group(1)
                )

            response_text = (
                f"Patient {patient_name.upper()}'s information "
                f"has been recorded."
            )

        else:
            response_text = "Please specify the patient."

    # --------------------------------
    # 4. GENERAL MESSAGE
    # --------------------------------
    else:
        response_text = f"I heard: {text}"

    # --------------------------------
    # 5. RIME TEXT-TO-SPEECH
    # --------------------------------
    try:
        response = requests.post(
            "https://users.rime.ai/v1/rime-tts",
            headers={
                "Authorization": f"Bearer {os.environ['RIME_API_KEY']}",
                "Accept": "audio/mpeg",
            },
            json={
                "speaker": "astra",
                "text": response_text,
                "modelId": "coda",
                "lang": "en",
            },
            timeout=30
        )

        response.raise_for_status()

        filename = f"response_{uuid.uuid4().hex}.mp3"
        audio_file = os.path.join("static", filename)

        with open(audio_file, "wb") as audio:
            audio.write(response.content)

        return jsonify({
            "response": response_text,
            "audio": f"/static/{filename}"
        })

    except Exception as error:
        print("Rime error:", error)

        return jsonify({
            "response": response_text,
            "audio": None,
            "voice_error": True
        })


if __name__ == "__main__":
    app.run(debug=True)