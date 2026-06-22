"""
InvoiceFlow chat backend — Vercel Python serverless function (Google Gemini).

Dependency-free: calls the Gemini REST API directly with urllib, so no
requirements.txt entry is needed.

Contract (must match index.html):
  Request  POST /api/chat  { "system": "...", "messages": [ {role, content}, ... ] }
  Response 200             { "reply": "..." }
Set GEMINI_API_KEY in Vercel → Settings → Environment Variables, then redeploy.
"""

import json
import os
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler

MODEL = "gemini-2.5-flash"          # stable; avoids preview-model deprecation
MAX_OUTPUT_TOKENS = 1024
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


class handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        self._send(200, {"status": "InvoiceFlow chat endpoint. Use POST."})

    def do_POST(self):
        # 1) Read and parse the request body.
        try:
            length = int(self.headers.get("Content-Length", 0))
            req = json.loads(self.rfile.read(length) or b"{}")
        except Exception:
            return self._send(400, {"error": "Invalid JSON body."})

        # 2) Health-check used by the frontend probe — answer without calling Gemini.
        if req.get("system") == "healthcheck":
            return self._send(200, {"reply": "ok"})

        # 3) Key check.
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return self._send(503, {"error": "GEMINI_API_KEY is not configured on Vercel."})

        # 4) Build Gemini `contents` from the frontend's messages array.
        #    Gemini roles are "user" / "model" (assistant -> model).
        messages = req.get("messages") or []
        contents = []
        for m in messages:
            role = m.get("role")
            text = str(m.get("content", "")).strip()
            if role in ("user", "assistant") and text:
                contents.append({
                    "role": "model" if role == "assistant" else "user",
                    "parts": [{"text": text}],
                })
        # Backward-compat: accept a single {text:""} shape too.
        if not contents and req.get("text"):
            contents = [{"role": "user", "parts": [{"text": str(req["text"])}]}]
        if not contents:
            return self._send(400, {"error": "No messages provided."})

        payload = {
            "contents": contents,
            "generationConfig": {
                "maxOutputTokens": MAX_OUTPUT_TOKENS,
                # Gemini 2.5 "thinks" by default and can spend the whole output
                # budget on it, returning an empty reply. Turn it off here.
                "thinkingConfig": {"thinkingBudget": 0},
            },
        }
        system = str(req.get("system") or req.get("systemPrompt") or "")
        if system:
            payload["systemInstruction"] = {"parts": [{"text": system}]}

        # 5) Call Gemini.
        url = ENDPOINT.format(model=MODEL) + "?key=" + api_key
        data = json.dumps(payload).encode("utf-8")
        http_req = urllib.request.Request(
            url, data=data, headers={"Content-Type": "application/json"}, method="POST"
        )
        try:
            with urllib.request.urlopen(http_req, timeout=30) as resp:
                gj = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "ignore")
            return self._send(502, {"error": "Gemini API error", "status": e.code, "details": detail})
        except Exception as e:
            return self._send(502, {"error": "Upstream error: " + str(e)})

        # 6) Extract the text safely (guard against blocks / empty candidates).
        candidates = gj.get("candidates") or []
        if not candidates:
            block = (gj.get("promptFeedback") or {}).get("blockReason")
            return self._send(502, {"error": "No response from model" + (f" (blocked: {block})" if block else "") + "."})
        cand = candidates[0]
        parts = (cand.get("content") or {}).get("parts") or []
        reply = "".join(p.get("text", "") for p in parts).strip()
        if not reply:
            return self._send(502, {"error": "Empty reply (finishReason: " + str(cand.get("finishReason")) + ")."})

        return self._send(200, {"reply": reply})
