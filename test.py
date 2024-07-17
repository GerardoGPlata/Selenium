import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Cargar la configuración desde el archivo JSON
with open('config.json') as f:
    config = json.load(f)

# Inicializar el driver de Firefox
driver = webdriver.Firefox()

# Iniciar sesión
def iniciar_sesion(driver, config):
    driver.get(config['inicio_sesion']['url'])
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, config['inicio_sesion']['email_input_id']))
    )
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, config['inicio_sesion']['password_input_id']))
    )
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, config['inicio_sesion']['login_button_xpath']))
    )
    email_input.send_keys("20170056")  # Reemplaza con tu email/usuario real
    password_input.send_keys("GAPG940611HCLLLR04")  # Reemplaza con tu contraseña real
    login_button.click()
    time.sleep(3)  # Esperar 3 segundos

# Navegar a 'Mi Espacio'
def navegar_a_mi_espacio(driver, config):
    mi_espacio = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, config['navegacion']['mi_espacio_xpath']))
    )
    mi_espacio.click()
    time.sleep(3)  # Esperar 3 segundos

# Navegar a 'Finanzas'
def navegar_a_finanzas(driver, config):
    finanzas = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, config['navegacion']['finanzas_xpath']))
    )
    finanzas.click()
    time.sleep(3)  # Esperar 3 segundos

# Navegar a 'Mis Pagos'
def navegar_a_mis_pagos(driver, config):
    mis_pagos = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, config['navegacion']['mis_pagos_xpath']))
    )
    mis_pagos.click()
    time.sleep(3)  # Esperar 3 segundos

# Obtener la tabla de pagos
def obtener_tabla_pagos(driver, config):
    tabla_pagos = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, config['tabla_pagos']['id']))
    )
    filas = tabla_pagos.find_elements(By.TAG_NAME, "tr")
    datos = []
    for fila in filas[1:]:  # Comenzar desde la segunda fila para omitir los encabezados
        celdas = fila.find_elements(By.TAG_NAME, "td")
        if celdas:
            datos_fila = [celda.text.strip() for celda in celdas[:-1]]  # Excluir la última celda (Imprimir)
            datos.append(datos_fila)
    return datos

# Main
def main():
    # Iniciar sesión
    iniciar_sesion(driver, config)
    
    # Navegar a 'Mi Espacio'
    navegar_a_mi_espacio(driver, config)
    
    # Navegar a 'Finanzas'
    navegar_a_finanzas(driver, config)
    
    # Navegar a 'Mis Pagos'
    navegar_a_mis_pagos(driver, config)
    
    # Obtener la tabla de pagos
    datos = obtener_tabla_pagos(driver, config)
    
    # Convertir los datos a un DataFrame de pandas
    df = pd.DataFrame(datos, columns=config['tabla_pagos']['columnas'])
    
    # Formatear las columnas numéricas
    df['Total'] = df['Total'].apply(lambda x: f"$ {float(x.replace('$', '').replace(',', '')):.2f}")
    df['Pagado'] = df['Pagado'].apply(lambda x: f"$ {float(x.replace('$', '').replace(',', '')):.2f}")
    
    # Guardar en un archivo de Excel
    excel_filename = "pagos.xlsx"
    df.to_excel(excel_filename, index=False)
    print(f"Los datos de pagos se han guardado en '{excel_filename}'.")
    print("¡Listo!")
    
    # Cerrar el navegador al finalizar
    driver.quit()

if __name__ == "__main__":
    main()