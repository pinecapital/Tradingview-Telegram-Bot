from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.options import Options
import time
import config
# from replit import db
from datetime import datetime
from threading import Thread
import telegrambot
from tkinter import Tk
import os 
import pyperclip

from dotenv import load_dotenv

load_dotenv()


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

def setup():
    print('--->Setup selenium start : ' + str(datetime.now()))
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode.
    # chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration.
   
    chrome_options.add_argument("--window-size=1280,720")
    chrome_options.add_experimental_option("prefs", {
        # "resolution": "768X432"  # Adjust this as needed
        "resolution": "1280X720"
        # "resolution": "1920X1080"

    })

    # Set up WebDriver with ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    print('Setup selenium complete')
    return driver


def screenshot(driver, chart, ticker, adjustment=100,save_path='./photo.png'):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    print('--->Opening Chart ' + chart + ' : ' + str(datetime.now()))

    chartUrl = config.urls["tvchart"] + chart + '/' + (
        '?symbol=' + ticker) if ticker != 'NONE' else ''
    print('Chart URL :', chartUrl)

    driver.get(chartUrl)
    print('Sleep for 10 seconds - wait for chart to load')
    time.sleep(10)
    print('Adjusting position by ', adjustment)
    actions = ActionChains(driver)
    actions.send_keys(Keys.ESCAPE).perform()
    actions.send_keys(Keys.RIGHT * adjustment).perform()
    time.sleep(3)
    print('Chart is ready for capture')
    ActionChains(driver).key_down(Keys.ALT).key_down('s').key_up(
        Keys.ALT).perform()
    time.sleep(3)
    # clipboard = pyperclip.paste()  # get the clipboard content
    driver.save_screenshot(save_path)
    print(f"Screenshot saved at {save_path}")

    return save_path
    # return clipboard


def quit_browser(driver):
    print('--->Exit browser : ' + str(datetime.now()))
    driver.close()
    driver.quit()


def send_chart(chart, ticker, message, delivery):
    driver = setup()
    try:
        driver.get("https://www.tradingview.com")
        sessionId = os.getenv('sessionid')
        print('Session Id Used :', sessionId)
        driver.add_cookie({
            'name': 'sessionid',
            'value': sessionId,
            'domain': '.tradingview.com'
        })
        screenshot_path = screenshot(driver, chart, ticker)

        if delivery != 'asap':
            if os.path.exists(screenshot_path):

                telegrambot.sendMessage(message, screenshot_path)  # Include the actual screenshot
            else:
                print("Screenshot not found, sending message only.")
                telegrambot.sendMessage(message)
    finally:
        quit_browser(driver)



def send_chart_async(chartUrl, ticker='NONE', message='', delivery='asap'):
    try:
        capture = Thread(target=send_chart,
                         args=[chartUrl, ticker, message, delivery])
        capture.start()
    except Exception as e:
        print("[X] Capture error:\n>", e)
