import time
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class WhatsappScrapper():
    def __init__(self):
        self.driver = self.load_driver()
        # self.page = page
        # Open the web page with the given browser
        # self.driver.get(self.page)

    def load_driver(self, headless=False):
        """ Updated code to create driver for chrome `ONLY` """
        ops = Options()  # create object of Options

        if headless:
            ops.add_argument('--headless')  # headless browser testing

        # prevents browser from closing when function is returned
        ops.add_experimental_option("detach", True)

        driver = webdriver.Chrome(options=ops,  service=Service(
            ChromeDriverManager().install()))

        # driver.get(link)
        return driver
    

    def get_element(self, driver, path, timeout=10, all=False):
        element_present = None

        try:
            if all:
                element_present = WebDriverWait(driver, timeout).until(
                    EC.presence_of_all_elements_located((By.XPATH, path)))
                
            else:
                element_present = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, path)))
            
            

        except TimeoutException:
            print("Timed out waiting for page to load and finding the required web element.")
            print(path)
        finally:
            return element_present
    
    def open_conversation(self, name):  
        """
        Function that search the specified user by the 'name' and opens the conversation.
        """

        while True:
            # for chatter in self.driver.find_element(By.XPATH,"//div[@id='pane-side']/div/div/div/div"):

            ''' wail for 5minutes (300 sec) to open whatsapp''' 
            for chatter in self.get_element(self.driver, path="//div[@id='pane-side']/div/div/div/div", 
                                            timeout=300, all=True):
                
                chatter_path = ".//span[@title='{}']".format(
                    name)

                # Wait until the chatter box is loaded in DOM
                try:
                    WebDriverWait(self.driver, 120).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//span[contains(@title,'{}')]".format(
                                name)))
                    )
                except StaleElementReferenceException:
                    WebDriverWait(self.driver, 120).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//span[contains(@title,'{}')]".format(
                                name)))
                    )

                try:
                    chatter_name = chatter.find_element(By.XPATH, 
                        chatter_path).text
                    if chatter_name == name:
                        chatter.find_element(By.XPATH, 
                            ".//div/div").click()
                        return True
                except Exception as e:
                    pass

    def get_contact_info(self):

        # get name
        contact_name = self.get_element(
            self.driver, path="//*[@id = 'main']/header/div[2]/div[1]/div/span", timeout=120).text
        print('name: ', contact_name)

        # last seen
        try:
            time.sleep(20) 
            # sleeep for 20 sel to let the text change from "click here for contact info" to actual last seen

            # wait for 30 sec for last seen to show up
            last_seen = self.get_element(
                self.driver, path='//*[@id = "main"]/header/div[2]/div[2]/span',timeout=30).text
        except:
            print("last seen not found...")
            last_seen = None

        print('last seen: ', last_seen)
            
        # click profile to view status
        self.get_element(self.driver, path="//*[@id='main']/header/div[2]/div[1]/div/span", timeout=10).click()
        time.sleep(5) # sleep 5 sec for about to load
        
        # trying to get profile pic
        try:
            img_src = self.get_element(
                self.driver, path="//*[@id='app']/div/div/div[6]/span/div/span/div/div/section/div[1]/div[1]/div/img").get_attribute("src")
        except Exception:
            print("Profile picture not found...")
            img_src = None

        print('DP: ', img_src)

        try:
            status = self.get_element(
                self.driver, path='//*[@id="app"]/div/div/div[6]/span/div/span/div/div/section/div[2]', timeout=30).text[6:].strip('\n').replace('\n','\\n')
        
        except Exception:
            status = None
            print("unable to view status")

        # links and docs is the next element (with that XPATH) 
        # when status is not visible
        if 'links and docs' in status: # <space> before 'links' is required
            status = 'Hey there! I am using WhatsApp.'

        print('status: ', status)

        return (contact_name, img_src, last_seen, status)