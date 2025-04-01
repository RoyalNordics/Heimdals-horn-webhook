import requests

ROO_WEBHOOK_URL = "https://heimdals-horn-webhook.onrender.com"

def send_task(task_name, build_id, params=None):
    payload = {
        "task_name": task_name,
        "build_id": build_id,
        "params": params or {}
    }

    try:
        response = requests.post(ROO_WEBHOOK_URL, json=payload)
        print(f"[Baldr] Task sendt til Roo: {task_name}")
        print("Respons:", response.status_code, response.text)
        return True
    except Exception as e:
        print("[Baldr] Fejl ved sending til Roo:", e)
        return False
