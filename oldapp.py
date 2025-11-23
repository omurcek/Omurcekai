import difflib
import random
import json
import requests
from flask import Flask, request

app = Flask(__name__)

class OmurcekAI:
    def __init__(self):
        self.data = []
        self.words = []

    def save(self, file):
        try:
            with open(file, "w", encoding="utf-8") as f:
                f.write(json.dumps({"data": self.data, "words": self.words}))
        except:
            pass

    def load(self, file):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.loads(f.read())
                self.data = data["data"]
                self.words = data["words"]
        except:
            pass

    def train(self, text):
        self.data.append(text)
        for h in text.strip().split():
            if h not in self.words:
                self.words.append(h)

    def meaning(self, text):
        new = []
        for h in text.lower().strip().split():
            if h in self.words:
                new.append(h)
            else:
                more = "sorry"
                morevalue = 0
                for word in self.words:
                    value = difflib.SequenceMatcher(None, word, h).ratio()
                    if value > morevalue:
                        morevalue = value
                        more = word
                new.append(more)
        return " ".join(new)

    def same_think(self, prompt, text):
        newp = ""
        for h in prompt:
            if h not in "_&-+()/@#₺:;~!?.,":
                newp += h
        newt = ""
        for h in text:
            if h not in "!?., \n":
                newt += h
        correct = 0
        maxcorrect = 0
        for h in newp.split():
            if h in newt:
                correct += 1
            maxcorrect += 1
        return correct/maxcorrect if maxcorrect > 0 else 0

    def fetch_external_data(self, url):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                # Return first 500 characters to avoid huge responses
                return response.text[:500] + ("..." if len(response.text) > 500 else "")
            else:
                return f"Failed to fetch data: HTTP {response.status_code}"
        except Exception as e:
            return f"Error fetching data: {str(e)}"

    def talk(self, prompt, trainbot=True, temperature=0.2):
        if prompt == "":
            return ""

        # Check if prompt starts with 'fetch ' command
        if prompt.lower().startswith("fetch "):
            url = prompt[6:].strip()
            if not (url.startswith("http://") or url.startswith("https://")):
                return "Please provide a valid URL starting with http:// or https://"
            return self.fetch_external_data(url)

        results = []
        thinkis = ("I'm very sorry, I'm having a hard time understanding what you're saying, even though I tried hard, I couldn't understand it. Please remember to write it in a clearer language and more accurately.", 0.1)
        meaning = self.meaning(prompt)
        for text in self.data:
            value = self.same_think(meaning, text)
            if value >= thinkis[1]:
                thinkis = (text, value)
            if value >= 1-temperature:
                results.append(text)
        newprompt = ""
        upperlevel = True
        for h in prompt:
            if upperlevel:
                if h in ".,!? 1234567890_()+-/₺#@":
                    newprompt += h
                else:
                    newprompt += h.upper()
                    upperlevel = False
            else:
                if h in ".!?\"\'":
                    upperlevel = True
                    newprompt += h
                else:
                    newprompt += h.lower()
        if not (newprompt.endswith(".") or newprompt.endswith(",") or newprompt.endswith("!") or newprompt.endswith("?")):
            newprompt += "."
        if trainbot:
            self.train(newprompt)
        if len(results) == 0:
            return thinkis[0]
        else:
            return random.choice(results)

# Initialize chatbot and load data
chatbot = OmurcekAI()
chatbot.load("CHATBOT_DATA.json")

