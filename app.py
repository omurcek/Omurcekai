import os
import json
import random
import requests
from flask import Flask, request, jsonify, render_template

from src.engine import LehnLM
from src.chatbot import OmurcekAI

app = Flask(__name__)

chatbot = OmurcekAI()
engine = LehnLM()
for resp in chatbot.responses:
    engine.add(resp)

if len(chatbot.responses) < 10:
    ornekler = [
        "Merhaba! Ben OmurcekAI, seninle sohbet etmek icin buradayim.",
        "Nasil yardimci olabilirim? Her konuda konusabiliriz!",
        "LehnLM motoru sayesinde artik cok daha dogal cevaplar veriyor!",
        "Bir web sitesi okumami ister misin? Sadece 'fetch https://ornek.com' yaz yeter.",
        "Sen ne kadar cok konusursan ben de o kadar akillaniyorum!",
    ]
    for o in ornekler:
        chatbot.train(o)
    chatbot.save()


@app.route("/chatbot")
def chatbot_page():
    return render_template("chat.html")


@app.route("/chatbot/api/free/use", methods=["POST"])
def chatbot_api():
    global engine, chatbot
    data = request.get_json()
    text = data.get("text", "").strip()
    train = data.get("train", True)
    use_lehnlm = data.get("lehnlm", True)
    temperature = float(data.get("temperature", 0.4))

    if not text:
        return "Bos mesaj gonderme lutfen."

    if text.lower().startswith("fetch "):
        try:
            url = text[6:].strip()
            if url.startswith(("http://", "https://")):
                r = requests.get(url, timeout=8)
                cevap = r.text.replace("\n", " ").replace("\r", " ")[:1400] + ("..." if len(r.text) > 1400 else "")
            else:
                cevap = "Gecerli URL gir (http:// veya https:// ile baslasin)"
        except:
            cevap = "Siteye ulasilamadi."
    else:
        if not chatbot.responses:
            cevap = "Henuz bir sey ogrenmedim, bana bir seyler soyle!"
        elif not use_lehnlm:
            cevap = random.choice(chatbot.responses)
        else:
            candidates = engine.process(text, maxlength=180, responses=max(5, int(40 * temperature)))
            if not candidates:
                cevap = random.choice(chatbot.responses)
            else:
                top_n = max(1, int(10 * temperature))
                choice = random.choice(candidates[:top_n])
                cevap = engine.restore(choice)

    if train:
        chatbot.train(text)
        chatbot.save()

    return cevap


if __name__ == "__main__":
    print("OmurcekAI running on http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
