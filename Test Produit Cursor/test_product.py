import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class TestProductCreation:
    @pytest.fixture
    def driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")
        
        # Utiliser le gestionnaire de pilotes intégré de Selenium
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        yield driver
        try:
            driver.quit()
        except:
            pass

    def find_input(self, driver, ids_or_names, timeout=10):
        for by, value in ids_or_names:
            try:
                return WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((by, value))
                )
            except Exception:
                continue
        raise Exception(f"Aucun champ trouvé pour {ids_or_names}")

    def admin_login(self, driver):
        driver.get("http://localhost:3000/admin/login")
        email_input = self.find_input(driver, [
            (By.ID, "email"),
            (By.NAME, "email"),
            (By.XPATH, "//input[contains(translate(@placeholder, 'EMAIL', 'email'), 'email')]")
        ])
        email_input.send_keys("malyy@mail.com")
        password_input = self.find_input(driver, [
            (By.ID, "password"),
            (By.NAME, "password"),
            (By.XPATH, "//input[contains(translate(@placeholder, 'PASSWORD', 'password'), 'password')]")
        ])
        password_input.send_keys("azertyuiopq1")
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'] | //input[@type='submit']"))
        )
        submit_button.click()
        WebDriverWait(driver, 10).until(
            lambda driver: "/login" not in driver.current_url
        )

    def test_create_product(self, driver):
        self.admin_login(driver)
        driver.get("http://localhost:3000/admin/products")
        new_product_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'New Product')]"))
        )
        new_product_button.click()
        fields = {
            "name": "Sabre laser",
            "sku": "1",
            "price": "100",
            "weight": "2",
            "qty": "12",
            "urlKey": "az12"
        }
        for field_id, value in fields.items():
            input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, field_id))
            )
            input_field.clear()
            input_field.send_keys(value)
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'primary')]"))
        )
        save_button.click()
        WebDriverWait(driver, 10).until(
            lambda driver: "/admin/products" in driver.current_url
        )

    
    