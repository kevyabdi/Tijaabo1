# Telegram File Saver Bot

## Overview

This is a Telegram bot that functions as a file sharing service, similar to FiletoBot. Users can send files to the bot and receive unique download links that can be shared with others. The bot stores file references using Telegram's built-in file system and provides a simple interface for file retrieval via deep links.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a simple bot-based architecture built on Python with the following key characteristics:

### Bot Framework
- **Pyrogram**: Used as the Telegram bot framework for handling messages and file operations
- **Event-driven**: Responds to user messages and commands asynchronously

### Data Storage
- **JSON File Database**: Uses a simple `files.json` file to store file ID mappings
- **Telegram File Storage**: Leverages Telegram's built-in file hosting capabilities
- **File Mapping**: Maps unique file IDs to Telegram file IDs for retrieval

### Deployment Strategy
- **Web Server**: Includes a Flask-based keep-alive server for hosting platforms
- **Environment Variables**: Supports configuration via environment variables for security

## Key Components

### 1. Main Bot (`main.py`)
- **File Handler**: Processes incoming files (documents, videos, audio, photos)
- **Start Command Handler**: Processes download requests via deep links
- **File Management**: Saves and retrieves file mappings

### 2. Database Layer (`files.json`)
- **Simple JSON Storage**: Stores file_id to unique_id mappings
- **Persistent Storage**: Maintains file references across bot restarts
- **Timestamp Tracking**: Records when files were saved

### 3. Keep-Alive Server (`keep_alive.py`)
- **Health Check Endpoint**: Provides a web interface showing bot status
- **Hosting Compatibility**: Ensures the bot stays alive on platforms like Replit/Render
- **Status Dashboard**: Shows bot features and running status

## Data Flow

### File Upload Process
1. User sends a file to the bot
2. Bot extracts file_id and file_unique_id from Telegram
3. File mapping is saved to `files.json` database
4. Bot generates a shareable deep link: `https://t.me/BotUsername?start=UNIQUE_ID`
5. Link is returned to the user

### File Download Process
1. User clicks the deep link or sends `/start UNIQUE_ID`
2. Bot parses the unique ID from the start command
3. Bot looks up the file_id in the JSON database
4. If found, bot sends the file back to the user
5. If not found, bot returns an error message

## External Dependencies

### Python Packages
- **pyrogram**: Telegram bot framework for API interactions
- **tgcrypto**: Cryptographic library for Telegram operations
- **flask**: Web server for keep-alive functionality
- **threading**: For running the web server alongside the bot

### Telegram Services
- **Telegram Bot API**: For bot authentication and message handling
- **Telegram File Storage**: For actual file hosting and retrieval

### Configuration
- **API_ID**: Telegram application ID
- **API_HASH**: Telegram application hash
- **BOT_TOKEN**: Bot authentication token from BotFather

## Deployment Strategy

### Environment Setup
- Supports both hardcoded credentials (for development) and environment variables (for production)
- Automatic database initialization if `files.json` doesn't exist
- Logging configuration for debugging and monitoring

### Hosting Platforms
- **Replit-ready**: Includes keep-alive server for continuous operation
- **Render-compatible**: Can be deployed on various cloud platforms
- **Self-hosted**: Can run on any Python-capable server

### File Management
- **No External Storage**: Uses Telegram's file system exclusively
- **Lightweight Database**: Simple JSON file for metadata storage
- **Automatic Cleanup**: Relies on Telegram's file retention policies

The architecture prioritizes simplicity and reliability, using Telegram's robust infrastructure for file storage while maintaining a minimal local database for file mapping. This approach reduces hosting costs and complexity while providing a reliable file sharing service.