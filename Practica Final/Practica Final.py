import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd

def execute_actions(driver, actions):
    for action in actions:
        print(f"Executing action: {action['description']}")
        if action['action'] == 'select':
            try:
                select_element = WebDriverWait(driver, action.get('waitTime', 10)).until(
                    EC.presence_of_element_located((By.NAME, action['selector']))
                )
                select = Select(select_element)
                option_index = action['index']
                if option_index > 0:  # Skip default option
                    select.select_by_index(option_index)
                time.sleep(action.get('waitTime', 3000) / 1000)
            except Exception as e:
                print(f"Error selecting value: {e}")
        elif action['action'] == 'extract':
            try:
                header_container = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, action['selector']))
                )
                headers = header_container.find_elements(By.CSS_SELECTOR, action['headerSelector'])
                header_texts = [header.text.strip() for header in headers]

                rows = driver.find_elements(By.CSS_SELECTOR, action['tableSelector'])
                table_data = []
                for row in rows:
                    cells = row.find_elements(By.CSS_SELECTOR, "div.col-12.col-xl.m-0.p-0, div.col-12.col-xl-1.m-0.p-0")
                    row_data = [cell.text.strip() for cell in cells]
                    table_data.append(row_data)

                df = pd.DataFrame(table_data, columns=header_texts)
                df.to_excel(action['output'], index=False)
            except Exception as e:
                print(f"Error extracting data: {e}")
        elif action['action'] == 'navigate':
            try:
                driver.get(action['url'])
                time.sleep(action.get('waitTime', 3000) / 1000)
            except Exception as e:
                print(f"Error navigating to URL: {e}")

if __name__ == "__main__":
    with open("config.json", "r") as file:
        config = json.load(file)

    driver = webdriver.Firefox()  # Usa el driver de Chrome

    for subject in config['configurations']:
        driver.get(subject["url"])
        time.sleep(3)  # Esperar para que la página cargue
        execute_actions(driver, subject["actions"])

    driver.quit()
