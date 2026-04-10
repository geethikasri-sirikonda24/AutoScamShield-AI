from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import anthropic, os, json

load_dotenv()
app    = Flask(__name__)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

RAG_MEMORY = [
    {"pattern": "urgent account suspension",     "category": "Phishing"},
    {"pattern": "you have won a prize",           "category": "Lottery Scam"},
    {"pattern": "verify your bank details",       "category": "Banking Fraud"},
    {"pattern": "investment guaranteed returns",  "category": "Investment Scam"},
    {"pattern": "your parcel is waiting",         "category": "Delivery Scam"},
    {"pattern": "click here to claim",            "category": "Phishing"},
    {"pattern": "OTP password reset",             "category": "Account Takeover"},
    {"pattern": "you owe tax payment",            "category": "Tax Scam"},
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan-inbox", methods=["POST"])
def scan_inbox():
    data  = request.json
    gmail = data.get("gmail", "")
    if not gmail or "@" not in gmail:
        return jsonify({"error": "Invalid email"}), 400

    gen_prompt = f"""Simulate a Gmail inbox for demo purposes for user: {gmail}
Generate exactly 8 realistic emails — 4 safe, 4 scam.
Safe types: newsletter, order confirmation, meeting invite, bank statement.
Scam types: phishing, lottery, fake delivery, tax fraud.
Reply ONLY with a JSON array, no extra text:
[{{"from":"sender@example.com","subject":"Subject","preview":"First 100 chars of body","time":"2h ago"}}]"""

    gen = client.messages.create(
        model="claude-opus-4-5", max_tokens=1500,
        messages=[{"role":"user","content":gen_prompt}]
    )
    raw    = gen.content[0].text.strip().replace("```json","").replace("```","").strip()
    emails = json.loads(raw)

    results = []
    for email in emails:
        text    = (email["subject"]+" "+email["preview"]).lower()
        matched = next((r for r in RAG_MEMORY if any(w in text for w in r["pattern"].split())), None)
        rag_ctx = f"Similar: {matched['category']}" if matched else "No match."

        analyze = f"""Analyze this email for scams.
From: {email['from']}
Subject: {email['subject']}
Preview: {email['preview']}
RAG: {rag_ctx}
Reply ONLY with JSON: {{"is_scam":true/false,"risk_score":0-100,"category":"name","reason":"1 sentence","action":"Block/Quarantine/Deliver"}}"""

        res = client.messages.create(
            model="claude-opus-4-5", max_tokens=200,
            messages=[{"role":"user","content":analyze}]
        )
        a = json.loads(res.content[0].text.strip().replace("```json","").replace("```","").strip())
        results.append({**email, **a, "rag_match": rag_ctx})

    return jsonify({"gmail": gmail, "emails": results})

@app.route("/simulate", methods=["POST"])
def simulate():
    try:
        data    = request.json
        subject = data.get("subject","No Subject")
        body    = data.get("email","")
        matched = next((r for r in RAG_MEMORY if any(w in body.lower() for w in r["pattern"].split())), None)
        rag_ctx = f"Similar: {matched['category']}" if matched else "No match."

        prompt = f"""Analyze this email for scams.
Subject: {subject}
Body: {body}
RAG: {rag_ctx}
Reply ONLY with JSON: {{"is_scam":true/false,"risk_score":0-100,"category":"name","reasoning":"1 sentence","action":"Block/Quarantine/Deliver"}}"""

        msg    = client.messages.create(
            model="claude-opus-4-5", max_tokens=300,
            messages=[{"role":"user","content":prompt}]
        )
        result = json.loads(msg.content[0].text.strip().replace("```json","").replace("```","").strip())
        result["subject"]   = subject
        result["rag_match"] = rag_ctx
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)