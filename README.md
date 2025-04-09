# Telegram StoryBlocks Video Downloader Bot

A Telegram bot that allows authorized users to download videos from StoryBlocks by providing a link.

## Features

- Authentication system to control who can use the bot
- Automatic login to StoryBlocks using saved cookies
- Download links for 4K and HD video formats
- Fully dockerized setup with Chromium and ChromeDriver

## Prerequisites

- Docker and Docker Compose installed on your system
- A Telegram Bot Token (obtained from @BotFather)
- StoryBlocks account credentials

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/tgbotyara.git
   cd tgbotyara
   ```

2. Create a `.env` file based on the example:
   ```bash
   cp .env.example .env
   ```

3. Edit the `.env` file with your actual credentials:
   ```
   TG_TOKEN=your_telegram_bot_token
   PASSWORD=password_for_user_authentication
   WEB_EMAIL=your_storyblocks_email
   WEB_PASSWORD=your_storyblocks_password
   ```

## Running the Bot

### Using Docker Compose (Recommended)

Build and start the container:
```bash
docker-compose up -d
```

Stop the container:
```bash
docker-compose down
```

Check logs:
```bash
docker-compose logs -f
```

### Manual Docker Build

Build the Docker image:
```bash
docker build -t tgbot-storyblocks .
```

Run the container:
```bash
docker run -d --name tgbot-container \
  --env-file .env \
  -v "$(pwd)/cookies.pkl:/app/cookies.pkl" \
  -v "$(pwd)/users.txt:/app/users.txt" \
  tgbot-storyblocks
```

## Usage

1. Start a chat with your bot on Telegram
2. Enter the password to authenticate yourself
3. Once authenticated, send a StoryBlocks video URL
4. The bot will process the URL and send back download links for 4K and HD formats if available

## Notes

- The `cookies.pkl` file is used to store authentication cookies for StoryBlocks
- The `users.txt` file stores the list of authorized user IDs
- Both files are mounted as volumes to persist data between container restarts
