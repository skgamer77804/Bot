# ======================================================
# ZXERA FORCE JOIN FILE BOT
# FULL STYLISH VERSION
# ======================================================

BOT_TOKEN = "8606175656:AAH9zKrmNQsehhhaasQuVUAxBhpj8TcIcKI"

ADMIN_ID = 6258296048

# ======================================================
# CHANNELS
# ======================================================

CHANNELS = [
    {
        "name": "CHANNEL 3",
        "link": "https://t.me/SGCheats",
        "check": "@SGCheats"
    },
    {
        "name": "CHANNEL 2",
        "link": "https://t.me/sgcheats04",
        "check": "@sgcheats04"
    },
    {
        "name": "MAIN CHANNEL",
        "link": "https://t.me/+GS_EPZ0kiuliMWZl",
        "check": None
    }
]

# ======================================================

import json
import os

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# ======================================================
# FILE DATABASE
# ======================================================

DB_FILE = "files.json"

if not os.path.exists(DB_FILE):

    with open(DB_FILE, "w") as f:
        json.dump([], f)

# ======================================================
# USER DATABASE
# ======================================================

USERS_FILE = "users.json"

if not os.path.exists(USERS_FILE):

    with open(USERS_FILE, "w") as f:
        json.dump([], f)

# ======================================================

def load_files():

    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_files(data):

    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ======================================================

def load_users():

    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(data):

    with open(USERS_FILE, "w") as f:
        json.dump(data, f)

# ======================================================

async def save_user(user_id):

    users = load_users()

    if user_id not in users:

        users.append(user_id)

        save_users(users)

# ======================================================
# FORCE JOIN CHECK
# ======================================================

async def check_joined(bot, user_id):

    for channel in CHANNELS:

        if channel["check"] is None:
            continue

        try:

            member = await bot.get_chat_member(
                channel["check"],
                user_id
            )

            if member.status in ["left", "kicked"]:
                return False

        except:
            return False

    return True

# ======================================================
# START
# ======================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    await save_user(user.id)

    joined = await check_joined(
        context.bot,
        user.id
    )

    # ==========================================
    # NOT JOINED
    # ==========================================

    if not joined:

        buttons = []

        for channel in CHANNELS:

            buttons.append([
                InlineKeyboardButton(
                    f"🔥 JOIN {channel['name']} 🔥",
                    url=channel["link"]
                )
            ])

        buttons.append([
            InlineKeyboardButton(
                "✅ CHECK JOIN ✅",
                callback_data="check_join"
            )
        ])

        keyboard = InlineKeyboardMarkup(buttons)

        text = """
╔══════════════════╗
   ⚠️ ACCESS REQUIRED ⚠️
╚══════════════════╝

🚀 Bot Access Pane Ke Liye
Sabhi Channels Join Karo

✅ Join Karne Ke Baad
CHECK JOIN Button Dabao
"""

        await update.message.reply_text(
            text,
            reply_markup=keyboard
        )

        return

    await verified(update, context)

# ======================================================
# VERIFIED
# ======================================================

async def verified(update, context):

    text = """
╔══════════════════╗
   ✅ VERIFIED SUCCESSFULLY
╚══════════════════╝

🔥 Subscription Verification Successful
📂 Premium Files Unlock Ho Gayi
"""

    await update.effective_chat.send_message(text)

    await show_files(update, context)

# ======================================================
# SHOW FILES
# ======================================================

