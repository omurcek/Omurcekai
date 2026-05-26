import os
import json


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
                print(f"{len(self.responses)} responses loaded.")
            except Exception as e:
                print("JSON read error:", e)
                self.responses = []

    def save(self):
        with open("CHATBOT_DATA.json", "w", encoding="utf-8") as f:
            json.dump({"responses": self.responses}, f, ensure_ascii=False, indent=2)

    def train(self, text):
        clean = text.strip()
        if clean and len(clean) > 12 and clean not in self.responses:
            self.responses.append(clean)
