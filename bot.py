from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import os

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
TOKEN = '7444805320:AAFmTqe6Bnw6TO5PIxnbPvoHTP6_YqwVqhs'  # Replace with your bot token
CHANNEL_ID = -1002369652420  # Replace with your channel ID (include the -100)
LAST_PHOTO_FILE = 'last_photo.txt'  # File to store the last photo info

# Store the last photo details
last_photo = {'file_id': None, 'caption': None}

def save_last_photo():
    """Save the last photo info to file"""
    with open(LAST_PHOTO_FILE, 'w') as f:
        f.write(f"{last_photo['file_id']}\n{last_photo['caption'] or ''}")

def load_last_photo():
    """Load the last photo info from file"""
    if os.path.exists(LAST_PHOTO_FILE):
        with open(LAST_PHOTO_FILE, 'r') as f:
            lines = f.readlines()
            if len(lines) >= 2:
                last_photo['file_id'] = lines[0].strip()
                last_photo['caption'] = lines[1].strip() if lines[1].strip() else None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message when the command /start is issued."""
    await update.message.reply_text(
        "Hello! Use /getphoto to receive the latest photo from our private collection."
    )

async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the last photo to the user"""
    if not last_photo['file_id']:
        await update.message.reply_text("No photos available yet.")
        return
    
    try:
        if last_photo['caption']:
            await update.message.reply_photo(
                photo=last_photo['file_id'],
                caption=last_photo['caption']
            )
        else:
            await update.message.reply_photo(photo=last_photo['file_id'])
    except Exception as e:
        logger.error(f"Error sending photo: {e}")
        await update.message.reply_text("Sorry, couldn't send the photo. Please try again later.")

async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle new posts in the channel"""
    channel_post = update.channel_post
    
    # Check if the post contains a photo
    if channel_post.photo:
        # Get the highest quality photo
        photo = sorted(channel_post.photo, key=lambda p: p.width * p.height, reverse=True)[0]
        
        # Store the photo details
        last_photo['file_id'] = photo.file_id
        last_photo['caption'] = channel_post.caption
        
        # Save to file
        save_last_photo()
        
        logger.info("New photo stored in channel")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logger.error(f"Update {update} caused error {context.error}")

def main() -> None:
    """Start the bot."""
    # Load the last photo if it exists
    load_last_photo()
    
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("getphoto", get_photo))

    # Handle channel posts
    application.add_handler(MessageHandler(filters.Chat(chat_id=CHANNEL_ID) & filters.PHOTO, handle_channel_post))

    # Register error handler
    application.add_error_handler(error_handler)

    # Run the bot until you press Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
