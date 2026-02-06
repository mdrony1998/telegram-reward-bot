from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import time, os

TOKEN = os.getenv("TOKEN")

users = {}
TASK_SECONDS = 180
DAILY_LIMIT = 10
REWARD = 20

def today():
    return time.strftime("%Y-%m-%d")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    users.setdefault(uid, {"date": today(),"count": 0,"task_start": 0,"reward": 0})

    kb = [[InlineKeyboardButton("🎯 Start Task", callback_data="task")]]
    await update.message.reply_text("🎁 Reward Bot Ready", reply_markup=InlineKeyboardMarkup(kb))

async def task_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    u = users[uid]

    if u["date"] != today():
        u["date"] = today()
        u["count"] = 0

    if u["count"] >= DAILY_LIMIT:
        await q.message.reply_text("Daily limit finished")
        return

    u["task_start"] = time.time()

    kb = [
        [InlineKeyboardButton("Open Sponsor Link",
         url="https://www.effectivegatecpm.com/dzj83wtgth?key=6132a511d4eac695ade5c69372fa4b71")],
        [InlineKeyboardButton("I Completed", callback_data="done")]
    ]

    await q.message.reply_text("Stay 3 min then press completed", reply_markup=InlineKeyboardMarkup(kb))

async def done_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    u = users[uid]

    if time.time() - u["task_start"] < TASK_SECONDS:
        await q.message.reply_text("Not enough time")
        return

    u["count"] += 1
    u["reward"] += REWARD
    await q.message.reply_text(f"Reward {REWARD} added")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(task_click, pattern="task"))
app.add_handler(CallbackQueryHandler(done_click, pattern="done"))
app.run_polling()
