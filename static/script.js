let currentAudio = null;
let requestId = 0;

// Send typed or spoken text to the backend
async function sendText() {
    const input = document.getElementById("textInput");
    const response = document.getElementById("response");

    const text = input.value.trim();

    if (!text) {
        response.innerText = "Please enter or speak something.";
        return;
    }

    requestId++;
    const thisRequest = requestId;

    // Stop previous Rime audio
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
        currentAudio = null;
    }

    response.innerText = "Processing...";

    const result = await fetch("/process", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: text })
    });

    const data = await result.json();

    // Ignore old responses
    if (thisRequest !== requestId) {
        return;
    }

    response.innerText = data.response;

    // Play newest Rime response
    if (data.audio) {
        currentAudio = new Audio(data.audio);
        currentAudio.play();
    }
}


// 🎤 Voice input
function startListening() {
    // Stop Rime voice immediately when the user interrupts
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
        currentAudio = null;
    }
    const input = document.getElementById("textInput");
    const response = document.getElementById("response");

    const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        response.innerText = "Voice input is not supported in this browser.";
        return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.continuous = false;

    response.innerText = "Listening... 🎤";

    recognition.start();

    recognition.onresult = function(event) {
        const spokenText = event.results[0][0].transcript;

        input.value = spokenText;

        sendText();
    };

    recognition.onerror = function(event) {
        response.innerText = "Could not understand voice input. Please try again.";
        console.log(event.error);
    };
}