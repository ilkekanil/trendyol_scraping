from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the browser
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# wait to avoid loading problems
driver.implicitly_wait(10)

website = 'https://www.trendyol.com/sanaozel/1?versionKey=singleProducts_JFY_Original_Woman_Deng'
driver.get(website)

all_names = []
all_brands = []
all_prices = []
all_ratings = []
all_evaluation = []
all_attributes = []

# Wait for products
wait = WebDriverWait(driver, 30)
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scraping
    try:
        names = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'p-card-wrppr')))
    except:
        break  # If products don't load, exit the loop
    
    for name in names:
        try:
            name_two = name.find_element(By.CLASS_NAME, 'prdct-desc-cntnr')
            brand = name_two.find_element(By.CLASS_NAME, 'prdct-desc-cntnr-ttl').get_attribute('title')
            all_brands.append(brand)
            print(f"Brand: {brand}")

            title = name_two.find_element(By.CLASS_NAME, 'prdct-desc-cntnr-name').get_attribute('title')
            all_names.append(title)
            print(f"Title: {title}")

            price = name.find_element(By.CLASS_NAME, 'prc-box-sllng').text
            all_prices.append(price)
            print(f"Price: {price}")

            try:
                rating = name.find_element(By.CLASS_NAME, 'rating-score').text
            except:
                rating = None
            print(f"Rating: {rating}")
            all_ratings.append(rating)

            try:
                numOfassessment = name.find_element(By.CLASS_NAME, 'ratingCount').text.strip('()')
            except:
                numOfassessment = None
            print(f"Number of evaluations: {numOfassessment}")
            all_evaluation.append(numOfassessment)

            # Get the product URL and open it in a new tab
            new_url = name.find_element(By.CLASS_NAME, 'p-card-chldrn-cntnr').get_attribute('href')
            driver.execute_script("window.open(arguments[0], '_blank');", new_url)
            driver.switch_to.window(driver.window_handles[-1])

            try:
                attributes = driver.find_elements(By.CLASS_NAME, 'attribute-item')
                product_attributes = [attribute.text for attribute in attributes]
                all_attributes.append(product_attributes)
                print(f"Attributes: {product_attributes}")
            except:
                all_attributes.append(None)
                print("Attributes: None")

            # Closing the tab and switching back to the main window
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        except Exception as e:
            print(f"Error: {e}")

    # Scroll down
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(7)

    new_height = driver.execute_script("return document.body.scrollHeight")
    
    if new_height == last_height:
        after_scroll = driver.find_elements(By.CLASS_NAME, 'p-card-wrppr')
        if len(after_scroll) == len(names):
            break
    last_height = new_height

driver.quit()
