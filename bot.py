import config
import random
import time

from datetime import datetime, timedelta
from playsound import playsound
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])


class SeleniumDriver():
    def __init__(self):
        self.driver = webdriver.Chrome('chromedriver', options=chrome_options)
        self.driver.get('https://fp.trafikverket.se/boka/#/licence')
        self.driver.implicitly_wait(0.1)
        self.continue_running = True
    def select_exam(self):
        try:
            while self.driver.title == "Förarprov - Bokning":
                WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "social-security-number-input"))
                ).send_keys(config.social_security)
                self.driver.find_element(By.XPATH, f"//*[@title='{config.license_type}']").click()
        except:
            pass
    def select_exam_type(self):
        try:
            exam_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//select[@id='examination-type-select']/option[text()='{config.exam}']"))
            ).click()
        except:
            pass
    def select_rent_or_language(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//select[@id='vehicle-select']/option[text()='{config.rent_or_language}']"))
            ).click()
        except:
            pass
    def select_location(self, location):
        self.location = location
        try:
            location_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "id-control-searchText-1-1"))
            )
            location_element.clear()
            location_element.send_keys(self.location, Keys.ENTER)
        except:
            pass
    def select_time(self, first_date, last_date):
        self.first_date = first_date
        self.last_date = last_date
        try:
            WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//*[text()='Lediga provtider']"))
            )
            self.first_date = datetime.strptime(self.first_date, '%Y-%m-%d').date()
            self.last_date = datetime.strptime(self.last_date, '%Y-%m-%d').date()
            while self.first_date < self.last_date:
                try:
                    find_date = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{str(self.first_date)}')]")
                    if find_date:
                        find_date.find_element(By.XPATH, f"//*[text()='Välj']").click()
                        return False
                except:
                    pass
                finally:
                    if self.first_date <= self.last_date:
                        self.first_date = self.first_date + timedelta(days=1)
        except:
            pass
        return True
    def refresh_page(self):
        return self.driver.refresh()

def find_exam(driver, period=[60, 5 * 60, 1], speed=[5, 50, 0.1]):
    periods = list(map(lambda value: period[-1] * value, range(*period[:2])))
    speeds = list(map(lambda value: speed[-1] * value, range(*speed[:2])))
    playsound('sounds/horn.wav')
    driver.select_exam()
    while driver.continue_running:
        for i in config.locations:
            try:
                driver.select_exam_type()
                time.sleep(random.choice(speeds))
                driver.select_rent_or_language()
                time.sleep(random.choice(speeds))
                if driver.continue_running:
                    driver.select_location(i)
                    time.sleep(random.choice(speeds))
                    for j in range(0, len(config.dates), 2):
                        driver.continue_running = driver.select_time(config.dates[j], config.dates[j+1])
                        time.sleep(random.choice(speeds))
                        if not driver.continue_running:
                            timestamp = datetime.now() + timedelta(minutes=15)
                            while datetime.now() < timestamp:
                                playsound('sounds/alert.mp3')
                            break
            except:
                pass
        driver.refresh_page()
        time.sleep(random.choice(periods))

if __name__ == '__main__':
    find_exam(SeleniumDriver())
