# VoiceMed
## Demo

Demo video: https://drive.google.com/file/d/1ynQrx45MZNkRCnLfSIvtZH4IfS8kRh0z/view?usp=sharing

VoiceMed is a voice-first medical information assistant designed for hands-free interaction with basic patient information.

The project demonstrates how voice input, simple patient-data processing, and Rime text-to-speech can work together in a healthcare-oriented workflow.

> **Demo safety:** VoiceMed uses synthetic patient data only. It is a hackathon prototype and does not provide medical diagnosis or treatment recommendations.

## Key Features

* 🎤 Voice input using browser speech recognition
* 🩺 Stores basic synthetic patient information
* 🔎 Retrieves recorded patient information
* ✏️ Supports spoken corrections
* 🔊 Uses Rime for generated voice responses
* 🛑 Supports interruption and recovery during voice playback
* 🔄 Prevents stale responses from replacing newer requests
* 🛡️ Rime API credentials are kept in environment variables

## Hard Voice Challenge

The main voice-engineering challenge is **interruption and recovery**.

While VoiceMed is speaking a response using Rime, the user can start a new voice interaction and provide a correction.

The application:

1. Stops the currently playing Rime audio.
2. Captures the new voice instruction.
3. Processes the latest instruction.
4. Updates the patient information.
5. Generates a new Rime response.
6. Prevents an older response from being played as the current response.

## Example Workflow

The user can say:

**"Patient A temperature is 37.5 degrees and pulse is 110."**

VoiceMed records the synthetic patient information.

The user can then ask for Patient A's information and receive a Rime-generated response.

While the response is playing, the user can interrupt and say:

**"Correction, the temperature is 38.5 degrees Celsius."**

VoiceMed stops the previous audio, processes the correction, updates Patient A's information, and generates a new spoken response.

## Architecture

```text
User Voice
    ↓
Browser Speech Recognition
    ↓
JavaScript Frontend
    ↓
Flask Backend
    ↓
Patient Data Processing
    ↓
Rime Text-to-Speech API
    ↓
MP3 Voice Response
    ↓
Browser Playback
```

### Components

* **Frontend:** HTML, CSS, JavaScript
* **Voice Input:** Browser Speech Recognition API
* **Backend:** Python Flask
* **Text-to-Speech:** Rime TTS API
* **Patient Data:** In-memory synthetic data for the prototype

## Rime Integration

VoiceMed uses Rime as the primary voice-generation service in the demo flow.

### Current Rime Configuration

* **Endpoint:** `https://users.rime.ai/v1/rime-tts`
* **Model ID:** `coda`
* **Speaker:** `astra`
* **Language:** `en`
* **Audio format:** `audio/mpeg`
* **Transport:** HTTPS POST
* **Authentication:** Bearer API key

The API key is loaded from the server environment and is not stored in the source code.

## Project Structure

```text
VoiceMedical/
├── app.py
├── requirements.txt
├── README.md
├── RIME_EVIDENCE.md
├── .env.example
├── .gitignore
├── templates/
│   └── index.html
└── static/
    ├── script.js
    └── style.css
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/BhumikaS24/voice-medical.git
cd voice-medical
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Rime API key

Create a `.env` file:

```text
RIME_API_KEY=your_rime_api_key_here
```

Do not commit the real API key to GitHub.

### 4. Run the application

```bash
python app.py
```

Open the local application at:

```text
http://127.0.0.1:5000
```

## Testing the Voice Workflow

A basic reproducible test is:

1. Record Patient A's temperature and pulse.
2. Ask VoiceMed to retrieve the information.
3. Allow the Rime response to begin playing.
4. Press **Speak** and provide a correction.
5. Verify that the previous audio stops.
6. Verify that the corrected information is processed.
7. Retrieve Patient A's information again.
8. Verify that the corrected value is returned.

Detailed evidence for the interruption and recovery test is documented in [`RIME_EVIDENCE.md`](RIME_EVIDENCE.md).

## Limitations

* Patient information is stored only in memory and is lost when the server restarts.
* The prototype uses a Speak button to initiate interruption rather than automatic voice activity detection.
* Stale responses are fenced at the frontend playback layer.
* An already-running backend Rime request is not currently cancelled.
* Browser speech recognition support can vary by browser.
* No unverified latency or performance numbers are claimed.

## Safety and Privacy

VoiceMed is a hackathon prototype.

* Only synthetic/de-identified patient information should be used.
* The application is not intended for clinical decision-making.
* No diagnosis or treatment recommendations are provided.
* API credentials must remain in environment variables and must never be committed to the repository.
