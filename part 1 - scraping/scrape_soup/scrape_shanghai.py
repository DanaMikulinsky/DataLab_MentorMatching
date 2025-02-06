import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def scrape_arwu_2024(driver):
    """
    Scrape the Academic Ranking of World Universities (ARWU) 2024
    from: https://www.shanghairanking.com/rankings/arwu/2024
    
    The requirement is to find:
      - University name in <span data-v-a91a96c2 class="univ-name">...</span>
      - Ranking in the second-to-last <td> inside the <tr/>
    
    Then paginate until no more pages.
    """
    driver.get("https://www.shanghairanking.com/rankings/arwu/2024")
    time.sleep(5)  # Let the page load

    results = []

    while True:
        # Locate all <tr data-v-ae1ab4a8> in the table
        rows = driver.find_elements(By.CSS_SELECTOR, "table tr[data-v-ae1ab4a8]")

        for row in rows:
            try:
                # Grab the university name from the span with data-v-a91a96c2
                univ_span = row.find_element(By.CSS_SELECTOR, 'span[data-v-a91a96c2].univ-name')
                university_name = univ_span.text.strip()
            except:
                # If we can't find it, skip this row
                continue

            # The instructions say the ranking is in the second-to-last <td>
            tds = row.find_elements(By.TAG_NAME, "td")
            if len(tds) < 2:
                # Not a valid row
                continue

            # The last td
            ranking_text = tds[-1].text.strip()

            # Add to our results
            results.append([university_name, ranking_text])

        # Attempt to click the "Next" button in the pagination
        next_btns = driver.find_elements(By.CSS_SELECTOR, "ul.ant-pagination li.ant-pagination-next")
        if not next_btns:
            # No next button found
            break
        
        # Check if the button is disabled
        next_btn_class = next_btns[0].get_attribute("class")
        if "ant-pagination-disabled" in next_btn_class:
            # No more pages to load
            break

        # Otherwise, click the next button and wait
        next_btns[0].click()
        time.sleep(2)

    return results


def scrape_sport_science(driver):
    """
    Scrape the Sport Science Ranking (GRSSSD) 2024
    from: https://www.shanghairanking.com/rankings/grsssd/2024
    
    Requirements:
      - Only take the name if the span.univ-name is a direct child of <a>.
      - First switch the dropdown (in the header <th>) to 'TOP'.
      - The ranking is in the last <td> of each row.
      - Then paginate the same way until no more pages.
    """
    driver.get("https://www.shanghairanking.com/rankings/grsssd/2024")
    time.sleep(5)  # Let the page load

    # 1) Switch the dropdown to "TOP"
    try:
        # Click the input to show the dropdown options
        dropdown_input = driver.find_element(By.CSS_SELECTOR, "div.rank-select .head-bg")
        dropdown_input.click()
        time.sleep(1)

        # Find the LI that has text 'TOP' and click it
        options = driver.find_elements(By.CSS_SELECTOR, "ul.options li")
        for opt in options:
            if opt.text.strip() == 'TOP':
                opt.click()
                break
        time.sleep(2)
    except:
        # If something fails, we just keep going (it might already be on TOP)
        pass

    results = []

    while True:
        rows = driver.find_elements(By.CSS_SELECTOR, "table tr[data-v-ae1ab4a8]")

        for row in rows:
            # Find the <span class="univ-name"> that is a direct child of <a>
            name_elems = row.find_elements(By.CSS_SELECTOR, "a > span.univ-name")
            if not name_elems:
                continue  # This row doesn't have the proper structure

            university_name = name_elems[0].text.strip()

            # Ranking is in the last <td>
            tds = row.find_elements(By.TAG_NAME, "td")
            if not tds:
                continue
            ranking_text = tds[-1].text.strip()

            results.append([university_name, ranking_text])

        # Attempt to click the "Next" button in the pagination
        next_btns = driver.find_elements(By.CSS_SELECTOR, "ul.ant-pagination li.ant-pagination-next")
        if not next_btns:
            break

        next_btn_class = next_btns[0].get_attribute("class")
        if "ant-pagination-disabled" in next_btn_class:
            break

        next_btns[0].click()
        time.sleep(2)

    return results


def main():
    # Start a simple Chrome session (make sure chromedriver is in your PATH).
    service = Service()  # uses default, assuming chromedriver in PATH
    driver = webdriver.Chrome(service=service)

    # 1) Scrape ARWU 2024
    arwu_data = scrape_arwu_2024(driver)
    with open("academic_ranking_world_universities.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["university", "ranking"])
        writer.writerows(arwu_data)

    # # 2) Scrape Sport Science Ranking
    # sport_data = scrape_sport_science(driver)
    # with open("sport_science_ranking.csv", "w", newline="", encoding="utf-8") as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["university", "ranking"])
    #     writer.writerows(sport_data)

    # Done, close the browser
    driver.quit()


if __name__ == "__main__":
    main()
