from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def get_time_from_etherscan(link):
    global driver

    original_window = driver.current_window_handle
    driver.switch_to.new_window('tab')

    driver.get(link)
    xpath = '/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[4]/div/div[2]'
    timestamp = driver.find_element(By.XPATH, xpath).get_attribute('innerText')
    first_bracket = timestamp.index('(')
    second_bracket = timestamp.index(')')

    driver.close()
    driver.switch_to.window(original_window)

    return timestamp[first_bracket + 1: second_bracket]


def parse_table(element):
    # element is a row
    price = element.find_element(By.CLASS_NAME, "Price--amount").get_attribute('innerText')
    from_element = element.find_elements(By.CLASS_NAME, "AccountLink--ellipsis-overflow")[1]
    from_acc = from_element.get_attribute('innerText')
    from_acc_link = from_element.get_attribute('href')

    to_element = element.find_elements(By.CLASS_NAME, "AccountLink--ellipsis-overflow")[3]
    to_acc = to_element.get_attribute('innerText')
    to_acc_link = to_element.get_attribute('href')

    etherscan_link = element.find_elements(By.CLASS_NAME, "EventTimestamp--link")[0].get_attribute('href')
    time = get_time_from_etherscan(etherscan_link)
    return price + ";" + from_acc + ";" + from_acc_link + ";" + to_acc + ";" + to_acc_link + ";" + time


def check_exists_by_xpath(xpath, webElement=None):
    try:
        if (webElement is None):
            driver.find_element(By.XPATH, xpath)
        else:
            webElement.find_element(By.XPATH, xpath)

    except NoSuchElementException:
        return False
    return True


def check_exists_by_class(className):
    try:
        driver.find_element(By.CLASS_NAME, className)
    except NoSuchElementException:
        return False
    return True


def extract_from_link(link):
    global driver
    driver.get(link)
    # get name:
    xpath = "/html/body/div[1]/div/main/div/div/div/div[1]/div/div[1]/div[2]/section[1]/h1"
    WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.XPATH, xpath)))
    name = driver.find_element(By.XPATH, xpath).get_attribute("innerText")

    # get owner:
    xpath = "/html/body/div[1]/div/main/div/div/div/div[1]/div/div[1]/div[2]/section[2]/div/div/a"
    owner = driver.find_element(By.XPATH, xpath).get_attribute("innerText") if (
        check_exists_by_xpath(xpath)) else 'None'
    owner_link = driver.find_element(By.XPATH, xpath).get_attribute("href") if (
        check_exists_by_xpath(xpath)) else 'None'

    # get all time average price:
    # xpath = "/html/body/div[1]/div/main/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div/div/div/div/div/div/div[1]/div[2]/div/div/div[2]"
    class_name = 'PriceHistoryStats--value'
    avg_price = driver.find_element(By.CLASS_NAME, class_name).get_attribute("innerText")[1:] if (
        check_exists_by_class(class_name)) else 'None'

    print(name, owner, owner_link, avg_price)

    # get details: contract address, token ID, token Standard, Blockchain
    xpath = "/html/body/div[1]/div/main/div/div/div/div[1]/div/div[1]/div[1]/section/div"
    panel = driver.find_element(By.XPATH, xpath)
    children_count = len(panel.find_elements(By.XPATH, './div'))
    xpath = "/html/body/div[1]/div/main/div/div/div/div[1]/div/div[1]/div[1]/section/div/div[{}]/div/div/div/div/div".format(
        children_count)
    details = panel.find_element(By.XPATH, xpath)

    contract_address = details.find_element(By.XPATH, "div[1]/span/a").get_attribute("href")
    last_index = contract_address.rindex('/')
    contract_address = contract_address[last_index + 1:]

    # if (check_exists_by_xpath('div[2]/span/a', details)):
    # 	contract_token_id = details.find_element(By.XPATH, "div[2]/span/a").get_attribute("innerText")
    # else:
    contract_token_id = details.find_element(By.XPATH, "div[2]/span").get_attribute("innerText")

    contract_token_standard = details.find_element(By.XPATH, "div[3]/span").get_attribute("innerText")
    contract_blockchain = details.find_element(By.XPATH, "div[4]/span").get_attribute("innerText")

    print(contract_address, contract_token_id, contract_token_standard, contract_blockchain)
    # remove all filters
    while (check_exists_by_class('EventHistory--filter-pills')):
        filter = driver.find_elements(By.CLASS_NAME, 'EventHistory--filter-pill')[0]
        filter.click()

    if (contract_blockchain != 'Ethereum'):
        return ''

    # get item activity:
    xpath = "/html/body/div[1]/div/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/section/div"
    activity_filter = driver.find_element(By.XPATH, xpath)
    activity_filter.click()
    xpath = "/html/body/div[1]/div/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/section/ul/li[2]"  # CAREFUL: sometiems 2 and sometimes 4
    sale_filter = driver.find_element(By.XPATH, xpath)
    sale_filter.click()  # unclick the transfer options

    time.sleep(1)

    xpath = "/html/body/div[1]/div/main/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div"
    activity_content = driver.find_element(By.XPATH, xpath)
    all_txns = activity_content.find_elements(By.CLASS_NAME, 'EventHistory--row')

    txn_str = parse_table(all_txns[0]) if len(all_txns) > 0 else ''
    for i in range(1, len(all_txns)):
        txn_str += ',' + parse_table(all_txns[i])

    return (
                name + ',' + owner + ',' + owner_link + ',' + avg_price + ',' + contract_address + ',' + contract_token_id + ',' + contract_token_standard +
                ',' + contract_blockchain + ',' + txn_str)


if __name__ == "__main__":
    # k = extract_from_link('https://opensea.io/assets/0x6b00de202e3cd03c523ca05d8b47231dbdd9142b/528')
    # k = extract_from_link('https://opensea.io/assets/0x19cb5b009bdad0dad0404dd860b0bea75465e678/634')
    k = extract_from_link("https://opensea.io/assets/0xc799f57355677a19b91c722734743215513dece5/6430")
    print(k)
