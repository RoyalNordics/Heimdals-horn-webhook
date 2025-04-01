from fastapi import FastAPI
import os
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Heimdal Webhook is live!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))