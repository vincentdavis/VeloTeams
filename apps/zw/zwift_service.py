from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests
import time

class ZwiftAutoLogin:
    def __init__(self, email, password, driver_path):
        self.email = email
        self.password = password
        self.driver_path = driver_path
        self.driver = None

    def setup_driver(self):
        # Set options for headless browser if necessary
        options = Options()
        options.headless = True  # Set to False if you don't want headless
        self.driver = webdriver.Chrome(options=options)

    def login(self):
        self.driver.get('https://www.zwift.com/eu/sign-in')
        self.driver.find_element(By.ID, 'email-input').send_keys(self.email)
        self.driver.find_element(By.ID, 'password-input').send_keys(self.password)
        self.driver.find_element(By.ID, 'password-input').send_keys(Keys.RETURN)
        time.sleep(10)  # Replace with more robust wait

    def get_access_token(self):
        accessToken = self.driver.execute_script("return window.ZPageData.sessionTokens")
        return accessToken.get('accessToken')

    def get_profile_info(self):
        accessToken = self.get_access_token()
        response = requests.get('https://us-or-rly101.zwift.com/api/profiles/me', headers={
            'Authorization': 'Bearer ' + accessToken,
            'Accept': 'application/json'
        })
        return response.status_code, response.content

    def close(self):
        self.driver.quit()

# usage:
email = ''
password = ''
driver_path = ''

zwift_login = ZwiftAutoLogin(email, password, driver_path)
zwift_login.setup_driver()
zwift_login.login()
status_code, content = zwift_login.get_profile_info()
print(status_code)
print(content)
zwift_login.close()
