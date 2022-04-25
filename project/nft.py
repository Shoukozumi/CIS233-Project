from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
import time

"""No need to run this file, just used for reference"""

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://opensea.io/assets/matic/0x71aacdb40a3cec7aa95674fa4dfdbbf5e28608aa/2981")

# get name:
xpath = "/html/body/div[1]/div/main/div/div/div/div[1]/div/div[1]/div[2]/section[1]/h1"
WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.XPATH, xpath)))
name = driver.find_element(By.XPATH, xpath).get_attribute("innerText")

# get owner:
xpath = "/html/body/div[1]/div/main/div/div/div/div[1]/div/div[1]/div[2]/section[2]/div/div/a/span"
owner = driver.find_element(By.XPATH, xpath).get_attribute("innerText")

# get all time average price:
xpath = "/html/body/div[1]/div/main/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div[1]/div[" \
        "2]/div/div/div[2] "
avg_price = driver.find_element(By.XPATH, xpath).get_attribute("innerText")

# get details: contract address, token ID, token Standard, Blockchain
xpath = "/html/body/div[1]/div/main/div/div/div/div[1]/div/div[1]/div[1]/section/div/div[4]/div/div/div/div/div"
details = driver.find_element(By.XPATH, xpath)

contract_address = details.find_element(By.XPATH, "div[1]/span/a").get_attribute("innerText")
contract_token_id = details.find_element(By.XPATH, "div[2]/span/a").get_attribute("innerText")
contract_token_standard = details.find_element(By.XPATH, "div[3]/span").get_attribute("innerText")
contract_blockchain = details.find_element(By.XPATH, "div[4]/span").get_attribute("innerText")

# get item activity:
xpath = "/html/body/div[1]/div/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/section/div"
activity_filter = driver.find_element(By.XPATH, xpath)
activity_filter.click()
xpath = "/html/body/div[1]/div/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/section/ul/li[2]"
filter_sales = driver.find_element(By.XPATH, xpath)
filter_sales.click()
xpath = "/html/body/div[1]/div/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div"
activity_content = driver.find_element(By.XPATH, xpath)
time.sleep(30)
print(activity_content.get_attribute("innerHTML"))
