# Coffee Black

A Python bot that sends cheesy coffee messages to specified phone numbers at a random time once a day using Twilio SMS. Used as a refresher project for Python and gain some familiarity with Twilio API.

## Features

- Sends daily coffee reminders at random times between 8 AM and 11 AM
- Uses a rotating queue of coffee messages to keep content fresh
- Configurable phone numbers for message recipients
- Recovers message queue state between restarts

## Prerequisites

- Python 3.7+
- Twilio account (free trial available at [twilio.com](https://www.twilio.com))

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/bryan-gibson/coffee-black.git
   cd coffee-black
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:

   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Create a `.env` file** in the project root with the following variables:

   ```
   # Twilio credentials
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_PHONE_NUMBER="+1234567890"  # Your Twilio phone number

   # Comma-separated list of phone numbers to send messages to
   PHONE_CONTACTS="+1987654321,+1234567890"
   ```

2. **Ensure the coffee_messages.json file** in the `src/coffee_bot` directory has your coffee messages:
   ```json
   [
     "Time for a coffee break!",
     "How about some coffee right now?",
     "Coffee o'clock!",
     "You deserve a coffee break."
   ]
   ```

## Usage

Run the bot from the project root directory:

```bash
python src/coffee_bot/main.py
```

The bot will:

1. Schedule a message to be sent at a random time between 8 AM and 11 AM
2. Send the scheduled message to all phone numbers in `PHONE_CONTACTS`
3. Continue running and rescheduling daily messages

## Project Structure

```
coffee-black/
├── .env                   # Environment variables (not in git)
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── pytest.ini             # PyTest configuration
├── src/
│   └── coffee_bot/
│       ├── __init__.py    # Package initialization
│       ├── main.py        # Main application code
│       ├── coffee_messages.json     # Coffee message database
│       └── message_queue.json       # Runtime message queue state
└── tests/                 # Test files
    └── test_main.py       # Tests for main functionality
```

## Development

To run the project:

1. Set `ENV=production` in your `.env` file, otherwise `main()` will not run.
