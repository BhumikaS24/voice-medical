# Rime Voice Evidence

## Hard Voice Challenge

VoiceMed demonstrates **interruption and recovery** during a Rime-generated voice response.

The user can interrupt an ongoing spoken response, provide a correction, and receive a new response based on the latest instruction.

## Acceptance Test

**Test scenario:** Correct a patient's temperature while a previous Rime response is playing.

### Procedure

1. Record synthetic patient information:

   * Patient A temperature: 37.5 degrees Celsius
   * Patient A pulse: 110
2. Ask VoiceMed to retrieve Patient A's information.
3. While the Rime voice response is playing, press the **Speak** button.
4. Say a correction such as:

   * "Correction, the temperature is 38.5 degrees Celsius."
5. Verify that the previous Rime audio stops.
6. Verify that the correction is processed.
7. Verify that the updated Rime response reports the corrected temperature.
8. Retrieve Patient A's information again and verify that the stored temperature is 38.5 degrees Celsius.

## Observed Result

The interruption and recovery flow worked successfully.

* The previous Rime audio stopped when the user started a new voice interaction.
* The new spoken correction was converted to text by browser speech recognition.
* VoiceMed updated the stored patient temperature.
* Rime generated a new spoken response for the correction.
* A subsequent retrieval returned the corrected temperature.

## Stale Response Protection

VoiceMed uses a request ID on the frontend to identify the latest request.

If an older request finishes after a newer request has started, its response is ignored by the frontend and is not played as the current response.

This prevents an obsolete response from replacing the latest user instruction at the playback layer.

## Rime Configuration

* **Endpoint:** `https://users.rime.ai/v1/rime-tts`
* **Model ID:** `coda`
* **Speaker:** `astra`
* **Language:** `en`
* **Output format:** `audio/mpeg`
* **Transport:** HTTPS POST request
* **Authentication:** Bearer token stored in the server environment

The Rime API key is stored in `.env` and is not committed to the repository.

## Reproducibility

The test can be repeated by running VoiceMed locally, entering or speaking the synthetic Patient A information, starting a response, interrupting it with a correction, and then retrieving the updated information.

No real patient data is used.

## Limitations

* Patient information is stored in memory for the demo and is lost when the server restarts.
* The current interruption is initiated using the Speak button rather than automatic voice activity detection.
* The frontend prevents stale responses from being played, but the backend does not currently cancel an already-running Rime HTTP request.
* No unverified latency or performance numbers are claimed.
