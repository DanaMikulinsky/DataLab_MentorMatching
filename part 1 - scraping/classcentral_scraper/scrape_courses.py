import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Selenium WebDriver
options = webdriver.ChromeOptions()
# REMOVE '--headless' so you can SEE the browser in action
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the website
url = "https://www.classcentral.com/collection/top-free-online-courses"
driver.get(url)

# Wait for the page to load
wait = WebDriverWait(driver, 10)

# Scroll down and load all courses
while True:
    try:
        load_more_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-name="LOAD_MORE"]'))
        )
        print("Clicking 'Load More'...")
        driver.execute_script("arguments[0].click();", load_more_button)
        time.sleep(2)  # Wait for new courses to load
    except:
        print("No more 'Load More' button found.")
        break

# Extract course details
course_data = []
courses = driver.find_elements(By.CSS_SELECTOR, "a.color-charcoal.course-name")
for course in courses:
    try:
        course_name = course.find_element(By.CSS_SELECTOR, "h2[itemprop='name']").text
        course_link = "https://www.classcentral.com" + course.get_attribute("href")

        # Extract rating from JSON-like attribute
        data_props = course.get_attribute("data-track-props")
        data_dict = json.loads(data_props.replace("&quot;", '"'))
        course_rating = data_dict.get("course_avg_rating", "N/A")

        course_data.append({
            "course_name": course_name,
            "course_link": course_link,
            "course_rating": course_rating
        })
    except Exception as e:
        print(f"Error extracting course: {e}")

# Close the browser
driver.quit()

# Save results to CSV
df = pd.DataFrame(course_data)
df.to_csv("top_courses.csv", index=False, encoding="utf-8")

print("✅ Scraping complete! Data saved to `top_courses.csv`.")
