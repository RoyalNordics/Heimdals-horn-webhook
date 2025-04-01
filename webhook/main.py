from fastapi import FastAPI, Request
import os
from openai import OpenAI
from pydantic import BaseModel

app = FastAPI()

# === Gemini/OpenAI Assistant Setup ===
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_assistant_id = os.environ.get("OPENAI_ASSISTANT_ID")
client = OpenAI(api_key=openai_api_key, base_url="http://localhost:5050")

class AskRequest(BaseModel):
    message: str

@app.get("/")
async def root():
    return "Webhook is live ✅"

@app.post("/ask")
async def ask(request: Request):
    ask_request = await request.json()
    message = ask_request["message"]
    response = ask_assistant(message)
    return {"response": response}

def ask_assistant(message: str):
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=openai_assistant_id,
    )

    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(f"Run status: {run.status}")

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    response = messages.data[0].content[0].text.value
    return response

# === Nyt endpoint: webhook til Baldr ===
baldr_webhook_url = os.environ.get("BALDR_WEBHOOK_URL")

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print("🔔 Task modtaget:")
    print(data)
    # Send to Autogen
    import requests
    autogen_url = os.environ.get("AUTOGEN_WEBHOOK_URL")
    if autogen_url:
        autogen_data = {
            "agent": "Roo",
            "task_name": "Unknown",
            "status": "received",
            "result": str(data),
            "timestamp": "2025-04-01T19:05:00" # Replace with actual timestamp
        }
        try:
            response = requests.post(autogen_url, json=autogen_data)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            print("Sent to Autogen:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Error sending to Autogen:", e)
    if baldr_webhook_url:
        try:
            response = requests.post(baldr_webhook_url, json=data)
            response.raise_for_status()
            print("Sent to Baldr:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Error sending to Baldr:", e)

    return {"status": "received", "echo": data}

@app.post("/autogen_webhook")
async def autogen_webhook(request: Request):
    data = await request.json()
    print("🔔 Task modtaget fra Autogen:")
    print(data)
    return {"status": "received", "echo": data}
