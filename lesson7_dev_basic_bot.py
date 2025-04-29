import os
import ptbot
from dotenv import load_dotenv
from pytimeparse import parse
load_dotenv()


TG_TOKEN = os.getenv("API_TG")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def wait(chat_id, question):
    time = parse(question)
    message_id = bot.send_message(chat_id, "Запускаю обратный отсчет")
    bot.create_countdown(time, notify_progress,
                         chat_id=chat_id, message_id=message_id, time=time)
    bot.create_timer(time, choose, chat_id=chat_id, question=question)


def notify_progress(secs_left, chat_id, message_id, time):
    text = (
        f"Осталось секунд: {secs_left}\n"
        f"{render_progressbar(time, time - secs_left)}"
    )
    bot.update_message(chat_id, message_id, text)


def choose(chat_id, question):
    message = "Время вышло!"
    bot.send_message(chat_id, message)


if __name__ == "__main__":
    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(wait)
    bot.run_bot()
