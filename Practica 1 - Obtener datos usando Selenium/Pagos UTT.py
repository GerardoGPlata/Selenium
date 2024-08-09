from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Inicializar el driver de Firefox
driver = webdriver.Firefox()

# Iniciar sesión
url = "https://uttorreon.mx/"
email_input_id = "email"
password_input_id = "password"
login_button_xpath = "//button[@type='submit']"

driver.get(url)
email_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, email_input_id))
)
password_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, password_input_id))
)
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, login_button_xpath))
)
email_input.send_keys("20170056")  # Reemplaza con tu email/usuario real
password_input.send_keys("GAPG940611HCLLLR04")  # Reemplaza con tu contraseña real
login_button.click()
time.sleep(3)  # Esperar 3 segundos

# Navegar a 'Mi Espacio'
mi_espacio_xpath = "//span[@class='fa fa-th']"
mi_espacio = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, mi_espacio_xpath))
)
mi_espacio.click()

# Navegar a 'Finanzas'
finanzas_xpath = "//span[contains(text(), 'Finanzas')]"
finanzas = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, finanzas_xpath))
)
finanzas.click()

# Navegar a 'Mis Pagos'
mis_pagos_xpath = "//span[contains(text(), 'Mis Pagos')]"
mis_pagos = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, mis_pagos_xpath))
)
mis_pagos.click()
time.sleep(3)  # Esperar 3 segundos

# Obtener la tabla de pagos
tabla_pagos_id = "Tabla"
columnas = [
    "Periodo",
    "Folio Recibo",
    "Concepto",
    "Total",
    "Pagado",
    "Estado del Pago",
    "Fecha de vencimiento"
]

tabla_pagos = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, tabla_pagos_id))
)
filas = tabla_pagos.find_elements(By.TAG_NAME, "tr")
datos = []
for fila in filas[1:]:  # Comenzar desde la segunda fila para omitir los encabezados
    celdas = fila.find_elements(By.TAG_NAME, "td")
    if celdas:
        datos_fila = [celda.text.strip() for celda in celdas[:-1]]  # Excluir la última celda (Imprimir)
        datos.append(datos_fila)

# Convertir los datos a un DataFrame de pandas
df = pd.DataFrame(datos, columns=columnas)

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
