from flask import Flask, request
from supervisor import webhook_receiver
from supervisor.task_sender import send_task

app = Flask(__name__)

@app.route("/")
def index():
    return "Baldr er online og klar til at styre dine builds ⚙️"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    result = webhook_receiver.handle(data)
    return {"status": "received", "response": result}, 200

@app.route("/send_test_task", methods=["GET"])
def send_test_task():
    success = send_task(
        task_name="Test Task fra Baldr",
        build_id=1,
        params={"note": "Dette er en test"}
    )
    if success:
        return {"status": "Task sendt til Roo ✅"}, 200
    else:
        return {"status": "Fejl ved sending ❌"}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
