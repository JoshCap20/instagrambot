from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from settings import _username, _password, COMMENTS, ACCOUNTS
from random import randint


class AccountInstagramBot:
    """Follows accounts specified in settings."""
    accounts: list[str] = ACCOUNTS
    related_accounts: list[str] = []
    successful_comments: dict[str: str] = {}
    related_account_amount: int = 20
    comment_counter: int = 0

    
    def __init__(self):
        print("Initialized AccountInstagramBot")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 10)
        if self.instagram_authentication():
            for account in self.accounts:
                self.related_accounts.clear()
                i: int = 0
                self.related_accounts = self.search(account)
                for i in range(len(self.related_accounts)):
                    self.get_account(i)
                    post = self.grab_post()
                    self.comment(account, post)
                    self.driver.get("https://instagram.com")
                    sleep(2)
                    print(f"{i+1}/{len(self.related_accounts)} for {account}")        
                    i += 1
                print(f"[{self.accounts.index(account)+1}/{len(self.accounts)}] Finished with {account}")
            print("Finished running bot.")
            print(self.successful_comments)
            self.driver.quit()
        else:
            print("Authentication error")

    def instagram_authentication(self, retry=True):
        try:
            self.driver.get("https://instagram.com")
            self.wait.until(EC.presence_of_element_located((By.NAME, 'username'))).send_keys(_username)
            sleep(1)
            self.wait.until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(_password)
            sleep(1)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div'))).click()
            print(f"{_username} authenticated successfully")
            sleep(4)
            if self.driver.current_url == "https://instagram.com":
                if not retry:
                    return False
                sleep(10)
                self.instagram_authentication(retry=False)
            return True
        except:
            return False

        
    def search(self, account):
        """Searches for account."""
        links: list[str] = []
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'input'))).send_keys(account)
        sleep(3)
        searchresults = self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
        sleep(7)
        for searchresult in searchresults[:self.related_account_amount]:
            links.append(searchresult.get_attribute('href'))
        links = [link for link in links if account in link or account[:4] in link]
        print(links)
        return links

    def get_account(self, i):
        """Grabs account"""
        sleep(3)
        if i <= len(self.related_accounts):
            self.driver.get(self.related_accounts[i])
        else:
            print("Whew! Avoided an index error in self.get_account(i).")

    def grab_post(self):
        """Grabs post from account to comment on."""
        sleep(3)
        links: list[str] = []
        images = self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
        sleep(3)
        for image in images[:9]:
            if 'https://www.instagram.com/p/' in image.get_attribute('href'):
                links.append(image.get_attribute('href'))
        print(links)
        post = links[0]
        self.driver.get(post)
        return post

    def comment(self, account, post):
        """Comment post mechanics."""
        if self.comment_counter != 0 and self.comment_counter % 25 == 0:
            sleep(120)
        try:
            sleep(2)
            comment = COMMENTS[randint(0, len(COMMENTS)-1)]
            select_textbox = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.\_aamx > .\_abl-'))).click()
            type_text = self.wait.until(EC.presence_of_element_located((By.XPATH, '//textarea'))).send_keys(comment)
            sleep(2)
            submit_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//form/button/div'))).click()
            print(f"[SUCCESS] Commented: {comment}")
            self.comment_counter += 1
            if account not in self.successful_comments:
                self.successful_comments[account] = post
            else:
                prior = self.successful_comments[account]
                if isinstance(prior, list):
                    new_list: list[str] = []
                    for item in prior:
                        new_list.append(item)
                    new_list.append(post)
                    self.successful_comments[account] = new_list
                else:
                    new_value: list[str] = []
                    new_value.append(prior)
                    new_value.append(post)
                    self.successful_comments[account] = new_value
        except:
            print("[ERROR] Not commented")



class HashtagInstagramBot:
    """Likes and comments on posts given a certain hashtag."""
    tags: list[str] = []
    hrefs: list[str] = []
    
    def __init__(self, tag):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 10)
        if self.instagram_authentication():
            self.search(tag)
            self.image_loop()
            self.driver.quit()


    def instagram_authentication(self):
        try:
            self.driver.get("https://instagram.com")
            self.wait.until(EC.presence_of_element_located((By.NAME, 'username'))).send_keys(_username)
            sleep(1)
            self.wait.until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(_password)
            sleep(1)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div'))).click()
            print(f"{_username} authenticated successfully")
            sleep(7)
            return True
        except:
            print("Authentication error")
            return False
        

    def search(self, tag):
        """Searches hashtag"""
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'input'))).send_keys(f'#{tag}')
        sleep(5)
        searchresults = self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
        sleep(5)
        for searchresult in searchresults:
            self.tags.append(searchresult.get_attribute('href'))
        self.tags = [tag for tag in self.tags if 'https://www.instagram.com/explore/tags/' in tag]
        self.driver.get(self.tags[0])
        sleep(3)


    def image_loop(self):
        """Loops through images with given hashtag."""
        sleep(5)
        images = self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
        for image in images:
            self.hrefs.append(image.get_attribute('href'))
        self.hrefs = [href for href in self.hrefs if 'https://www.instagram.com/p/' in href]
        i: int = 0
        for href in self.hrefs:
            sleep(1)
            self.driver.get(href)
            print(self.driver.current_url)
            if i % 20:
                sleep(12.5*i)
                print(f'RESTING FOR {(12.5*i)/60} MINS')
            try:
                self.like()
            except:
                print("Like error")
            try:
                self.comment()
            except:
                print("Comment error")
            i += 1


    def like(self, try_again=True, path='//li[2]/div/div/div/div/div[2]'):
        """Like post mechanics."""
        try:
            sleep(2)
            action = ActionChains(self.driver)
            img = self.wait.until(EC.presence_of_element_located((By.XPATH, path)))
            action.double_click(img).perform()
            print("[SUCCESS] Liked")
            sleep(2)
        except:
            if try_again:
                self.like(try_again=False, path='xpath=//div[2]')
            if not try_again:
                print("[ERROR] Not liked")
        


    def comment(self):
        """Comment post mechanics."""
        try:
            sleep(2)
            select_textbox = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.\_aamx > .\_abl-'))).click()
            sleep(2)
            type_text = self.wait.until(EC.presence_of_element_located((By.XPATH, '//textarea'))).send_keys(COMMENTS[randint(0, len(COMMENTS)-1)])
            sleep(2)
            submit_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//form/button/div'))).click()
            print("[SUCCESS] Commented")
        except:
            print("[ERROR] Not commented")

# initialize object with hashtag to use

# use this to search by a given hashtag and like and comment under those posts
#Bot1 = HashtagInstagramBot("softwaredeveloper")
# use this to comment on accounts specified in settings
Bot2 = AccountInstagramBot()
