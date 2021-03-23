from dotenv import load_dotenv
from os import getenv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from validator_collection import *
from time import sleep

class SeleniumTelegram:

    def __init__(self):
        load_dotenv()
        self.telegram_web_url = "https://web.telegram.org/"
        self.chrome_webdriver_path = getenv("chrome_webdriver_path")
        self.telegram_telephone_code = getenv("telegram_telephone_code")
        self.telegram_telephone_number = getenv("telegram_telephone_number")

    def setup_selenium_drive_with_android_useragent(self):
        options = Options()
        #options.add_argument("--headless")  
        #options.add_argument('--no-sandbox')
        #options.add_argument('--disable-dev-shm-usage')
        options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 6.0; HTC One M9 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36")
        self.driver = webdriver.Chrome(executable_path=self.chrome_webdriver_path, chrome_options=options)

    def go_to_telegram_web_url(self):
        self.driver.get(self.telegram_web_url)
        sleep(5)

    def login_to_telegram_web(self):
        phone_input_elements = self.driver.find_elements_by_class_name("ng-pristine")
        telephone_code = phone_input_elements[1]
        telephone_number = phone_input_elements[2]
        telephone_code.clear()
        telephone_code.send_keys(f"+{self.telegram_telephone_code}")
        telephone_number.send_keys(self.telegram_telephone_number)
        sleep(1)
        self.driver.find_element_by_class_name("login_head_submit_wrap").click()
        sleep(2)
        self.driver.find_element_by_class_name("btn-md-primary").click()

        login_code = input("enter your login code :")
        self.driver.find_elements_by_class_name("ng-invalid-required")[-1].send_keys(login_code)
        sleep(1)
        self.driver.find_element_by_class_name("login_head_submit_wrap").click()
        sleep(5)
        secound_password_elements = self.driver.find_elements_by_class_name("ng-invalid-required")
        if len(secound_password_elements) == 2:
            secound_password_user_answer = input("enter your secound password:")
            secound_password_elements[-1].send_keys(secound_password_user_answer)
            sleep(1)
            self.driver.find_element_by_class_name("login_head_submit_wrap").click()
