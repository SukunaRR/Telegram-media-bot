from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import os
import json

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
TOKEN = '7444805320:AAFmTqe6Bnw6TO5PIxnbPvoHTP6_YqwVqhs'  # Replace with your bot token
CHANNEL_ID = -1002369652420  # Replace with your channel ID (include the -100)
POSTS_DB_FILE = 'channel_posts.json'  # File to store posts data

# Database structure: {message_id: {"file_id": "", "type": "photo|video", "caption": ""}}
channel_posts = {}

def load_posts():
    """Load posts data from file"""
    global channel_posts
    if os.path.exists(POSTS_DB_FILE):
        with open(POSTS_DB_FILE, 'r') as f:
            channel_posts = json.load(f)

def save_posts():
    """Save posts data to file"""
    with open(POSTS_DB_FILE, 'w') as f:
        json.dump(channel_posts, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message when the command /start is issued."""
    await update.message.reply_text(
        "Hello! I can share content from a private channel.\n\n"
        "Use /list to see available posts\n"
        "Use /get [number] to get a specific post"
    )

async def list_posts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List available posts with their captions"""
    if not channel_posts:
        await update.message.reply_text("No posts available yet.")
        return
    
    keyboard = []
    for i, (msg_id, post) in enumerate(channel_posts.items(), start=1):
        caption = post.get('caption', 'No caption')[:50]
        keyboard.append([InlineKeyboardButton(f"Post {i}: {caption}", callback_data=f"get_{msg_id}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Available posts:", reply_markup=reply_markup)

async def get_post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send specific post to user"""
    try:
        post_num = int(context.args[0]) if context.args else None
        if post_num is None or post_num < 1 or post_num > len(channel_posts):
            await update.message.reply_text("Please specify a valid post number. Use /list to see available posts.")
            return
        
        msg_id = list(channel_posts.keys())[post_num - 1]
        post = channel_posts[msg_id]
        
        if post['type'] == 'photo':
            await update.message.reply_photo(
                photo=post['file_id'],
                caption=post.get('caption', '')
            )
        elif post['type'] == 'video':
            await update.message.reply_video(
                video=post['file_id'],
                caption=post.get('caption', '')
            )
    except Exception as e:
        logger.error(f"Error getting post: {e}")
        await update.message.reply_text("Error getting post. Please try again.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks for post selection"""
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith('get_'):
        msg_id = query.data[4:]
        post = channel_posts.get(msg_id)
        
        if not post:
            await query.edit_message_text("This post is no longer available.")
            return
        
        try:
            if post['type'] == 'photo':
                await context.bot.send_photo(
                    chat_id=query.message.chat_id,
                    photo=post['file_id'],
                    caption=post.get('caption', '')
                )
            elif post['type'] == 'video':
                await context.bot.send_video(
                    chat_id=query.message.chat_id,
                    video=post['file_id'],
                    caption=post.get('caption', '')
                )
        except Exception as e:
            logger.error(f"Error sending post: {e}")
            await query.edit_message_text("Error sending post. Please try again.")

async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle new posts in the channel and store them"""
    channel_post = update.channel_post
    
    if channel_post.photo:
        # Get highest quality photo
        photo = sorted(channel_post.photo, key=lambda p: p.width * p.height, reverse=True)[0]
        channel_posts[str(channel_post.message_id)] = {
            'file_id': photo.file_id,
            'type': 'photo',
            'caption': channel_post.caption,
            'date': channel_post.date.isoformat()
        }
    elif channel_post.video:
        channel_posts[str(channel_post.message_id)] = {
            'file_id': channel_post.video.file_id,
            'type': 'video',
            'caption': channel_post.caption,
            'date': channel_post.date.isoformat()
        }
    else:
        return  # We only store photos and videos
    
    save_posts()
    logger.info(f"New {channel_posts[str(channel_post.message_id)]['type']} stored")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logger.error(f"Update {update} caused error {context.error}")

def main() -> None:
    """Start the bot."""
    # Load existing posts
    load_posts()
    
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("list", list_posts))
    application.add_handler(CommandHandler("get", get_post))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Handle channel posts (photos and videos)
    application.add_handler(MessageHandler(
        filters.Chat(chat_id=CHANNEL_ID) & (filters.PHOTO | filters.VIDEO),
        handle_channel_post
    ))

    # Register error handler
    application.add_error_handler(error_handler)

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
