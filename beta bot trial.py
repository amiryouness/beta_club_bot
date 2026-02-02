from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ================== CONFIG ==================

BOT_TOKEN = "8309158492:AAFoKJs7IyELN3OlAWnM-eV4Ku4BhQ4fDKo"

# Replace with real admin Telegram IDs
ADMINS = [1948880762]

CLUB_NAME = "BETA Scientific Club"
CLUB_DESCRIPTION = (
    "🔬 Welcome to BETA Scientific Club!\n\n"
    "We work on engineering, science, and innovation "
    "through projects, workshops, and events."
)

RESOURCES_TEXT = (
    "📚 *Club Resources*\n\n"
    "🔧 Mechanics: https://ocw.mit.edu/search/?q=mechanics\n https://www.youtube.com/@EngineeringExplained \n https://www.youtube.com/@LearnEngineering \n https://eng.libretexts.org/ \n"
    "💻 Programming: https://docs.python.org/3/tutorial/\n https://docs.python.org/3/tutorial/ \n https://www.freecodecamp.org/ \n https://www.youtube.com/@TechWithTim\n"
    "📡 Signals & Systems: https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/ \n https://www.youtube.com/@nesoacademy \n https://www.allaboutcircuits.com/ \n"
    "⚙️ Electronics: https://www.electronics-tutorials.ws/\n https://docs.arduino.cc/ \n https://www.youtube.com/@JacobSorber \n"
    "🧪 SCIENCE & RESEARCH: https://scholar.google.com/ \n https://www.researchgate.net/ \n https://www.khanacademy.org/ \n "
    "🛠️ TOOLS: https://www.desmos.com/ \n https://www.geogebra.org/ \n https://www.wolframalpha.com/ \n "
)

# ================== STORAGE ==================

# Store users who interact with the bot
USERS = set()
USERS.add ((1948880762,"amir"))
USERS.add ((5448700750,"fatma"))
USERS.add ((5174103306,"acil"))
USERS.add ((2128641027,"noureddine"))
USERS.add ((5351021557,"kaouther"))
USERS.add ((5630258540,"nourelhana"))
USERS.add ((5766178785,"tassadit"))
USERS.add ((7438910102,"insaf"))
USERS.add ((5002763550,"miled"))
USERS.add ((5017510784,"malak"))
USERS.add ((6348734085,"ahmed"))

# ================== HELPERS ==================

async def save_user(update: Update):
    user = update.effective_user
    if user:
        USERS.add((user.id, user.first_name))

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = await context.bot.get_chat_member(
        update.effective_chat.id,
        update.effective_user.id
    )
    return member.status in ["administrator", "creator"]

# ================== COMMANDS ==================

# /new
async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await save_user(update)
    text = (
        f"👋 *Welcome to {CLUB_NAME}!*\n\n"
        f"{CLUB_DESCRIPTION}\n\n"
        "📌 Use /resources to access learning materials.\n"
        "📝 Use /feedback to send suggestions."
    )
    await update.message.reply_text(text, parse_mode="Markdown")

# /resources
async def resources(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await save_user(update)
    await update.message.reply_text(RESOURCES_TEXT, parse_mode="Markdown")

# /everyone
async def everyone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await save_user(update)

    if not await is_admin(update, context):
        await update.message.reply_text("❌ Only admins can use this command.")
        return

    if not USERS:
        await update.message.reply_text("⚠️ No members to mention yet.")
        return

    mentions = ""
    for uid, name in USERS:
        mentions += f"[{name}](tg://user?id={uid}) "

    await update.message.reply_text(
        "🚨 *Attention everyone!*\n\n" + mentions,
        parse_mode="Markdown"
    )

# /feedback (start)
async def feedback_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await save_user(update)
    context.user_data["waiting_feedback"] = True
    await update.message.reply_text(
        "📝 Please send your feedback now.\n"
        "It will be sent privately to the admins."
    )

# Handle feedback messages
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await save_user(update)

    if context.user_data.get("waiting_feedback"):
        feedback_text = update.message.text
        user = update.effective_user

        admin_message = (
            "📩 *New Feedback*\n\n"
            f"👤 From: {user.full_name}\n"
            f"🆔 ID: `{user.id}`\n\n"
            f"💬 Message:\n{feedback_text}"
        )

        for admin_id in ADMINS:
            await context.bot.send_message(
                chat_id=admin_id,
                text=admin_message,
                parse_mode="Markdown"
            )

        context.user_data["waiting_feedback"] = False
        await update.message.reply_text("✅ Thank you for your feedback!")

# ================== BOT SETUP ==================

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("new", new_member))
app.add_handler(CommandHandler("resources", resources))
app.add_handler(CommandHandler("everyone", everyone))
app.add_handler(CommandHandler("feedback", feedback_start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

print("🤖 Bot is running...")
app.run_polling()
