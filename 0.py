from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Configure Selenium to use Chrome in headless mode
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the YouTube video URL
url = "https://www.youtube.com/watch?v=pQsdygaYcE4"  # Replace with your URL
driver.get(url)

# Scroll to the bottom of the page repeatedly to load more comments
scroll_pause_time = 2  # Pause to allow loading of comments
num_scrolls = 20  # Number of scrolls

for _ in range(num_scrolls):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(scroll_pause_time)

# Extract comments
comments = driver.find_elements(By.XPATH, '//*[@id="content-text"]')
comments_list = [comment.text for comment in comments]

# Close the driver
driver.quit()

# Convert the comments to a DataFrame
reviews_data = pd.DataFrame(comments_list, columns=['Comment'])

# Process the comments as needed (example: clean and analyze)
# ...

# Output the DataFrame or perform further analysis
print(reviews_data)
