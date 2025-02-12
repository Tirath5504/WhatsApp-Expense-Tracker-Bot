import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure()
gemini_model = genai.GenerativeModel("gemini-2.0-flash-lite-preview-02-05")

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

    response = gemini_model.generate_content(prompt)
    message_type = response.text.strip().lower()

    if message_type in ["expense_entry", "query"]:
        return message_type
    return "query"  
