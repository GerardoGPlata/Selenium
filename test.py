from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import tabulate as tb

# Initialize the Firefox driver (make sure you have geckodriver in your PATH)
driver = webdriver.Firefox()

# Load the SIAAUTT login page
driver.get("https://uttorreon.mx/")

try:
    # Wait for the email and password inputs to be present
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
except TimeoutException:
    print("Error: Some elements were not found on the page.")
    driver.quit()
    
# Fill in the login credentials
email_input.send_keys("20170056")  # Replace with your actual email/username
password_input.send_keys("GAPG940611HCLLLR04")  # Replace with your actual password

# Click the login button
login_button.click()

# Wait for the page to load
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Cerrar sesión')]"))
    )
    print("Login successful!")
except TimeoutException:
    print("Error: Login failed.")

# Buscar el elemento <span class="fa fa-th"></span<span class="xn-text">Mi Espacio</span>
mi_espacio = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//span[@class='fa fa-th']"))
)
mi_espacio.click()

# Buscar el elemento <span class="item-text">Finanzas</span>
finanzas = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Finanzas')]"))
)
finanzas.click()


# Buscar el elemento <span class="item-text">Mis Pagos</span>
mis_pagos = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Mis Pagos')]"))
)
mis_pagos.click()

# Buscar el elemento <button type="button" class="btn btn-default  dropdown-toggle" data-toggle="dropdown"><span class="page-size">10</span> <span class="caret"></span></button>
dropdown = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-default  dropdown-toggle']"))
)
dropdown.click()
