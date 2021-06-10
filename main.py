import csv
import configparser
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

# Read config.ini file
config = configparser.ConfigParser()
config.read("config.ini")

# Config selenium
PATH = config["SELENIUM"]["PATH_DRIVER"]
options = webdriver.ChromeOptions()
options.binary_location = config["SELENIUM"]["BINARY_LOCATION"]

driver = webdriver.Chrome(PATH, options=options)
driver.implicitly_wait(240)
driver.get("https://leetcode.com/accounts/login/")

# Login
username = driver.find_element_by_id("id_login")
password = driver.find_element_by_id("id_password")
username.send_keys(config["LEETCODE"]["USER"])
password.send_keys(config["LEETCODE"]["PASSWORD"])

while driver.current_url != "https://leetcode.com/":
    try:
        singin = driver.find_element_by_id("signin_btn")
        singin.click()
    except Exception as e:
        print(e)

# Show all problems

driver.get("https://leetcode.com/problemset/all/")
select = Select(driver.find_element_by_xpath(
    "//*[@id=\"question-app\"]/div/div[2]/div[2]/div[2]/table/tbody[2]/tr/td/span/select"))
select.select_by_value("9007199254740991")

#
auxiliar_element = driver.find_element_by_class_name("text-success")

# Get problems and write csv
with open('leetcode.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['#', 'Nombre', 'Link', 'Resuelto'])
    table = driver.find_element_by_class_name("reactable-data")
    rows = table.find_elements_by_tag_name("tr")
    i = 1
    for row in rows:
        print("problem", i)
        i = i + 1
        colums = row.find_elements_by_tag_name("td")
        writer.writerow([
            colums[1].text,
            colums[2].get_attribute("value"),
            colums[2].find_element_by_tag_name("a").get_attribute("href"),
            colums[0].get_attribute("value") is not None
        ])

driver.close()
