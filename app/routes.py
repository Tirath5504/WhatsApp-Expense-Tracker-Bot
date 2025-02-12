from fastapi import APIRouter, Depends, Request
from twilio.twiml.messaging_response import MessagingResponse
from starlette.responses import Response
from sqlalchemy.orm import Session
from datetime import datetime

from app.db import SessionLocal, Expense
from app.nlp import parse_expense, handle_query
from app.utils import classify_message_type 

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/webhook")
async def whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    form = await request.form()

    user_message = form.get("Body", "")
    user_id = form.get("From", "")

    response = MessagingResponse()

    message_type = classify_message_type(user_message)

    if message_type == "expense_entry":
        expense_data = parse_expense(user_message)
        if expense_data:
            new_expense = Expense(
                user_id=user_id,
                amount=expense_data["amount"],
                category=expense_data["category"],
                vendor=expense_data["vendor"],
                date=datetime.now().date()
            )
            db.add(new_expense)
            db.commit()
            response.message(f"✅ Added: {expense_data['category']} - ₹{expense_data['amount']}.")
        else:
            response.message("❌ Could not understand the expense.")
    
    else:  
        result = handle_query(user_message, user_id, db)
        response.message(result)

    return Response(content=str(response), media_type="application/xml")
