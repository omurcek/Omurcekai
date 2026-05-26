import os
import json
from difflib import SequenceMatcher


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
                s = SequenceMatcher(None, t.lower(), p.lower()).ratio()
                candidate = text[start + lenp:start + lenp + maxlength]

                if len(candidate) < 5:
                    continue

                score = s + (len(candidate) / maxlength) * 0.3
                while score in mosts:
                    score += 1e-14
                mosts[score] = candidate

            for score, resp in mosts.items():
                while score in response_mosts:
                    score += 1e-14
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
            for known in self.words:
                sim = SequenceMatcher(None, low, known).ratio()
                if sim > best_score and sim >= minseq:
                    best_score, best = sim, known
            restored.append(best.capitalize() if best and word[0].isupper() else best or word)
        return " ".join(restored)
