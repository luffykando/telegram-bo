import asyncio
import requests
import json
import urllib3
from bs4 import BeautifulSoup
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes




def get_jobs():
    res = requests.get(URL, verify=False)
    soup = BeautifulSoup(res.text, "html.parser")

    jobs = []
    for text in soup.stripped_strings:
        if "Advertisement" in text and "posts" in text:
            jobs.append(text)

    return jobs

# 💾 Load saved jobs
def load_old_jobs():
    try:
        with open("jobs.json", "r") as f:
            return json.load(f)
    except:
        return []

# 💾 Save jobs
def save_jobs(jobs):
    with open("jobs.json", "w") as f:
        json.dump(jobs, f)

# 🤖 Command: /job
async def job_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jobs = get_jobs()
    if not jobs:
        await update.message.reply_text("No jobs found.")
    else:
        for job in jobs[:10]:
            await update.message.reply_text(job)

# 🔁 Auto checker
async def auto_check():
    bot = Bot(token=TOKEN)

    while True:
        current_jobs = get_jobs()
        old_jobs = load_old_jobs()

        # First run → just save
        if not old_jobs:
            print("First run, saving jobs...")
            save_jobs(current_jobs)

        else:
            new_jobs = [job for job in current_jobs if job not in old_jobs]

            for job in new_jobs:
                await bot.send_message(
                    chat_id=CHAT_ID,
                    text=f"🆕 NEW JOB ALERT:\n{job}"
                )

            if new_jobs:
                print("New jobs sent!")

            save_jobs(current_jobs)

        await asyncio.sleep(1800)  # 30 min


    asyncio.create_task(auto_check())

# 🚀 Main bot setup
app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

app.add_handler(CommandHandler("job", job_command))

print("saroj is legend his bot is running")
app.run_polling()
