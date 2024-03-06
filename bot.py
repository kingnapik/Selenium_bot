from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import os

def get_currencies(currencies, start, end, export_csv=False):
    Frames = []
    while True:
        try:
            print(currencies)
            my_url = f'https://br.investing.com/currencies/usd-{currencies.lower()}-historical-data'
            option = Options()
            option.headless = False #visible window on False only
            option.add_argument('--ignore-certificate-errors-spki-list')
            driver = webdriver.Chrome(options=option)
            driver.get(my_url)
            driver.maximize_window()
            
            privacy_button = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div/div/div[2]/div/div/button")))
            privacy_button.click()
            

            date_button = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[5]/section/div[8]/div[3]/div/div[2]/span")))
            
            date_button.click()
            start_bar = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[7]/div[1]/input[1]")))
            start_bar.clear()
            start_bar.send_keys(start)

            end_bar = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[7]/div[1]/input[2]")))
            end_bar.clear()
            end_bar.send_keys(end)

            apply_button = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[7]/div[5]/a")))
            apply_button.click()
            sleep(5)

            dataframes = pd.read_html(driver.page_source)
            driver.quit()
            print(f'{currencies} scraped.')

            for dataframe in dataframes:
                if dataframe.columns.to_list() == ['Date', 'Price', 'Open', 'High', 'Low', 'Change%']:
                    df = dataframe
                    break
            Frames.append(df)
            break

        except:
            driver.quit()
            print(f'Failed to scrape {currencies}. Trying again in 30 seconds')
            i = 30
            while i > 0:
                os.system('cls')
                print(f'trying again in {i} seconds')
                i = i-1
                sleep(1)

            continue

get_currencies('eur',1,1)
