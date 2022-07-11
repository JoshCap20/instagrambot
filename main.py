import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from settings import _username, _password, TAG, OTHER_TAGS

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# 10 seconds is timeout for driver to wait
wait = WebDriverWait(driver, 10)

class InstagramBot:
    tags: list[str] = []

    def __init__(self, tag=TAG):
        if self.instagram_authentication():
            self.search(tag)
            self.image_loop()
            driver.quit()


    def instagram_authentication(self):
        try:
            driver.get("https://instagram.com")
            wait.until(EC.presence_of_element_located((By.NAME, 'username'))).send_keys(_username)
            sleep(1)
            wait.until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(_password)
            sleep(1)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div'))).click()
            print(f"{_username} authenticated successfully")
            sleep(10)
            return True
        except:
            print("Authentication error")
            return False
        

    def search(self, tag):
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'input'))).send_keys(f'#{tag}')
        sleep(5)
        searchresults = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
        sleep(5)
        for searchresult in searchresults:
            self.tags.append(searchresult.get_attribute('href'))
        self.tags = [tag for tag in self.tags if 'https://www.instagram.com/explore/tags/' in tag]
        driver.get(self.tags[0])


    def image_loop(self):
        sleep(5)
        images = driver.find_elements(By.TAG_NAME, 'a')
        hrefs = []
        q = 0
        i = 0
        for image in images:
            hrefs.append(image.get_attribute('href'))
        hrefs = [href for href in hrefs if 'https://www.instagram.com/p/' in href]
        print(hrefs)
        for href in hrefs:
            driver.get(href)
            sleep(4)
            print(driver.current_url)
            if i % 20:
                sleep(12.5*i)
                print(f'RESTING FOR {(12.5*i)/60} MINS')
            sleep(3)
            try:
                self.like()
            except:
                print("Like error")
            try:
                self.comment()
            except:
                print("Comment error")
            i += 1
        q += 1
        if q < len(OTHER_TAGS):
            self.search(OTHER_TAGS[q])


    def like(self, try_again=True, path='//li[2]/div/div/div/div/div[2]'):
        try:
            sleep(2)
            action = ActionChains(driver)
            img = driver.find_element(By.XPATH, path)
        # img.click()
        # img.click()
            action.double_click(img).perform()
            sleep(5)
            print("[SUCCESS] Liked image")
        except:
            if try_again:
                    self.like(try_again=False, path='xpath=//div[2]')
            if not try_again:
                print("Error liking")
        


    def comment(self):
        try:
            sleep(4)
        # try:
                #textbox = driver.find_element(By.CSS_SELECTOR, '.\_aamx .\_abm1 > .\_ab6-')
                #print(1)
            #except:
            textbox = driver.find_element(By.CSS_SELECTOR, '.\_aamx > .\_abl-')
            #    print(2)
            textbox.click()
            sleep(4)
            textarea = driver.find_element(By.XPATH, '//textarea')
            textarea.send_keys("Nice! I like this.")
            sleep(2)
            submit_button = driver.find_element(By.XPATH, '//form/button/div')
            submit_button.click()
            print("Comment done")
        except:
                print("Error Commenting")


Bot1 = InstagramBot()