async def show_files(update, context):

    files = load_files()

    if not files:

        text = """
╔══════════════════╗
      ❌ NO FILES
╚══════════════════╝

🚫 Abhi Koi File Available Nahi Hai
"""

        await update.effective_chat.send_message(text)

        return

    buttons = []

    for item in files:

        buttons.append([
            InlineKeyboardButton(
                f"📁 {item['text']}",
                url=item["link"]
            )
        ])

    # EXTRA BUTTON

    buttons.append([
        InlineKeyboardButton(
            "🚀 JOIN ZXERA MODE 🚀",
            url="https://t.me/+GS_EPZ0kiuliMWZl"
        )
    ])

    keyboard = InlineKeyboardMarkup(buttons)

    text = f"""
╔════════════════════╗
      🔥 ZXERA FILE STORE 🔥
╚════════════════════╝

👋 Welcome Everyone ❤️ Thank you for using our bot

📂 Total Files: {len(files)}

━━━━━━━━━━━━━━━━━━

⚡ Premium Files Available
⚡ Daily Updated Links
⚡ Fast Download Access

━━━━━━━━━━━━━━━━━━

👇 Select Any File Below 👇
"""

    await update.effective_chat.send_photo(
        photo="https://i.ibb.co/zhN4XgTp/IMG-20260510-223400-468.jpg",
        caption=text,
        reply_markup=keyboard
    )

# ======================================================
# CHECK JOIN BUTTON
# ======================================================

async def check_button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    user = query.from_user

    await query.answer()

    joined = await check_joined(
        context.bot,
        user.id
    )

    # ==========================================
    # NOT JOINED MESSAGE
    # ==========================================

    if not joined:

        await query.answer(
            "❌ First Join all Channels above",
            show_alert=True
        )

        return

    # ==========================================
    # VERIFIED
    # ==========================================

    await verified(update, context)

# ======================================================
# ADD FILE
# FORMAT:
# /add Button Name | Link
# ======================================================

async def add_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    try:

        msg = update.message.text.replace(
            "/add ",
            ""
        )

        text, link = msg.split("|")

        text = text.strip()
        link = link.strip()

        data = load_files()

        data.append({
            "text": text,
            "link": link
        })

        save_files(data)

        await update.message.reply_text(
            f"""
✅ FILE ADDED SUCCESSFULLY

📁 {text}
"""
        )

    except:

        await update.message.reply_text(
            """
❌ WRONG FORMAT

Use:
 /add Button Name | Link
"""
        )

# ======================================================
# FILE LIST
# ======================================================

async def list_files(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    files = load_files()

    if not files:

        await update.message.reply_text(
            "❌ No Files Found"
        )

        return

    text = "📂 FILE LIST\n\n"

    for i, item in enumerate(files):

        text += (
            f"{i+1}. {item['text']}\n"
            f"{item['link']}\n\n"
        )

    await update.message.reply_text(text)

# ======================================================
# DELETE FILE
# ======================================================

async def delete_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    try:

        index = int(context.args[0]) - 1

        data = load_files()

        removed = data.pop(index)

        save_files(data)

        await update.message.reply_text(
            f"""
🗑 FILE DELETED

📁 {removed['text']}
"""
        )

    except:

        await update.message.reply_text(
            """
❌ USE:
 /delete 1
"""
        )

# ======================================================
# BROADCAST MESSAGE
# ======================================================

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    try:

        msg = update.message.text.replace(
            "/msg ",
            ""
        )

        users = load_users()

        success = 0

        for user_id in users:

            try:

                await context.bot.send_message(
                    chat_id=user_id,
                    text=msg
                )

                success += 1

            except:
                pass

        await update.message.reply_text(
            f"✅ Message Sent To {success} Users"
        )

    except:

        await update.message.reply_text(
            "❌ Use:\n/msg your message"
        )

# ======================================================
# MAIN
# ======================================================

app = ApplicationBuilder().token(
    BOT_TOKEN
).build()

# COMMANDS

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CommandHandler("add", add_file)
)

app.add_handler(
    CommandHandler("files", list_files)
)

app.add_handler(
    CommandHandler("delete", delete_file)
)

app.add_handler(
    CommandHandler("msg", broadcast)
)

# BUTTON

app.add_handler(
    CallbackQueryHandler(
        check_button,
        pattern="check_join"
    )
)

# ======================================================

print("🚀 ZXERA BOT RUNNING...")

app.run_polling()