import csv
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager


SCROLL_DELAY = 10

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://opensea.io/assets?search[resultModel]=ASSETS&search[sortAscending]=false&search["
           "sortBy]=LAST_SALE_DATE")

WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.ID, "main")))
main = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/div/div[3]/div[2]/div[2]/div/div")
# xpath = "/html/body/div[1]/div/div/main/div/div/div[3]/div[2]/div[2]/div/div/div[1]"

with open("nft_urls.csv", mode="w") as csv_file:
    driver.fullscreen_window()

    writer = csv.writer(csv_file)
    links = set()
    counter = 0

    while True:
        if len(links) % 10 == 0:
            print(len(links))

        divs = main.find_elements(By.XPATH, 'div')
        for div in divs:
            link = div.find_element(By.XPATH, "div/article/a").get_attribute("href")

            if link in links:
                print(f'already found id: {counter}')
                counter += 1
            else:
                links.add(link)
                writer.writerow([link])

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.ID, "main")))
        time.sleep(SCROLL_DELAY)
