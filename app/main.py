from fastapi import FastAPI
from routes import router

app = FastAPI(title="WhatsApp Expense Tracker Bot")

app.include_router(router)

@app.get("/")
def home():
    return {"message": "WhatsApp Expense Tracker Bot is running!"}
