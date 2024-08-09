import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def load_config(filename="configAmazon.json"):
    """Cargar la configuración desde un archivo JSON."""
    with open(filename, "r") as file:
        return json.load(file)

def perform_action(driver, action, config):
    """Realizar una acción específica según la configuración."""
    if action["action"] == "open_page":
        driver.get(action["url"])
    
    elif action["action"] == "input":
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, action["selector_value"]))
        )
        element.send_keys(action["input_value"])
    
    elif action["action"] == "click":
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, action["selector_value"]))
        )
        element.click()
    
    elif action["action"] == "wait":
        time.sleep(action["wait_time"])
    
    elif action["action"] == "extract":
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((getattr(By, action["selector_type"].upper()), action["selector_value"]))
        )
        return element
    
    elif action["action"] == "extract_all":
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((getattr(By, action["selector_type"].upper()), action["selector_value"]))
        )
        return elements

def extract_product_data(product, config):
    """Extraer datos del producto usando los selectores proporcionados en la configuración."""
    try:
        title_element = product.find_element(By.CSS_SELECTOR, config["actions"][6]["selector_value"])
        product_title = title_element.text
    except Exception as e:
        product_title = "Título no disponible"

    try:
        price_whole_element = product.find_element(By.CSS_SELECTOR, config["actions"][7]["selector_value"])
        price_fraction_element = product.find_element(By.CSS_SELECTOR, config["actions"][8]["selector_value"])
        product_price = f"${price_whole_element.text}.{price_fraction_element.text}"
    except Exception as e:
        product_price = "Precio no disponible"

    return {
        "title": product_title,
        "price": product_price
    }

def main():
    config = load_config()
    driver = webdriver.Chrome()  # Cambia a Firefox() si prefieres usar Firefox

    # Ejecutar acciones de configuración
    for action in config["actions"]:
        if action["action"] in ["open_page", "input", "click", "wait"]:
            perform_action(driver, action, config)
        elif action["action"] in ["extract", "extract_all"]:
            result = perform_action(driver, action, config)
            if action["action"] == "extract_all":
                products = result
                products_data = []
                for product in products:
                    data = extract_product_data(product, config)
                    products_data.append(data)
                df = pd.DataFrame(products_data)
                df.to_excel(config["actions"][-1]["file_name"], index=False)
                print(f"Los datos de productos se han guardado en '{config['actions'][-1]['file_name']}'.")
    
    driver.quit()

if __name__ == "__main__":
    main()
