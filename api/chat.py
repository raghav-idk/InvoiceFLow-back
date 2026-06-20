import json
import os
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Read incoming request body from your HTML front-end
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        req_body = json.loads(post_data.decode('utf-8'))
        
        # 2. Grab your Gemini API key securely from Vercel's environment variables
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "GEMINI_API_KEY environment variable is not configured on Vercel."}).encode('utf-8'))
            return

        # 3. Target the Gemini 2.5 Flash model endpoint
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={api_key}"
        
        # 4. Construct the payload for Gemini
        gemini_payload = {
            "contents": [{"parts": [{"text": req_body.get("text", "")}]}],
            "systemInstruction": {"parts": [{"text": req_body.get("systemPrompt", "")}]}
        }
        
        data = json.dumps(gemini_payload).encode('utf-8')
        
        # 5. Forward the request to Google's API
        req = urllib.request.Request(
            url, 
            data=data, 
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                res_data = response.read()
                gemini_json = json.loads(res_data.decode('utf-8'))
                
                # Extract text response from Gemini's nested structure
                reply_text = gemini_json['candidates'][0]['content']['parts'][0]['text']
                
                # Send response back to index.html
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                # Optional: Enable CORS if testing locally across different ports
                self.send_header('Access-Control-Allow-Origin', '*') 
                self.end_headers()
                
                output = {"reply": reply_text}
                self.wfile.write(json.dumps(output).encode('utf-8'))
                
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_msg = e.read().decode('utf-8')
            self.wfile.write(json.dumps({"error": "Gemini API error", "details": error_msg}).encode('utf-8'))
            
    def do_OPTIONS(self):
        # Handle preflight CORS requests for local development
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