@app.route("/chatbot")
def chatbot_page():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OmurcekAI - ChatBot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #121212; /* Dark background */
            color: #FFD700; /* Gold color for text */
            margin: 0;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: auto;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
            overflow: hidden;
            background: linear-gradient(180deg, rgba(18, 18, 18, 0.9), rgba(0, 0, 0, 0.8));
        }

        h1 {
            text-align: center;
            margin-bottom: 10px;
            border-bottom: 2px solid #FFD700;
            padding-bottom: 10px;
        }

        .description {
            text-align: center;
            font-size: 0.9em;
            margin-bottom: 20px;
            padding: 10px;
        }

        .messages {
            background-color: rgba(30, 30, 30, 0.9);
            color: #FFD700;
            border: 1px solid #FFD700;
            height: 300px;
            overflow-y: auto;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
        }

        .input-container {
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
        }

        .input-field {
            width: 60%;
            padding: 10px;
            border: 1px solid #FFD700;
            border-radius: 5px;
            background-color: #1E1E1E;
            color: #FFD700;
            transition: border-color 0.3s;
        }

        .input-field:focus {
            border-color: #FF8C00; /* Lighter orange */
            outline: none;
            box-shadow: 0 0 5px rgba(255, 140, 0, 0.8);
        }

        .send-button {
            width: 25%;
            padding: 10px;
            background-color: #FFD700;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            color: black;
            transition: background-color 0.3s, transform 0.2s;
        }

        .send-button:hover {
            background-color: #FF8C00; /* Lighter orange */
            transform: scale(1.05);
        }

        .settings {
            text-align: center;
            margin-top: 20px;
            border-top: 2px solid #FFD700;
            padding-top: 10px;
        }

        .settings-header {
            margin-bottom: 20px;
        }

        .settings-label {
            display: block;
            margin: 10px 0 5px;
            font-size: 1em;
        }

        .radio-group {
            margin: 10px 0;
            display: flex;
            justify-content: center;
        }

        .radio-group label {
            margin-right: 20px;
            color: #FFD700;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>OmurcekAI - ChatBot</h1>
        <p class="description">This AI has basic training data in Turkish and English, and users can train it based on their requests.</p>

        <div id="messages" class="messages"></div>

        <div class="input-container">
            <input type="text" id="userInput" placeholder="Type your message..." class="input-field">
            <button id="sendButton" class="send-button">Send</button>
        </div>

        <div class="settings">
            <h2 class="settings-header">- - - + Chat Settings + - - -</h2>
            <label class="settings-label">Train the bot with my messages:</label>
            <div class="radio-group">
                <label><input type="radio" name="train" value="true" checked> True</label>
                <label><input type="radio" name="train" value="false"> False</label>
            </div>
            <label class="settings-label">Bot temperature (drool value):</label>
            <select id="temperatureSelect">
                <option value="0.0">0.0</option>
                <option value="0.1">0.1</option>
                <option value="0.2">0.2</option>
                <option value="0.3">0.3</option>
                <option value="0.4" selected>0.4</option>
                <option value="0.5">0.5</option>
                <option value="0.6">0.6</option>
                <option value="0.7">0.7</option>
                <option value="0.8">0.8</option>
                <option value="0.9">0.9</option>
                <option value="1.0">1.0</option>
            </select>
        </div>
    </div>

    <script>
        document.getElementById('sendButton').addEventListener('click', function() {
            const userInput = document.getElementById('userInput');
            const message = userInput.value;

            if (message.trim() === "") return; // Don't send empty messages

            // Add message to the message box
            const messagesDiv = document.getElementById('messages');
            messagesDiv.innerHTML += `<div style="text-align: right; background-color: #FFD700; color: black; padding: 5px; margin: 5px; border-radius: 5px;">${message}</div>`;

            // Reset message input
            userInput.value = '';

            // Send POST request
            const train = document.querySelector('input[name="train"]:checked').value;
            const temperature = document.getElementById('temperatureSelect').value;

            fetch('/chatbot/api/free/use', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: message,
                    train: train === "true",
                    temperature: parseFloat(temperature)
                }),
            })
            .then(response => response.text())
            .then(data => {
                // Add bot response
                messagesDiv.innerHTML += `<div style="text-align: left; background-color: black; color: #FFD700; padding: 5px; margin: 5px; border-radius: 5px;">${data}</div>`;
                messagesDiv.scrollTop = messagesDiv.scrollHeight; // Scroll to the bottom
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    </script>
</body>
</html>"""

@app.route("/chatbot/api/free/use", methods=["POST"])
def chatbot_free_use():
    global chatbot
    try:
        data = request.get_json()
        result = chatbot.talk(data["text"], trainbot=bool(data["train"]), temperature=float(data["temperature"]))
        if data["train"]:
            chatbot.save("CHATBOT_DATA.json")
        return result
    except Exception as e:
        print(e)
        return "I will have error on my system! So sorry im can't tell you what the error..."

if __name__ == "__main__":
    app.run(debug=True)
