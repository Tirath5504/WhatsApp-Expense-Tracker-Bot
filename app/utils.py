from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def classify_message_type(text):
    prompt = f"""
    Classify the following message as either "expense_entry" or "query":
    ---
    Message: "{text}"
    ---
    Only respond with either "expense_entry" or "query". No extra text.
    Example Inputs & Outputs:
    - "I spent ₹500 at Starbucks" → "expense_entry"
    - "How much did I spend on coffee this month?" -> "query"
    - "Show me my biggest expenses this week" -> "query"
    - "Paid 1200 for a new phone" → "expense_entry"
    - "List all my food expenses in January" -> "query"
    - "Bought groceries worth 350" → "expense_entry"
    """

    response = client.chat.completions.create(
        model="llama3-8b-8192",  
        messages=[{"role": "user", "content": prompt}]
    )

    message_type = response.choices[0].message.content.strip().lower()

    return message_type if message_type in ["expense_entry", "query"] else "query"
