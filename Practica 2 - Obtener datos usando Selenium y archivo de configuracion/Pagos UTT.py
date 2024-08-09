import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def load_config(filename="config.json"):
    with open(filename, "r") as file:
        return json.load(file)

def login(driver, config):
    driver.get(config['login']['url'])
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, config['login']['email_input_id']))
    )
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, config['login']['password_input_id']))
    )
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, config['login']['login_button_xpath']))
    )
    email_input.send_keys(config['login']['email'])
    password_input.send_keys(config['login']['password'])
    login_button.click()
    time.sleep(3)

def navigate(driver, actions):
    for action in actions:
        print(f"Executing action: {action['description']}")
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, action['selector']))
        )
        element.click()
        time.sleep(3)

def extract_data(driver, config):
    tabla_pagos = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, config['data_extraction']['tabla_id']))
    )
    filas = tabla_pagos.find_elements(By.TAG_NAME, "tr")
    datos = []
    for fila in filas[1:]:
        celdas = fila.find_elements(By.TAG_NAME, "td")
        if celdas:
            datos_fila = [celda.text.strip() for celda in celdas[:-1]]
            datos.append(datos_fila)
    
    df = pd.DataFrame(datos, columns=config['data_extraction']['column_names'])
    df['Total'] = df['Total'].apply(lambda x: f"$ {float(x.replace('$', '').replace(',', '')):.2f}")
    df['Pagado'] = df['Pagado'].apply(lambda x: f"$ {float(x.replace('$', '').replace(',', '')):.2f}")
    df.to_excel(config['data_extraction']['output_file'], index=False)
    print(f"Los datos de pagos se han guardado en '{config['data_extraction']['output_file']}'.")
    print("¡Listo!")

if __name__ == "__main__":
    config = load_config()
    driver = webdriver.Firefox()
    
    login(driver, config)
    navigate(driver, config['navigation'])
    extract_data(driver, config)
    
    driver.quit()
