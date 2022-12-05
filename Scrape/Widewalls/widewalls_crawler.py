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
from tqdm import tqdm

max_clicks = 150

chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
# chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--window-size=1920x1080")
chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
browser = webdriver.Chrome(options=chrome_options)
# browser.get("https://www.widewalls.ch/artists")
browser.get("https://www.widewalls.ch/artists")
run=True
while run:
    try:
        agree_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-1f5z9o6')))
        agree_button.click()
    except:
        pass
    try:
        x_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[href='/_nuxt/6d2608ce6e0b4c594d30174a4b817ca2.svg#i-close-icon']")))
        x_button.click()
    except:
        pass
    # browser.implicitly_wait(20)
    button = WebDriverWait(browser,20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='load more']")))
    """
    click "load more" max_clicks times to load the artists
    each click loads 18 artists
    """
    num_load_more = 0
    while button and num_load_more < max_clicks:
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
            print(f"button clicked {num_load_more} times")
        except ElementClickInterceptedException:
            x_subscribe_button = WebDriverWait(browser,20).until(EC.presence_of_element_located((By.ID, "ZA_CAMP_BUTTON_2")))
            x_subscribe_button.click()
            button.click()
            num_load_more += 1
            print(f"button clicked {num_load_more} times")
        button = WebDriverWait(browser,20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='load more']")))
    
    """
    scrape the artists
    """
    name_xpath = "//*[@id='__layout']/div/div/div[1]/div/div[3]/section/div[1]/div/div/div[2]/div[1]/a"
    artist_name_blocks = browser.find_elements(By.XPATH, name_xpath)
    artist_names = [element.get_attribute("textContent") for element in artist_name_blocks]
    artist_links = [element.get_attribute("href") for element in artist_name_blocks]
    artist_names = [name.strip() for name in artist_names]
    artist_links = [f"{link}" for link in artist_links]
    # print(artist_names[:5])

    bio_xpath = "//*[@id='__layout']/div/div/div[1]/div/div[3]/section/div[1]/div/div/div[2]/div[4]/div"
    artist_bio_blocks = browser.find_elements(By.XPATH, bio_xpath)
    artist_bios = [element.get_attribute("textContent") for element in artist_bio_blocks]

    # print(artist_bios[:5])
    print(len(artist_names))
    print(len(artist_bios))
    link_df = pd.DataFrame({"artist_links":artist_links})
    link_df.to_csv(f"./widewalls_links_{max_clicks}.csv")
    bio_df = pd.DataFrame({"artist_bios":artist_bios})
    bio_df.to_csv(f"./widewalls_bios_{max_clicks}.csv")
    name_df = pd.DataFrame({"artist_names":artist_names})
    name_df.to_csv(f"./widewalls_names_{max_clicks}.csv")
    run = False

full_artist_bios = []
try:
    i=0
    for link in tqdm(link_df['artist_links']):
        i+=1 
        if i == 5:
            break
        try:
            browser.get(link)
            xpath = "//*[@id='artistTabs']/div/ul/li[1]/a"
            button = browser.find_element(By.XPATH, xpath)
            desired_y = (button.size['height'] / 2) + button.location['y']
            window_h = browser.execute_script('return window.innerHeight')
            window_y = browser.execute_script('return window.pageYOffset')
            current_y = (window_h / 2) + window_y
            scroll_y_by = desired_y - current_y

            browser.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
            time.sleep(1)
            button.click()
            bio_xpath = "//*[@id='__layout']/div/div/div[1]/div/div[5]/div/div[2]/div[1]/div[2]/div/p[1]"
            full_bio_element = browser.find_element(By.XPATH, bio_xpath)
            full_bio = full_bio_element.get_attribute("textContent")
            full_artist_bios.append(full_bio)
        except:
            full_artist_bios.append("(n/a)")
    full_bio_df = pd.DataFrame({"full_bios":full_artist_bios})
    full_bio_df.to_csv(f"./widewalls_full_bios_{max_clicks}.csv")
except:
    full_bio_df = pd.DataFrame({"full_bios":full_artist_bios})
    full_bio_df.to_csv(f"./widewalls_full_bios_{max_clicks}.csv")

    
    # artist_blocks = browser.find_elements(By.CLASS_NAME, "ww-c-main-card__body")
    # for artist_block in artist_blocks:
    #     artist_name_block = artist_block.find_element(By.CLASS_NAME, "ww-c-main-card__name ww-u-app-link")
    #     artist_name = artist_name_block.get_attribute("textContent")
    #     artist_bio_block = artist_block.find_element(By.CLASS_NAME, "ww-c-main-card__info")
    #     artist_bio_block = artist_bio_block.find_element(By.TAG, "div")
    #     artist_bio = artist_bio_block.get_attribute("textContent")
    #     print(f"{artist_name}   {artist_bio}")
    