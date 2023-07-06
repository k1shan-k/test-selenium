from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Configure Selenium Grid options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")

# Set desired capabilities for Selenium nodes
desired_capabilities = DesiredCapabilities.CHROME.copy()
desired_capabilities['acceptInsecureCerts'] = True

# Create WebDriver instance with Selenium Grid URL and desired capabilities
driver = webdriver.Remote(
    command_executor='http://selenium-hub:4444/wd/hub',
    options=chrome_options,
    desired_capabilities=desired_capabilities
)

driver.get("http://quotes.toscrape.com")
client = MongoClient('mongodb://localhost:27017/')
db = client['mcs_assignment']
collection = db['quotes']

for page in range(1, 11):
    # Find all quote elements on the page
    quote_elements = driver.find_elements(By.CSS_SELECTOR, ".quote")

    for element in quote_elements:
        # Extract quote and author text from each element
        quote_text = element.find_element(By.CSS_SELECTOR, ".text").text
        author_name = element.find_element(By.CSS_SELECTOR, ".author").text
        print("Quote:", quote_text)
        print("Author:", author_name)
        print()

        document = {
            'quote_id': page * 10 + i,
            'quote': quote_text,
            'author': author_name
        }
        collection.insert_one(document)

    try:
        next_button = driver.find_element(By.CSS_SELECTOR, ".next > a")
        next_button.click()
    except:
        print("No more pages available. Exiting loop.")
        break

driver.quit()
