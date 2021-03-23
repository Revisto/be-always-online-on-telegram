from dotenv import load_dotenv
from os import getenv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import threading
import random
from validator_collection import *
from time import sleep

load_dotenv()

class SeleniumTelegram:

    def __init__(self):
        self.telegram_web_url = "https://web.telegram.org/"
        self.chrome_webdriver_path = getenv("chrome_webdriver_path")
        self.telegram_telephone_code = getenv("telegram_telephone_code")
        self.telegram_telephone_number = getenv("telegram_telephone_number")

    def setup_selenium_drive_with_android_useragent(self):
        options = Options()
        #options.add_argument("--headless")  
        #options.add_argument('--no-sandbox')
        #options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(executable_path=self.chrome_webdriver_path, chrome_options=options)
        self.driver.set_window_size(1920, 1080)

    def go_to_telegram_web_url(self):
        self.driver.get(self.telegram_web_url)
        sleep(10)

    def login_to_telegram_web(self):
        phone_input_elements = self.driver.find_elements_by_class_name("ng-pristine")
        telephone_code = phone_input_elements[1]
        telephone_number = phone_input_elements[2]
        telephone_code.clear()
        telephone_code.send_keys(f"+{self.telegram_telephone_code}")
        telephone_number.send_keys(self.telegram_telephone_number)
        sleep(3)
        self.driver.find_element_by_class_name("login_head_submit_wrap").click()
        sleep(3)
        self.driver.find_element_by_class_name("btn-md-primary").click()

        login_code = TelegramBotInformation().get_user_verification_input("verification")
        self.driver.find_elements_by_class_name("ng-invalid-required")[-1].send_keys(login_code)
        sleep(3)
        self.driver.find_element_by_class_name("login_head_submit_wrap").click()
        sleep(5)
        secound_password_elements = self.driver.find_elements_by_class_name("ng-invalid-required")
        if len(secound_password_elements) == 2:
            secound_password_user_answer = TelegramBotInformation().get_user_verification_input("secound password")
            secound_password_elements[-1].send_keys(secound_password_user_answer)
            sleep(3)
            self.driver.find_element_by_class_name("login_head_submit_wrap").click()
            sleep(5)

    def pretend_to_be_online(self):
        self.driver.find_element_by_xpath("//li[@class='im_dialog_wrap']").click()
        while True:
            sleep(1)
            textarea_element = self.driver.find_element_by_class_name("composer_rich_textarea")
            textarea_element.send_keys(f"I'm online ---- ‌{General().random_string_generator()}")
            textarea_element.send_keys(Keys.RETURN)

import string
class General:
    def random_string_generator(self, size=50):
        letters = string.ascii_letters
        return ( ''.join(random.choice(letters) for i in range(size)) )


class TelegramBotInformation:
    def __init__(self):
        self.chat_id = getenv("chat_id")
        self.bot_access_token = getenv("bot_access_token")

    def get_user_verification_input(self, message):
        def shutdown():
            updater.stop()
            updater.is_idle = False
        def get_input(update, context):
            update.message.reply_text("Done, thanks")
            threading.Thread(target=shutdown).start()
            global user_text_input
            user_text_input = update.message.text
            
        updater = Updater(self.bot_access_token, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(MessageHandler(Filters.text,get_input))
        updater.bot.send_message(chat_id=self.chat_id, text=f"Send me your {message} code")
        updater.start_polling()
        updater.idle()
        return user_text_input