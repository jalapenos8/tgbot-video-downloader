import json
import pickle
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selfunc import getCookie, getID
from request import getLinks
import os


def whoAreYou(filePath, userID):  # check if user allowed to use bot
    print(f"Checking user ID: {userID}")
    with open(filePath, "r") as file:
        for line in file:
            if line.strip() == str(userID):
                return True
    return False


def doAll(url):
    loginSession = getCookie()
    urlObject = getID(loginSession, url)
    if urlObject["pageFound"]:
        objectID = urlObject["id"]
        links = getLinks(loginSession, objectID)
        return {"linkValid": True, "links": links}
    else:
        return {"linkValid": False, "links": []}


token_api = os.getenv("TG_TOKEN")
password = os.getenv("PASSWORD")
users_file_path = "users.txt"


async def handlerLol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if whoAreYou(users_file_path, update.message.from_user.id):
        if "https://www.storyblocks.com/video/stock" == update.message.text[:39]:
            await context.bot.send_message(
                update.message.chat.id, "Запрос получен. Ждите..."
            )
            receivedText = update.message.text.strip()
            answer = doAll(receivedText)
            if answer["linkValid"]:
                [firstLink, secondLink] = answer["links"]
                firstLine = f"\n4K : [Скачать]({firstLink})" if (firstLink) else ""
                secondLine = f"\nHD : [Скачать]({secondLink})" if (secondLink) else ""
                text = f"Ссылки для скачивания: {firstLine} {secondLine}"
                await context.bot.send_message(
                    update.message.chat.id, text, parse_mode="MarkdownV2"
                )
            else:
                await context.bot.send_message(
                    update.message.chat.id, "Страницы не существует"
                )
        else:
            await context.bot.send_message(
                update.message.chat.id, "Неправильная ссылка"
            )
    else:
        receivedText = update.message.text
        if receivedText == password:
            with open(users_file_path, "a") as file:
                file.write(str(update.message.from_user.id) + "\n")
            await context.bot.send_message(
                update.message.chat.id,
                "Пароль правильный! Дайте ссылку на видео со StoryBlocks",
            )
        else:
            await context.bot.send_message(update.message.chat.id, "Напишите пароль")


if __name__ == "__main__":
    # Load cookies from a JSON file
    with open("cookies.json", "r") as f:
        cookies = json.load(f)

    # Save cookies into a pickle file
    with open("cookies.pkl", "wb") as f:
        pickle.dump(cookies, f)

    print("✅ Cookies converted and saved to cookies.pkl")
    application = ApplicationBuilder().token(token_api).build()
    handlerLolLol = MessageHandler(filters.ChatType.PRIVATE, handlerLol)
    application.add_handler(handlerLolLol)
    application.run_polling(poll_interval=1)
