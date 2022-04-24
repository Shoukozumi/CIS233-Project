import csv
import os
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager


from project.scrape_transactions import extract_from_link

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get("https://opensea.io/assets?search[resultModel]=ASSETS&search[sortAscending]=false&search["
           "sortBy]=LAST_SALE_DATE")
# driver.execute_script("document.body.style.zoom='33%';")
time.sleep(10)

WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.ID, "main")))
main = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div/div/div[3]/div[2]/div[2]/div/div")


def collect_data(csv_url, scroll_delay):
    links = set()
    mode = "a" if os.path.isfile(csv_url) else "w"

    # collect previous links
    if mode == "a":
        with open(csv_url, mode="r") as data_file:
            csv_file_reader = csv.reader(data_file, delimiter=',')
            for row in csv_file_reader:
                links.add(row[0])

    # find new links
    with open(csv_url, mode=mode) as data_file:
        num_links = 0
        # original_window = driver.current_window_handle

        while True:
            # link_found = False

            try:
                divs = main.find_elements(By.XPATH, 'div')
            except Exception as e:
                print(e)
                time.sleep(5)
                divs = []
            for div in divs:
                try:
                    link = div.find_element(By.XPATH, "div/article/a").get_attribute("href")
                except Exception as e:
                    print(e)
                    time.sleep(5)
                    continue

                if link and link in links:
                    print('already found id, error')
                elif link:
                    links.add(link)
                    if num_links % 50 == 0:
                        print(f"# of links collected: {num_links}")

                    # scrape link data
                    c = 0
                    s = ''
                    while c < 10:
                        try:
                            s = extract_from_link(link)
                            break
                        except Exception as e:
                            print(e)
                            time.sleep(2)
                            c += 1

                    if c == 10:
                        print(f"error with url: {link}")
                        # link_found = True
                    if s != '':
                        num_links += 1
                        data_file.write(s + '\n')
                        # link_found = True

            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # driver.switch_to.window(original_window)
            # while driver.current_window_handle != original_window:
            #     driver.close()
            html = driver.find_element(By.TAG_NAME, 'html')
            html.send_keys(Keys.PAGE_DOWN)
            print("scrolling...")
            # driver.implicitly_wait(scroll_delay)
            time.sleep(scroll_delay)


if __name__ == "__main__":
    collect_data("../data/new_data.csv", 10)
