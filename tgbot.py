from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selfunc import getCookie, getID
from request import getLinks
import os

def whoAreYou(filePath, userID):      #check if user allowed to use bot
    with open(filePath, "r") as file:
        for line in file:
            if line.strip() == str(userID):
                return True
    return False

def doAll(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    loginSession = getCookie(driver)
    urlObject = getID(driver, url)
    driver.quit()
    if (urlObject['pageFound']):
        objectID = urlObject['id']
        links = getLinks(loginSession, objectID)
        return {'linkValid': True, 'links': links}
    else:
        return {'linkValid': False, 'links': []}

token_api = os.getenv("TG_TOKEN")
password = os.getenv("PASSWORD")
users_file_path = 'users.txt'

async def handlerLol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (whoAreYou(users_file_path, update.message.from_user.id)):
        if ("https://www.storyblocks.com/video/stock" in update.message.text):
            await context.bot.send_message(update.message.chat.id, "Запрос получен. Ждите...")
            receivedText = update.message.text.strip()
            answer = doAll(receivedText)
            if (answer['linkValid']):
                [firstLink, secondLink] = answer['links']
                firstLine = f"\n4K : [Скачать]({firstLink})"if (firstLink) else ""
                secondLine = f"\nHD : [Скачать]({secondLink})"if (secondLink) else ""
                text = f"Ссылки для скачивания: {firstLine} {secondLine}"
                await context.bot.send_message(update.message.chat.id, text, parse_mode="MarkdownV2")
            else:
                await context.bot.send_message(update.message.chat.id, "Страницы не существует")
        else:
            await context.bot.send_message(update.message.chat.id, "Неправильная ссылка")
    else:
        receivedText = update.message.text
        if (receivedText==password):
            with open(users_file_path, "a") as file:
                file.write(str(update.message.from_user.id) + "\n")
            await context.bot.send_message(update.message.chat.id, "Пароль правильный!")
        else:
            await context.bot.send_message(update.message.chat.id, "Напишите пароль")

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    receivedText = update.message.text.strip()
    if (receivedText.split()[1]==password):
        with open(users_file_path, "a") as file:
            file.write(str(update.message.from_user.id) + "\n")
        await context.bot.send_message(update.message.chat.id, "Пароль правильный!")
    else:
        await context.bot.send_message(update.message.chat.id, "Пароль неверный!")


if __name__ == '__main__':
    application = ApplicationBuilder().token(token_api).build()
    handlerLolLol = MessageHandler(filters.ChatType.PRIVATE, handlerLol)
    application.add_handler(handlerLolLol)
    
    application.run_polling(poll_interval=1)