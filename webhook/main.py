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
@app.post("/webhook")
async def baldr_webhook(request: Request):
    data = await request.json()
    print("🔔 Task modtaget fra Baldr:")
    print(data)
    return {"status": "received", "echo": data}
