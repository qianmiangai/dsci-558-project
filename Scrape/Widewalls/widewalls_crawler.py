# Widewalls crawler to crawl artist biographies
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
import time
import pandas as pd


chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
# chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--window-size=1920x1080")
chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
browser = webdriver.Chrome(options=chrome_options)
# browser.get("https://www.widewalls.ch/artists")
browser.get("https://www.widewalls.ch/artists")

while True:
    agree_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-1f5z9o6')))
    agree_button.click()
    try:
        x_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[href='/_nuxt/6d2608ce6e0b4c594d30174a4b817ca2.svg#i-close-icon']")))
        x_button.click()
    except:
        pass
    # browser.implicitly_wait(20)
    button = WebDriverWait(browser,20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='load more']")))
    """
    click load more 20 times to load the artists
    """
    num_load_more = 0
    while button and num_load_more < 150:
        # ActionChains(browser).move_to_element(button).perform()
        # browser.execute_script("arguments[0].scrollIntoView();", button)
        desired_y = (button.size['height'] / 2) + button.location['y']
        window_h = browser.execute_script('return window.innerHeight')
        window_y = browser.execute_script('return window.pageYOffset')
        current_y = (window_h / 2) + window_y
        scroll_y_by = desired_y - current_y

        browser.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
        time.sleep(1)
        try:
            button.click()
            num_load_more += 1
            print("button clicked")
        except ElementClickInterceptedException:
            x_subscribe_button = WebDriverWait(browser,20).until(EC.presence_of_element_located((By.ID, "ZA_CAMP_BUTTON_2")))
            x_subscribe_button.click()
            button.click()
            num_load_more += 1
            print("button clicked")
        button = WebDriverWait(browser,20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='load more']")))
    
    """
    scrape the artists
    """
    name_xpath = "//*[@id='__layout']/div/div/div[1]/div/div[3]/section/div[1]/div/div/div[2]/div[1]/a"
    artist_name_blocks = browser.find_elements(By.XPATH, name_xpath)
    artist_names = [element.get_attribute("textContent") for element in artist_name_blocks]
    artist_names = [name.strip() for name in artist_names]
    # print(artist_names[:5])

    bio_xpath = "//*[@id='__layout']/div/div/div[1]/div/div[3]/section/div[1]/div/div/div[2]/div[4]/div"
    artist_bio_blocks = browser.find_elements(By.XPATH, bio_xpath)
    artist_bios = [element.get_attribute("textContent") for element in artist_bio_blocks]

    # print(artist_bios[:5])
    print(len(artist_names))
    print(len(artist_bios))
    bio_df = pd.DataFrame({"artist_bios":artist_bios})
    bio_df.to_csv("./widewalls_bios.csv")
    name_df = pd.DataFrame({"artist_names":artist_names})
    name_df.to_csv("./widewalls_names.csv")


    
    # artist_blocks = browser.find_elements(By.CLASS_NAME, "ww-c-main-card__body")
    # for artist_block in artist_blocks:
    #     artist_name_block = artist_block.find_element(By.CLASS_NAME, "ww-c-main-card__name ww-u-app-link")
    #     artist_name = artist_name_block.get_attribute("textContent")
    #     artist_bio_block = artist_block.find_element(By.CLASS_NAME, "ww-c-main-card__info")
    #     artist_bio_block = artist_bio_block.find_element(By.TAG, "div")
    #     artist_bio = artist_bio_block.get_attribute("textContent")
    #     print(f"{artist_name}   {artist_bio}")
    