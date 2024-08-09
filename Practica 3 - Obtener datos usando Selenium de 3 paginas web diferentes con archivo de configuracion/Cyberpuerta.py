import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def load_config(filename="configCyber.json"):
    """Cargar la configuración desde un archivo JSON."""
    with open(filename, "r") as file:
        return json.load(file)

def perform_action(driver, action):
    """Realizar una acción específica según la configuración."""
    try:
        if action["action"] == "open_page":
            driver.get(action["url"])
            
        
        elif action["action"] == "input":
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((getattr(By, action["selector_type"].upper()), action["selector_value"]))
            )
            element.send_keys(action["input_value"])
            
        
        elif action["action"] == "click":
            element = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((getattr(By, action["selector_type"].upper()), action["selector_value"]))
            )
            element.click()
            
        
        elif action["action"] == "wait":
            time.sleep(action["wait_time"])
            
        
        elif action["action"] == "extract":
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((getattr(By, action["selector_type"].upper()), action["selector_value"]))
            )
            
            return element
        
        elif action["action"] == "extract_all":
            elements = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((getattr(By, action["selector_type"].upper()), action["selector_value"]))
            )
            
            return elements

    except Exception as e:
        return None

def extract_product_data(product):
    """Extraer datos del producto usando los selectores proporcionados en la configuración."""
    try:
        product_link = product.find_element(By.CLASS_NAME, "emproduct_right_title")
        product_title = product_link.get_attribute("title")
    except Exception as e:
        product_title = "Título no disponible"

    try:
        price_container = product.find_element(By.CLASS_NAME, "emproduct_left_attribute_price")
        price_element = price_container.find_element(By.CLASS_NAME, "emproduct_right_price_left")
        product_price = price_element.find_element(By.CLASS_NAME, "price").text
    except Exception as e:
        product_price = "Precio no disponible"

    return {
        "title": product_title,
        "price": product_price
    }

def main():
    config = load_config()
    driver = webdriver.Firefox()  # Cambia a Chrome() si prefieres usar Chrome

    # Ejecutar acciones de configuración
    for action in config["actions"]:
        result = perform_action(driver, action)
        if action["action"] == "extract_all":
            if result:
                products = result
                products_data = []
                for product in products:
                    data = extract_product_data(product)
                    products_data.append(data)
                df = pd.DataFrame(products_data)
                df.to_excel(config["actions"][-1]["file_name"], index=False)
                print(f"Los datos de productos se han guardado en '{config['actions'][-1]['file_name']}'.")

    driver.quit()

if __name__ == "__main__":
    main()
