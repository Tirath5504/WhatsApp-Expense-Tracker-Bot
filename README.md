# WhatsApp Expense Tracker Bot

This is a WhatsApp bot that helps users track their expenses. The bot uses Twilio's WhatsApp API to receive messages and FastAPI to handle the backend logic. It can parse expense messages, categorize them, and store them in a PostgreSQL database. Users can also query their total expenses or expenses in specific categories.

## Features

- Add expenses by sending messages like "I spent ₹500 on groceries".
- Categorize expenses automatically using NLP.
- Query total expenses or expenses in specific categories.
- Store expenses in a PostgreSQL database.

## Requirements

- Python 3.11
- PostgreSQL
- Twilio account

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Tirath5504/trufides_intern_task_whatsapp_bot.git
    cd trufides_intern_task_whatsapp_bot
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the PostgreSQL database and update the connection details in [config.py](http://_vscodecontentref_/1).

5. Create a [.env](http://_vscodecontentref_/2) file in the root directory and add your Twilio credentials:
    ```env
    TWILIO_ACCOUNT_SID = "your_account_sid"
    TWILIO_AUTH_TOKEN = "your_auth_token"
    TWILIO_WHATSAPP_NUMBER = "your_whatsapp_number"
    ```

## Running the Application

1. Start the FastAPI server:
    ```sh
    uvicorn main:app --reload
    ```

2. Expose your local server to the internet using a tool like ngrok:
    ```sh
    ngrok http 8000
    ```

3. Configure your Twilio WhatsApp sandbox to use the ngrok URL as the webhook URL.

## Usage

- Send a WhatsApp message to your Twilio sandbox number to add an expense, e.g., "I spent ₹500 on groceries".
- Query your total expenses by sending a message like "What are my total expenses?".
- Query expenses in a specific category by sending a message like "How much did I spend on groceries?".

## Project Structure

- main.py: FastAPI application setup.
- routes.py: API routes for handling WhatsApp messages.
- db.py: Database models and setup.
- nlp.py: NLP functions for parsing and categorizing expenses.
- config.py: Configuration for environment variables and database connection.

## License

This project is licensed under the MIT License.
