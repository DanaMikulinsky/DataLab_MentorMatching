import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def scrape_gras_2024(driver):
    """
    Scrape the Global Ranking of Academic Subjects (GRAS) 2024
    by ensuring the correct dropdown is selected and "High Quality Research" is chosen.
    """
    driver.get("https://www.shanghairanking.com/rankings/gras/2024")
    time.sleep(3)

    # Collect (category, subcategory_text, subcategory_url)
    cat_subcat_links = []
    subject_items = driver.find_elements(By.CSS_SELECTOR, "div.subject-container div.subject-item")
    for item in subject_items:
        try:
            category_elem = item.find_element(By.CSS_SELECTOR, ".subject-category .subject-title")
            category = category_elem.text.strip()
        except:
            continue

        sub_links = item.find_elements(By.CSS_SELECTOR, ".subject-list a.subj-link")
        for link in sub_links:
            sub_text = link.text.strip()
            href = link.get_attribute("href")
            cat_subcat_links.append((category, sub_text, href))

    all_results = []

    # For each sub-category, open the page and scrape
    for category, subcat, url in cat_subcat_links:
        print(f"\nProcessing: {category} - {subcat}")  # Debug log
        driver.get(url)
        time.sleep(3)

        # Identify the correct dropdown by checking the available options
        dropdowns = driver.find_elements(By.CSS_SELECTOR, "div.rank-select .head-bg")
        print(f"Found {len(dropdowns)} potential dropdowns")  # Debug log
        correct_dropdown = None

        for dropdown in dropdowns:
            # Click the dropdown to reveal options
            dropdown.click()
            time.sleep(1)
            options = driver.find_elements(By.CSS_SELECTOR, "ul.options li")
            option_texts = [opt.text.strip() for opt in options]
            print(f"Dropdown options: {option_texts}")  # Debug log

            if "High Quality Research" in option_texts:
                correct_dropdown = dropdown
                print("Found dropdown with 'High Quality Research' option")  # Debug log
                break
            else:
                # Close this dropdown if it's the wrong one
                driver.find_element(By.CSS_SELECTOR, "body").click()

        # Change value to "High Quality Research"
        if correct_dropdown:
            correct_dropdown.click()  # Open the correct dropdown again
            time.sleep(1)
            
            try:
                # Find the option by its text content
                high_quality_option = driver.find_element(
                    By.XPATH, 
                    "//li[text()='High Quality Research']"
                )
                
                # First try regular click
                try:
                    high_quality_option.click()
                except:
                    # If regular click fails, try JavaScript click
                    driver.execute_script("arguments[0].click();", high_quality_option)
                
                time.sleep(2)
                print("Successfully clicked High Quality Research option")  # Debug log
                
            except Exception as e:
                print(f"Error clicking option: {str(e)}")  # Debug log
                continue
        else:
            print(f"Warning: No dropdown with 'High Quality Research' found for {subcat}")
            continue

        # Paginate & scrape
        while True:
            rows = driver.find_elements(By.CSS_SELECTOR, "table tr[data-v-ae1ab4a8]")
            for row in rows:
                # University name
                name_elems = row.find_elements(By.CSS_SELECTOR, "a > span[data-v-a91a96c2].univ-name")
                if not name_elems:
                    continue
                university_name = name_elems[0].text.strip()

                # 'High Quality Research' rank is in the last <td>
                tds = row.find_elements(By.TAG_NAME, "td")
                if not tds:
                    continue
                ranking_text = tds[-1].text.strip()

                all_results.append([category, subcat, university_name, ranking_text])

            # Pagination
            next_btns = driver.find_elements(By.CSS_SELECTOR, "ul.ant-pagination li.ant-pagination-next")
            if not next_btns:
                break
            next_btn_class = next_btns[0].get_attribute("class")
            if "ant-pagination-disabled" in next_btn_class:
                break
            next_btns[0].click()
            time.sleep(2)

    return all_results


def main():
    # Start a simple Chrome session
    service = Service()  # Assumes chromedriver is in your PATH
    driver = webdriver.Chrome(service=service)

    try:
        # Scrape GRAS 2024 (categorized) -> categorized_rankings.csv
        gras_data = scrape_gras_2024(driver)
        with open("categorized_rankings.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["category", "sub-category", "university", "ranking"])
            writer.writerows(gras_data)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
