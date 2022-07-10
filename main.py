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

def instagram_authentication():
    try:
        driver.get("https://instagram.com")
        sleep(6)
        username = driver.find_element(By.NAME, 'username')
        username.send_keys(_username)
        sleep(1)
        password = driver.find_element(By.NAME, 'password')
        password.send_keys(_password)
        sleep(1)
        submit = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div')
        submit.click()
        print("Authenticated")
    except:
        instagram_authentication()
        print("Error authenticating.... Retrying")
    if driver.current_url != 'https://instagram.com':
        print("Succ")
    else:
        sleep(10)
        instagram_authentication()
    

def search(tag=TAG):
    tags = []
    searchbar = driver.find_element(By.TAG_NAME, 'input')
    searchbar.send_keys(f'#{tag}')
    sleep(4)
    searchresults = driver.find_elements(By.TAG_NAME, 'a')
    sleep(1)
    for searchresult in searchresults:
        tags.append(searchresult.get_attribute('href'))
    print(tags)
    tags = [tag for tag in tags if 'https://www.instagram.com/explore/tags/' in tag]
    driver.get(tags[0])


def image_loop():
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
        if i % 20 == 0:
            sleep(12.5*i)
            print(f'RESTING FOR {(12.5*i)/60} MINS')
        sleep(3)
        try:
            like()
        except:
            print("Like error")
        try:
            comment()
        except:
            print("Comment error")
        i += 1
    q += 1
    if q < len(OTHER_TAGS):
        search(OTHER_TAGS[q])


def like(try_again=True, path='//li[2]/div/div/div/div/div[2]'):
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
                like(try_again=False, path='xpath=//div[2]')
        if not try_again:
            print("Error liking")
    


def comment():
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
        try:
            print("Error commenting [path not here]")
        except:
            print("Error Commenting [1]")


def main():
    try:
        instagram_authentication()
        try:
            sleep(7)
            search()
            try:
                sleep(5)
                image_loop()
            except:
                print("Image_loop error")
        except:
            print("Search error")
    except:
        print("Authentication error")
    finally:
        sleep(5)
        driver.quit()
        sys.exit()

if __name__ == "__main__":
    main()
