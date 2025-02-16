from groq import Groq
from sqlalchemy.orm import Session
from app.db import Expense
from dotenv import load_dotenv
import os
import re

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_amount(text):
    prompt = f"""
    Extract the **exact numeric amount** from the following expense message.
    Only return the number, nothing else. Do NOT include currency symbols or words.

    Example:
    - "I spent ₹500 at Starbucks" → 500
    - "Paid 1200 for a new phone" → 1200
    - "Bought groceries worth 350" → 350

    Now extract the amount from: "{text}"
    """
    
    response = client.chat.completions.create(
        model="llama3-8b-8192",  
        messages=[{"role": "user", "content": prompt}]
    )

    output = response.choices[0].message.content.strip()
    
    match = re.search(r"\d+(\.\d{1,2})?", output)  
    return float(match.group()) if match else None

def extract_vendor(text):
    prompt = f"""
    Identify the vendor/store where the user spent money.
    Return **only the vendor name** (no extra words).

    Example Inputs & Outputs:
    - "I spent ₹500 at Starbucks" → Starbucks
    - "Paid 1200 for a new phone on Amazon" → Amazon
    - "Bought groceries worth 350 from Big Bazaar" → Big Bazaar

    Now extract the vendor from: "{text}"
    """
    
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    vendor_name = response.choices[0].message.content.strip()
    return vendor_name if vendor_name.lower() not in ["none", "unknown"] else None

def classify_category(text):
    prompt = f"""
    Categorize the following expense message into a **single-word category** like:
    "food", "travel", "shopping", "groceries", "entertainment", "bills", "rent", or "other".
    
    Example Inputs & Outputs:
    - "Bought a burger for ₹250 at McDonald's" → food
    - "Paid ₹150 for Uber ride" → travel
    - "Spent ₹5000 on new shoes at Nike" → shopping
    - "Grocery shopping of ₹1200 at D-Mart" → groceries
    - "Paid ₹700 for Netflix subscription" → entertainment

    Now classify: "{text}"
    """
    
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    output = response.choices[0].message.content.strip().lower()
    match = re.search(r"\b(food|travel|shopping|groceries|entertainment|bills|rent|other)\b", output)

    return match.group() if match else "other"

def parse_expense(text):
    amount = extract_amount(text)
    vendor = extract_vendor(text)
    category = classify_category(text)

    if amount is None:
        return None
    
    return {"amount": amount, "category": category, "vendor": vendor}

def generate_llm_response(prompt):
    response = client.chat.completions.create(
        model="llama3-8b-8192", 
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip() if response.choices else "I couldn't process that request."


def handle_query(text, user_id, db: Session):
    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    print(expenses)
    total_spent = sum(exp.amount for exp in expenses)

    expense_summary = "\n".join(f"{exp.category}: ₹{exp.amount} at {exp.vendor or 'Unknown'}" for exp in expenses)

    prompt = f"""
    You are an intelligent financial assistant. A user is asking about their expenses. 
    Their total spending is ₹{total_spent}.
    Here are their recorded expenses:
    {expense_summary}

    Respond naturally to their query: "{text}"
    """

    return generate_llm_response(prompt)
