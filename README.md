# Automated Trading Bot

An automated trading bot that integrates with Bybit exchange and Telegram for notifications and monitoring. This bot implements various trading strategies and risk management features.

## Technologies Used

### Core Technologies

- Python 3.8+
- Bybit API (pybit v5.5.0)
- Telegram API (Telethon v1.32.1)
- MongoDB (Database)
- Discord API (discord.py)

### Key Libraries

- `python-dotenv`: Environment variable management
- `pybit`: Official Bybit API client for Python
- `telethon`: Asynchronous Telegram client library
- `pandas`: Data manipulation and analysis
- `numpy`: Numerical computing
- `python-telegram-bot`: Telegram bot framework
- `pymongo`: MongoDB Python driver
- `discord.py`: Discord API wrapper

### Development Tools

- Git for version control
- Virtual Environment (venv) for dependency management
- VS Code for development

### APIs and Services

- Bybit Exchange API
- Telegram Bot API
- Telegram MTProto API
- MongoDB Atlas (Cloud Database Service)
- Discord Bot API

### Security Features

- Environment variable encryption
- API key management
- Secure session handling
- Database authentication and encryption

## Features

- Real-time position monitoring
- Automated order execution (Market, Limit, Stop Loss, Take Profit)
- Telegram integration for notifications and alerts
- Risk management with trailing stops
- Position tracking and management
- Account value monitoring

## Prerequisites

- Python 3.8+
- Bybit account with API access
- Telegram account and API credentials

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd auto-trading
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:

```env
# Bybit API Credentials
BYBIT_API_KEY=your_bybit_api_key
BYBIT_API_SECRET=your_bybit_api_secret

# Telegram API Credentials
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash
TELEGRAM_ERROR_CHAT_ID=your_error_chat_id

# Discord Bot Token
DISCORD_BOT_TOKEN=your_discord_bot_token
```

## Project Structure

- `bybit_api.py`: Core trading functionality and Bybit API integration
- `telegram.py`: Telegram bot for notifications and monitoring
- `main.py`: Main application logic and strategy implementation
- `trade.py`: Trading utilities and helper functions
- `parse.py`: Data parsing and processing utilities

## Usage

1. Configure your API credentials in the `.env` file
2. Run the main application:

```bash
python main.py
```

## Features in Detail

### Trading Functions

- Market order execution
- Limit order placement
- Stop loss and take profit management
- Position tracking
- Account value monitoring
- Trailing stop implementation

### Risk Management

- Automated stop loss placement
- Take profit targets
- Position size management
- Multiple order types support

### Monitoring

- Real-time position updates via Telegram
- Error notifications
- Account value tracking
- Price monitoring

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
