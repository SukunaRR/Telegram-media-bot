from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8064503977:AAFdiBu75juk8dZqOmmmw8RMAuBPCjFDcus"  # Replace with your token
PHOTOS = [
    "https://files.catbox.moe/tp4e9f.jpg",  # Use direct image URLs
    "https://files.catbox.moe/5uothz.jpg"
]
CAPTION = "✨ *🔻𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗔𝗖𝗖𝗢𝗨𝗡𝗧🔺

♨️ACCOUNT LVL-79 HIGH' 
♨️RP:- OLD TO NEW MAX
♨️600 + UC AVAILABLE 
♨️1BIG MATERIAL

⛔ MYTHIC FASHION AVATAR [ 77/300 ]

🌟GALADRIA X-SUIT [LEVEL-2]
                  • ɪᴛᴇᴍs ᴜɴʟᴏᴄᴋ•  
        [ғʀᴀᴍᴇ,ʙᴀɢ,ᴏʀɴᴀ,ᴘᴀʀᴀᴄʜᴜᴛᴇ]

💠SET DYSTOPIAN SURVIVOR
💠SET FIEND HUNTRESS
💠SET JOKER OF SPADES
💠SET THORN TROOPER
💠SET CACTUS HAZARD
💠SET MELODIC FELINE
💠SET LAMBLING 

#WEAPON
📛M416 GLACIER LEVEL 6
📛AKM GLACIER LEVEL 4
📛UZI SAVAGERY LEVEL 4
📛GROZA RYOMEN LEVEL 2
📛UMP45 MARINE LEVEL 1
📛M16A4 THORNROSE LEVEL 1
📛UZI SPIRIT SENTRY LEVEL 1
📛SEADREAM MELODY LEVEL 1
📛NIGHTSCAPE PP-19 BIZON LEVEL 1
📛VIOLETFINESSE THOMPSON LEVEL 1
📛DBS PANTHERA PRIME LEVEL 1
📛MAGEBLAZE SLR LEVEL 1
📛FAERIE LUSTER PAN LEVEL 1
📛DRAKONBANE MACHETE LEVEL 1
📛TUNDRA KINGHT LEVEL 1
📛CROSSBOW LEVEL 1
📛GRENADE KILL MSG

#VEHICLE
🚙UAZ AVAILABLE 
🚘DACIA AVAILABLE 
🏎BUGGY AVAILABLE 
🏍️BIKE AVAILABLE 

✏️ MORE INFO CHECK SS

💵PRICE ➪  DM

🔒LOGIN ➪ SAFE

❣️  DM    ➪ @Rahool_gg* ✨"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    media_group = [
        InputMediaPhoto(media=url, caption=CAPTION if i == 0 else "")
        for i, url in enumerate(PHOTOS)
    ]
    await context.bot.send_media_group(
        chat_id=update.effective_chat.id,
        media=media_group
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
