from flask import Flask, render_template, request
from datetime import datetime
from telegram import Bot
import asyncio
import pytz

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/groups", methods=["POST"])
def get_groups():
    token = request.form["token"]
    bot = Bot(token)
    try:
        updates = asyncio.run(bot.get_updates())
        groups = []
        now = datetime.now(pytz.timezone("Asia/Bangkok"))
        
        for update in updates:
            if update.message and update.message.chat.type in ["group", "supergroup"]:
                diff = now - update.message.date.astimezone(pytz.timezone("Asia/Bangkok"))
                minutes = diff.total_seconds() / 60
                
                if minutes < 60:
                    last_activity = f"{int(minutes)} นาทีที่แล้ว"
                else:
                    hours = int(minutes / 60)
                    last_activity = f"{hours} ชั่วโมงที่แล้ว"
                
                groups.append({
                    "id": update.message.chat.id,
                    "title": update.message.chat.title,
                    "last_activity": last_activity
                })
        return render_template("groups.html", groups=groups, token=token)
    except Exception as e:
        return str(e)


@app.route("/messages", methods=["POST"])
def get_messages():
    token = request.form["token"]
    chat_id = request.form["chat_id"]
    bot = Bot(token)
    try:
        updates = asyncio.run(bot.get_updates())
        messages = []
        for update in updates:
            if update.message and str(update.message.chat.id) == chat_id:
                thai_tz = pytz.timezone("Asia/Bangkok")
                messages.append(
                    {
                        "text": update.message.text,
                        "date": update.message.date.astimezone(thai_tz).strftime(
                            "%Y-%m-%d %H:%M"
                        ),
                    }
                )
        return render_template("messages.html", messages=messages)
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(debug=True)
