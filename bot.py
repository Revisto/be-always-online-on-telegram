from models import *

SeleniumTelegram = SeleniumTelegram()
SeleniumTelegram.setup_selenium_drive_with_android_useragent()
SeleniumTelegram.go_to_telegram_web_url()
SeleniumTelegram.login_to_telegram_web()