import os
import json
import re
import webbrowser
from flask import Flask, request, render_template_string, jsonify
from difflib import SequenceMatcher
from collections import Counter

app = Flask(__name__)

# --- LEHNLM LOCAL PRO ENGINE ---
class LehnLM_Local:
    def __init__(self, storage_file="brain_data.json"):
        self.storage_file = storage_file
        self.texts = []
        self.word_map = {}
        self.load_data()

    def clean(self, text):
        return re.sub(r'[^\w\s]', '', str(text)).lower().strip()

    def add(self, text):
        if not text or text in self.texts: return
        self.texts.append(text)
        idx = len(self.texts) - 1
        words = self.clean(text).split()
        for w in words:
            if w not in self.word_map: self.word_map[w] = set()
            self.word_map[w].add(idx)
        self.save_data()

    def load_data(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for t in data.get("responses", []):
                        self.add(t)
            except: print("Veri yüklenemedi, yeni beyin oluşturuluyor.")

    def save_data(self):
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump({"responses": self.texts}, f, ensure_ascii=False, indent=4)
        except: pass

    def process(self, query):
        cleaned_query = self.clean(query)
        query_words = cleaned_query.split()
        if not query_words: return []

        candidate_indices = []
        for w in query_words:
            if w in self.word_map:
                candidate_indices.extend(list(self.word_map[w]))

        if not candidate_indices:
            candidates = self.texts[-100:]
        else:
            counts = Counter(candidate_indices).most_common(50)
            candidates = [self.texts[i] for i, count in counts]

        scored_results = []
        for text in candidates:
            cleaned_text = self.clean(text)
            base_ratio = SequenceMatcher(None, cleaned_query, cleaned_text).ratio()
            match_count = sum(1 for w in query_words if w in cleaned_text)
            
            # Lokal CPU gücü yüksek olduğu için daha hassas hesaplama
            final_score = base_ratio + (match_count / len(query_words)) * 0.5
            if cleaned_query in cleaned_text: final_score += 0.3
            
            scored_results.append((final_score, text))

        scored_results.sort(key=lambda x: x[0], reverse=True)
        return [scored_results[0][1]] if scored_results and scored_results[0][0] > 0.45 else []

engine = LehnLM_Local()

# --- LOKAL ÖZEL ARAYÜZ (FALLOUT GOLD EDITION) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>LOCAL_OMURCEK_OS v5.0</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
        
        :root {
            --amber: #ffb100;
            --amber-dim: #5f4200;
            --bg: #0a0a05;
        }

        body, html {
            margin: 0; padding: 0; height: 100%;
            background: var(--bg);
            color: var(--amber);
            font-family: 'VT323', monospace;
            overflow: hidden;
        }

        /* CRT Cam Efekti */
        .crt-container {
            width: 100vw; height: 100vh;
            display: flex; flex-direction: column;
            padding: 50px; box-sizing: border-box;
            position: relative;
            background: radial-gradient(circle at center, transparent 0%, rgba(0,0,0,0.6) 100%);
        }

        /* Scanlines Animasyonu */
        .crt-container::before {
            content: " ";
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.2) 50%),
                        linear-gradient(90deg, rgba(255, 0, 0, 0.02), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.02));
            z-index: 10; background-size: 100% 3px, 3px 100%; pointer-events: none;
        }

        #log {
            flex: 1; overflow-y: auto;
            text-shadow: 0 0 10px var(--amber);
            font-size: 1.8rem;
            scrollbar-width: none;
        }
        #log::-webkit-scrollbar { display: none; }

        .line { margin-bottom: 10px; opacity: 0.9; }
        .bot::before { content: "[SYS]: "; color: var(--amber-dim); }
        .user { color: #fff; text-shadow: 0 0 15px #fff; }
        .user::before { content: "[USR]: "; color: var(--amber); }

        .input-area {
            display: flex; align-items: center;
            border-top: 2px solid var(--amber-dim);
            padding-top: 20px;
            margin-top: 10px;
        }

        .prompt { font-size: 2rem; margin-right: 15px; }
        
        input {
            background: transparent; border: none;
            color: var(--amber); font-family: 'VT323', monospace;
            font-size: 2rem; flex: 1; outline: none;
            text-transform: uppercase;
        }

        /* Gürültü ve Titreme */
        @keyframes flicker {
            0% { opacity: 0.97; } 5% { opacity: 0.95; } 10% { opacity: 0.9; }
            15% { opacity: 0.98; } 100% { opacity: 1; }
        }
        .crt-container { animation: flicker 0.15s infinite; }

    </style>
</head>
<body>
    <div class="crt-container">
        <div id="log">
            <div class="line bot">LOCAL CORE INITIALIZED...</div>
            <div class="line bot">STORAGE: brain_data.json LOADED.</div>
            <div class="line bot">READY FOR INPUT.</div>
            <div class="line bot">--------------------------------------</div>
        </div>
        <div class="input-area">
            <span class="prompt">></span>
            <input type="text" id="userInput" autofocus autocomplete="off">
        </div>
    </div>

    <script>
        const log = document.getElementById('log');
        const input = document.getElementById('userInput');

        async function send() {
            const val = input.value.trim();
            if(!val) return;

            log.innerHTML += `<div class="line user">${val.toUpperCase()}</div>`;
            input.value = '';
            log.scrollTop = log.scrollHeight;

            try {
                const res = await fetch('/api', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: val})
                });
                const data = await res.json();
                
                const botDiv = document.createElement('div');
                botDiv.className = 'line bot';
                log.appendChild(botDiv);

                let i = 0;
                const msg = data.reply.toUpperCase();
                function type() {
                    if (i < msg.length) {
                        botDiv.innerHTML += msg.charAt(i);
                        i++; log.scrollTop = log.scrollHeight;
                        setTimeout(type, 10);
                    }
                }
                type();
            } catch(e) { log.innerHTML += `<div class="line" style="color:red">ERROR: CORE_LINK_LOST</div>`; }
        }
        input.onkeypress = (e) => { if(e.key === 'Enter') send(); };
        document.body.onclick = () => input.focus();
    </script>
</body>
</html>
"""

@app.route("/")
def home(): return render_template_string(HTML_TEMPLATE)

@app.route("/api", methods=["POST"])
def api():
    msg = request.json.get("text", "").strip()
    if not msg: return jsonify({"reply": "NO_SIGNAL"})
    
    res = engine.process(msg)
    reply = res[0] if res else "UNKNOWN DATA. MEMORY BUFFER UPDATED."
    
    engine.add(msg) # Her girdiğinde kendini geliştirir
    return jsonify({"reply": reply})

if __name__ == "__main__":
    # Uygulama açıldığında tarayıcıyı otomatik açar
    webbrowser.open("http://127.0.0.1:5000")
    app.run(port=5000, debug=False)