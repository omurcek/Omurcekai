import os
import json
import random
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

class LehnLM:
    def __init__(self):
        self.texts = []
        self.words = set()

    def add(self, text):
        if text not in self.texts:
            self.texts.append(text)
            self.words.update(text.lower().split())

    def process(self, p, maxlength=180, responses=30, spaces=None):
        response_mosts = {}
        lenp = len(p)
        spaces = max(8, min(32, lenp // 4)) if spaces is None else spaces

        for text in self.texts:
            mosts = {}
            lentext = len(text)
            step = max(1, lentext // spaces)

            for n in range(0, lentext, step):
                start = max(0, n - lenp)
                t = text[start:start + lenp]
                from difflib import SequenceMatcher
                s = SequenceMatcher(None, t.lower(), p.lower()).ratio()
                candidate = text[start + lenp:start + lenp + maxlength]

                if len(candidate) < 5:
                    continue

                score = s + (len(candidate) / maxlength) * 0.3
                while score in mosts: score += 1e-14
                mosts[score] = candidate

            for score, resp in mosts.items():
                while score in response_mosts: score += 1e-14
                response_mosts[score] = resp

        sorted_responses = sorted(response_mosts.items(), key=lambda x: x[0], reverse=True)
        return [resp for _, resp in sorted_responses[:responses]]

    def restore(self, text, minseq=0.65):
        words = text.split()
        restored = []
        for word in words:
            low = word.lower()
            if low in self.words:
                restored.append(word)
                continue
            best, best_score = None, 0
            from difflib import SequenceMatcher
            for known in self.words:
                sim = SequenceMatcher(None, low, known).ratio()
                if sim > best_score and sim >= minseq:
                    best_score, best = sim, known
            restored.append(best.capitalize() if best and word[0].isupper() else best or word)
        return " ".join(restored)

class OmurcekAI:
    def __init__(self):
        self.responses = []
        self.load()

    def load(self):
        if os.path.exists("CHATBOT_DATA.json"):
            try:
                with open("CHATBOT_DATA.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.responses = [r.strip() for r in data.get("responses", []) if len(r.strip()) > 12]
                print(f"{len(self.responses)} kaliteli yanıt yüklendi.")
            except Exception as e:
                print("JSON okuma hatası:", e)
                self.responses = []

    def save(self):
        with open("CHATBOT_DATA.json", "w", encoding="utf-8") as f:
            json.dump({"responses": self.responses}, f, ensure_ascii=False, indent=2)

    def train(self, text):
        clean = text.strip()
        if clean and len(clean) > 12 and clean not in self.responses:
            self.responses.append(clean)
            engine.add(clean)  

chatbot = OmurcekAI()
engine = LehnLM()
for resp in chatbot.responses:
    engine.add(resp)

if len(chatbot.responses) < 10:
    ornekler = [
        "Merhaba! Ben OmurcekAI, seninle sohbet etmek için buradayım.",
        "Nasıl yardımcı olabilirim? Her konuda konuşabiliriz!",
        "LehnLM motoru sayesinde artık çok daha doğal cevaplar veriyor!",
        "Bir web sitesi okumamı ister misin? Sadece 'fetch https://ornek.com' yaz yeter.",
        "Sen ne kadar çok konuşursan ben de o kadar akıllanıyorum!",
    ]
    for o in ornekler:
        chatbot.train(o)
    chatbot.save()


@app.route("/chatbot")
def chatbot_page():
    return """<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>OmurcekAI - ChatBot</title>
 <script async src="https://www.googletagmanager.com/gtag/js?id=G-RD06WE730X"></script>
<script>
 window.dataLayer = window.dataLayer || [];
 function gtag(){dataLayer.push(arguments);}
 gtag('js', new Date());
 gtag('config', 'G-RD06WE730X');
</script>
 <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
 <style>
  html, body {height:100%; margin:0; padding:0;}
  body {font-family:'Roboto',sans-serif;background:#000;color:#FFD700;display:flex;justify-content:center;align-items:center;}

  .container{width:100%;height:100%;max-width:1920px;max-height:1080px;display:flex;flex-direction:column;justify-content:flex-start;align-items:center;border-radius:12px;box-shadow:0 0 30px rgba(255,215,0,.08);background:linear-gradient(180deg,#050505 0%, #0b0b0b 100%);padding:28px;box-sizing:border-box;}

  .header-row{width:100%;display:flex;flex-direction:column;align-items:center;gap:6px;margin-bottom:6px}
  h1{margin:6px 0 0;color:#FFD700;text-shadow:0 0 10px rgba(255,215,0,.15);font-size:28px}

  .warning{max-width:980px;width:94%;text-align:center;font-size:0.92rem;color:#ffb3b3;background:rgba(255,85,85,0.03);padding:8px 12px;border-radius:8px;border:1px solid rgba(255,85,85,0.08);box-shadow:inset 0 1px 0 rgba(255,85,85,0.02);}
  .description{margin-top:6px;text-align:center;font-size:.92rem;padding:6px;color:#FFD700;opacity:.95}

  .messages{flex-grow:1;width:100%;background:#0d0d0d;border:1px solid rgba(255,215,0,0.06);overflow-y:auto;padding:12px;margin:18px 0;border-radius:10px;box-shadow:inset 0 0 20px rgba(255,215,0,.02);min-height:220px}
  .message-user{text-align:right;background:linear-gradient(135deg,#FFD700,#FFB700);color:#000;padding:8px 12px;margin:8px 0;border-radius:15px 15px 0 15px;max-width:70%;margin-left:auto;word-wrap:break-word;box-shadow:0 0 12px rgba(255,215,0,.15);}
  .message-bot{text-align:left;background:rgba(255,215,0,.06);color:#FFD700;padding:8px 12px;margin:8px 0;border-radius:15px 15px 15px 0;max-width:70%;margin-right:auto;word-wrap:break-word;box-shadow:0 0 8px rgba(255,215,0,.08);}

  .input-container{display:flex;justify-content:space-between;width:100%;gap:12px;margin-bottom:8px}
  .input-field{flex-grow:1;padding:12px;border:1px solid rgba(255,215,0,.12);border-radius:8px;background:transparent;color:#FFD700;transition:box-shadow .25s, background .25s;font-size:15px}
  .input-field:focus{outline:none;box-shadow:0 0 28px rgba(255,215,0,.18);background:#0b0b0b}
  .input-field.typing{box-shadow:0 0 28px rgba(255,215,0,.28);}

  .send-button{width:110px;padding:10px 12px;background:#FFD700;border:none;border-radius:8px;cursor:pointer;color:#000;font-weight:700;transition:transform .14s,box-shadow .18s;font-size:15px}
  .send-button:hover{transform:translateY(-2px);box-shadow:0 6px 30px rgba(255,215,0,.18)}
  .send-button:active{animation:glowPulse .9s ease}

  .settings{width:100%;margin-top:12px;border-top:1px dashed rgba(255,215,0,.06);padding-top:14px;display:flex;flex-direction:column;align-items:center;gap:10px}
  .settings-header{color:#FFD700;font-weight:600;margin-bottom:0}
  .train-row{display:flex;align-items:center;gap:12px;justify-content:center;flex-wrap:wrap}
  .train-row .train-label{color:#FFD700;font-size:15px;margin:0}

  .toggle-switch{position:relative;display:inline-block;width:60px;height:34px}
  .toggle-switch input{opacity:0;width:0;height:0}
  .slider{position:absolute;cursor:pointer;top:0;left:0;right:0;bottom:0;background:#222;border:1px solid rgba(255,215,0,.12);transition:.35s;border-radius:34px}
  .slider:before{position:absolute;content:"";height:26px;width:26px;left:4px;bottom:3px;background:#FFD700;transition:.35s;border-radius:50%;box-shadow:0 6px 18px rgba(255,215,0,.10)}
  .toggle-switch input:checked + .slider{background:#FFD700;box-shadow:0 0 28px rgba(255,215,0,.16)}
  .toggle-switch input:checked + .slider:before{transform:translateX(26px);background:#000;box-shadow:0 10px 30px rgba(255,215,0,.18);animation:glowPulse 1.4s infinite alternate}

  .temp-row{display:flex;align-items:center;gap:12px;justify-content:center}
  select{appearance:none;-webkit-appearance:none;-moz-appearance:none;padding:10px 14px;border-radius:999px;border:1px solid rgba(255,215,0,.12);background:linear-gradient(180deg,#0b0b0b,#0d0d0d);color:#FFD700;cursor:pointer;font-weight:600}
  .select-wrap{position:relative}
  .select-wrap:after{content:"▾";position:absolute;right:12px;top:9px;color:#FFD700;pointer-events:none}
  select:hover{box-shadow:0 8px 26px rgba(255,215,0,.06)}
  select:focus{outline:none;box-shadow:0 0 30px rgba(255,215,0,.12)}

  /* Butonlar */
  .manifest-row{margin-top:10px;}
  .manifest-button{padding:10px 18px;border:none;border-radius:8px;background:linear-gradient(135deg,#FFD700,#FFB700);color:#000;font-weight:700;cursor:pointer;transition:transform 0.15s,box-shadow 0.2s;box-shadow:0 0 18px rgba(255,215,0,0.08);}
  .manifest-button:hover{transform:translateY(-2px);box-shadow:0 6px 28px rgba(255,215,0,0.18);}
  .manifest-button:active{transform:translateY(0);box-shadow:0 0 14px rgba(255,215,0,0.25);}

  .buttons-row {display:flex;justify-content:center;align-items:center;gap:12px;margin-top:10px;}

  .usermap-button {background:linear-gradient(135deg,#00aaff,#0077ff);color:#fff;box-shadow:0 0 18px rgba(0,136,255,0.25);}
  .usermap-button:hover{transform:translateY(-2px);box-shadow:0 6px 28px rgba(0,136,255,0.45);}
  .usermap-button:active{transform:translateY(0);box-shadow:0 0 14px rgba(0,136,255,0.5);}

.privacy-button {background:linear-gradient(135deg,#BF2C2C,#B01E1E);color:#fff;box-shadow:0 0 18px rgba(204, 14, 14, 0.8);}
.privacy-button:hover{transform:translateY(-2px);box-shadow:0 6px 28px rgba(204, 14, 14, 0.8);}
.privacy-button:active{transform:translateY(0);box-shadow:0 0 14px rgba(204, 14, 14, 0.8);}

  @keyframes glowPulse{from{box-shadow:0 0 8px rgba(255,215,0,.12)}to{box-shadow:0 0 28px rgba(255,215,0,.28)}}

  .modal-overlay{position:fixed;inset:0;display:none;align-items:center;justify-content:center;background:rgba(0,0,0,.7);z-index:1200}
  .modal{width:min(720px,92%);background:linear-gradient(180deg,#060606,#0b0b0b);border:1px solid rgba(255,215,0,.12);padding:22px;border-radius:12px;text-align:center;color:#FFD700;box-shadow:0 10px 50px rgba(0,0,0,.6)}
  .modal h3{margin:0 0 8px;color:#fff}
  .modal p{color:#ffd6d6;margin:0 0 14px}
  .modal .btn{display:inline-block;padding:10px 16px;border-radius:10px;background:#FFD700;color:#000;border:none;cursor:pointer;font-weight:700;box-shadow:0 8px 30px rgba(255,215,0,.12)}
  .modal .controls{margin-top:8px;display:flex;gap:12px;align-items:center;justify-content:center}
  .modal label{color:#ffd6d6;font-size:14px}
 </style>
</head>
<body>
 <div class="container">
  <div class="header-row">
   <h1>OmurcekAI 🗁</h1>
   <div class="warning">⚠ This is an AI — we can't control what it learns or says. Responsibility is not ours.</div>
   <div class="description">Train, chat & vibe with this AI. Use <b>fetch [URL]</b>!</div>
  </div>

  <div id="messages" class="messages"></div>

  <div class="input-container">
   <input type="text" id="userInput" placeholder="Type your message..." class="input-field" autocomplete="off">
   <button id="sendButton" class="send-button">Send</button>
  </div>

  <div class="settings">
   <div class="settings-header">⚙ Chat Settings</div>

   <div class="train-row">
    <div class="train-label">Train the bot with my messages:</div>
    <label class="toggle-switch"><input type="checkbox" id="trainToggle" checked><span class="slider"></span></label>
    <div class="train-label">LehnLM:</div>
    <label class="toggle-switch"><input type="checkbox" id="lehnlmToggle"><span class="slider"></span></label>
   </div>

   <div class="temp-row">
    <div class="select-wrap"><select id="temperatureSelect"><option value="0.0">0.0 (Precise)</option><option value="0.15">0.15 (Smart)</option><option value="0.4" selected>0.4 (Default)</option><option value="0.7">0.7 (Creative)</option><option value="1.0">1.0 (Wild)</option></select></div>
   </div>

   <div class="manifest-row buttons-row">
    <button id="manifestBtn" class="manifest-button">Manifest</button>
    <button id="userMapBtn" class="manifest-button usermap-button">User Map</button>
    <button id="privacyBtn" class="manifest-button privacy-button">Privacy Policy</button>
   </div>
  </div>
 </div>

 <div id="modalOverlay" class="modal-overlay">
  <div class="modal">
   <h3>Important — Read before using</h3>
   <p>This is an AI. We cannot control what it learns or says. We are not responsible for outputs generated by this bot.</p>
   <div class="controls">
    <label><input type="checkbox" id="dontShow"> Don't show again</label>
   </div>
   <div style="margin-top:14px"><button id="understandBtn" class="btn">I understand</button></div>
  </div>
 </div>

 <script>
  const modal = document.getElementById('modalOverlay');
  const dontShow = localStorage.getItem('hideAiWarning');
  if (!dontShow) {
   modal.style.display = 'flex';
  }
  document.getElementById('understandBtn').addEventListener('click', ()=>{
   if(document.getElementById('dontShow').checked){
    localStorage.setItem('hideAiWarning', '1');
   }
   modal.style.display='none';
  });

  document.getElementById('sendButton').addEventListener('click', function(){
   const userInput = document.getElementById('userInput');
   const message = userInput.value;
   if (message.trim() === '') return;
   const messagesDiv = document.getElementById('messages');
   messagesDiv.innerHTML += `<div class="message-user">${message}</div>`;
   messagesDiv.scrollTop = messagesDiv.scrollHeight;
   userInput.value = '';

   const train = document.getElementById('trainToggle').checked;
   const lehnlm = document.getElementById('lehnlmToggle').checked;
   const temperature = document.getElementById('temperatureSelect').value;

   fetch('/chatbot/api/free/use', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: message, train: train, lehnlm: lehnlm, temperature: parseFloat(temperature) })
   })
   .then(r => r.text())
   .then(d => {
    messagesDiv.innerHTML += `<div class="message-bot">${d}</div>`;
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
   })
   .catch(e => {
    messagesDiv.innerHTML += `<div class="message-bot" style="color:red;">Error: ${e.message}</div>`;
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
   });

   const btn = document.getElementById('sendButton');
   btn.classList.add('active');
   setTimeout(()=>btn.classList.remove('active'), 800);
  });

  let typingTimer;
  const input = document.getElementById('userInput');
  input.addEventListener('input', ()=>{
   input.classList.add('typing');
   clearTimeout(typingTimer);
   typingTimer = setTimeout(()=>{ input.classList.remove('typing'); }, 800);
  });

  input.addEventListener('keydown', (e)=>{
   if(e.key === 'Enter'){
    e.preventDefault();
    document.getElementById('sendButton').click();
   }
  });

  document.getElementById('manifestBtn').addEventListener('click', () => {
   window.location.href = '/chatbot/manifest';
  });

  document.getElementById('userMapBtn').addEventListener('click', () => {
   window.location.href = '/chatbot/map';
  });

   document.getElementById('privacyBtn').addEventListener('click', () => {
   window.location.href = '/privacy';
  });
 </script>
</body>
</html>
"""


@app.route("/chatbot/api/free/use", methods=["POST"])
def chatbot_api():
    global engine, chatbot
    data = request.get_json()
    text = data.get("text", "").strip()
    train = data.get("train", True)
    use_lehnlm = data.get("lehnlm", True)
    temperature = float(data.get("temperature", 0.4))

    if not text:
        return "Boş mesaj gönderme lütfen."

    if text.lower().startswith("fetch "):
        try:
            url = text[6:].strip()
            if url.startswith(("http://", "https://")):
                r = requests.get(url, timeout=8)
                cevap = r.text.replace("\n", " ").replace("\r", " ")[:1400] + ("..." if len(r.text) > 1400 else "")
            else:
                cevap = "Geçerli URL gir (http:// veya https:// ile başlasın)"
        except:
            cevap = "Siteye ulaşılamadı."
    else:
        if not chatbot.responses:
            cevap = "Henüz bir şey öğrenmedim, bana bir şeyler söyle!"
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
    print("OmurcekAI ÇALIŞIYOR → http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)