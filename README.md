# yandex-cloud-tg-quiz-bot

## Description
This is a Telegram bot for conducting quizzes, developed using aiogram 3.x and YDB (Yandex Database). The bot is deployed as a serverless application using Yandex Cloud Functions.

## Live demo
```
https://t.me/edu_02_test_o_bot
```

## Main Features
- Conducting multiple-choice quizzes
- Tracking user progress
- Counting correct answers
- Displaying statistics upon quiz completion
- Ability to restart the quiz

## Tech Stack
- Python 3.x
- aiogram 3.x (asynchronous library for Telegram Bot API)
- YDB (distributed SQL-compatible database)
- Yandex Cloud Functions (serverless platform)

## Project Architecture
### Database
- The project uses two main tables:
- quiz-data-alt - stores questions, answer options, and correct answers
- quiz_state - tracks the quiz state for each user

### Main Components
1. **database.py** - module for working with YDB
- Database connection configuration
- Execution of SELECT and UPDATE queries
- Connection pool management

2. **service.py** - business logic of the application
- Generating a keyboard with answer options
- Managing quiz state
- Fetching questions and processing answers

3. **handlers.py** - bot command handlers
- Handling the /start command
- Handling the quiz start command
- Processing user answers
- Counting statistics

4. **tb_webhook.py** - webhook entry point
- Bot initialization
- Processing incoming updates
- Message routing

## Installation and Setup

### Environment Variables
```
API_TOKEN - Telegram bot token
YDB_ENDPOINT - endpoint for connecting to YDB
YDB_DATABASE - YDB database name
```

### Webhook
To set up the webhook, use the template:
```
https://api.telegram.org/bot<API_TOKEN>/setWebhook?url=<URL_API_GATEWAY>
```

## Implementation Features
- Asynchronous request processing
- Transactional safety when working with the database
- Fault tolerance through connection pooling
- Serverless architecture for resource optimization
