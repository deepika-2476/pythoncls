

import os
from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
import os
from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are Nova, a friendly Alexa-style voice assistant.
Reply naturally, warmly, and concisely.
Prefer short answers suitable for speaking aloud.
Help with questions, explanations, ideas, and everyday tasks.
Never claim to perform an action unless you actually did it.
"""

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nova AI Assistant</title>
<style>
* { box-sizing: border-box; }
body {
    margin: 0; min-height: 100vh; color: white;
    font-family: Arial, sans-serif;
    background: radial-gradient(circle at top, #193b65, #080d1b 65%);
    display: flex; justify-content: center; align-items: center;
}
.container {
    width: min(600px, 94%); text-align: center; padding: 28px 18px;
}
h1 { font-size: 34px; margin-bottom: 8px; }
.subtitle { color: #a9c6e8; margin-bottom: 30px; }
.orb {
    width: 170px; height: 170px; border-radius: 50%;
    margin: 25px auto; cursor: pointer;
    background: radial-gradient(circle at 35% 30%, #a9ffff, #16a9f5 35%, #1741b9 70%, #101a4d);
    box-shadow: 0 0 30px #168cff, 0 0 75px #1166cc55;
    transition: .2s;
}
.orb:hover { transform: scale(1.04); }
.orb.active { animation: pulse 1.2s infinite alternate; }
@keyframes pulse {
    from { box-shadow: 0 0 25px #168cff; }
    to { box-shadow: 0 0 75px #45d9ff; }
}
#status { color: #8feaff; min-height: 24px; }
#chat {
    text-align: left; margin: 22px 0; padding: 14px;
    height: 230px; overflow-y: auto; border-radius: 14px;
    background: #ffffff0b; border: 1px solid #ffffff20;
}
.msg { margin: 10px 0; line-height: 1.5; overflow-wrap: anywhere; }
.user { color: #a9d8ff; }
.bot { color: #fff; }
.controls { display: flex; gap: 8px; }
input {
    flex: 1; min-width: 0; padding: 14px; border-radius: 12px;
    border: 1px solid #345274; background: #101b30; color: white;
    font-size: 16px;
}
button {
    border: 0; border-radius: 12px; padding: 12px 16px;
    color: white; background: #087fe5; cursor: pointer;
    font-size: 15px;
}
button:disabled { opacity: .5; cursor: wait; }
.small { color: #91a8c5; font-size: 12px; margin-top: 18px; }
</style>
</head>
<body>
<div class="container">
    <h1>Nova AI</h1>
    <div class="subtitle">Your personal voice assistant</div>

    <div class="orb" id="orb" title="Click to speak"></div>
    <div id="status">Tap the orb and start speaking</div>

    <div id="chat" aria-live="polite">
        <div class="msg bot"><b>Nova:</b> Hello! How can I help you today?</div>
    </div>

    <form id="form" class="controls">
        <input id="message" placeholder="Ask Nova anything..." autocomplete="off">
        <button id="send" type="submit">Send</button>
    </form>
    <p class="small">Voice recognition works best in Chrome with microphone permission.</p>
</div>

<script>
const orb = document.getElementById("orb");
const statusText = document.getElementById("status");
const chat = document.getElementById("chat");
const input = document.getElementById("message");
const sendButton = document.getElementById("send");

function addMessage(who, text, className) {
    const div = document.createElement("div");
    div.className = "msg " + className;
    const bold = document.createElement("b");
    bold.textContent = who + ": ";
    div.appendChild(bold);
    div.appendChild(document.createTextNode(text));
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function speak(text) {
    if (!("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.05;
    utterance.lang = "en-US";
    window.speechSynthesis.speak(utterance);
}

async function askNova(text) {
    if (!text.trim()) return;

    addMessage("You", text, "user");
    input.value = "";
    sendButton.disabled = true;
    statusText.textContent = "Nova is thinking...";

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: text})
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "Request failed");

        addMessage("Nova", data.reply, "bot");
        statusText.textContent = "Ready for your next question";
        speak(data.reply);
    } catch (error) {
        addMessage("System", error.message, "bot");
        statusText.textContent = "Something went wrong";
    } finally {
        sendButton.disabled = false;
        input.focus();
    }
}

document.getElementById("form").addEventListener("submit", event => {
    event.preventDefault();
    askNova(input.value);
});

const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    orb.addEventListener("click", () => {
        try {
            recognition.start();
            orb.classList.add("active");
            statusText.textContent = "Listening...";
        } catch (error) {
            statusText.textContent = "Already listening. Please try again.";
        }
    });

    recognition.onresult = event => {
        const text = event.results[0][0].transcript;
        statusText.textContent = "I heard: " + text;
        askNova(text);
    };

    recognition.onerror = event => {
        statusText.textContent = "Microphone error: " + event.error;
        orb.classList.remove("active");
    };

    recognition.onend = () => orb.classList.remove("active");
} else {
    statusText.textContent =
        "Voice recognition unavailable. Try Chrome or type below.";
}
</script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")

    if not isinstance(message, str) or not message.strip():
        return jsonify(error="Please enter a message."), 400

    if len(message) > 4000:
        return jsonify(error="Message is too long."), 400

    try:
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            instructions=SYSTEM_PROMPT,
            input=message.strip()
        )
        return jsonify(reply=response.output_text.strip())

    except Exception:
        app.logger.exception("AI request failed")
        return jsonify(error="I couldn't reach the AI service. Please try again."), 502


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
